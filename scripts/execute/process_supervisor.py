#!/usr/bin/env python3

"""Iteration-owned POSIX process lifecycle management.

Each iteration is launched by a small helper that becomes the leader of a new
session.  The session, rather than an executable name, is the ownership
boundary.  This matters because shells and launch systems may create additional
process groups inside the session; scanning only the helper's initial PGID
would miss those groups.
"""

from __future__ import annotations

import ctypes
import json
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

import psutil


@dataclass(frozen=True)
class CleanupReport:
    """Result of stopping one iteration-owned session."""

    pgid: int
    sid: int | None
    signals_sent: tuple[str, ...]
    survivors: tuple[int, ...]
    elapsed_seconds: float


class ProcessGroupSupervisor:
    """Start benchmark commands and stop every process in their session.

    POSIX forbids a process in the caller's session from joining a group in a
    newly created session.  Therefore a helper process starts a new session and
    launches the configured command(s) from inside it. Cleanup enumerates all
    members of that session and signals each of its process groups, so nested
    shell job control cannot evade ownership cleanup.
    """

    def __init__(
        self,
        commands: Sequence[Sequence[str]],
        environment: dict[str, str] | None = None,
        logger: Callable[[str], None] = print,
        graceful_timeout: float = 10.0,
        terminate_timeout: float = 5.0,
        kill_timeout: float = 1.0,
        final_cleanup_timeout: float = 30.0,
    ) -> None:
        if not 1 <= len(commands) <= 3:
            raise ValueError("An iteration requires one to three launch commands")
        if any(
            not command
            or any(not isinstance(argument, str) or not argument for argument in command)
            for command in commands
        ):
            raise ValueError("Launch commands must contain non-empty strings")
        if min(
            graceful_timeout,
            terminate_timeout,
            kill_timeout,
            final_cleanup_timeout,
        ) < 0:
            raise ValueError("Cleanup timeouts must not be negative")

        self.commands = [list(command) for command in commands]
        self.environment = None
        if environment:
            self.environment = dict(os.environ)
            self.environment.update(environment)
        self.logger = logger
        self.graceful_timeout = graceful_timeout
        self.terminate_timeout = terminate_timeout
        self.kill_timeout = kill_timeout
        self.final_cleanup_timeout = final_cleanup_timeout
        self.supervisor_process: subprocess.Popen[bytes] | None = None
        self.pgid: int | None = None
        self.sid: int | None = None
        self._cleanup_report: CleanupReport | None = None
        self._status_reader: int | None = None
        self._command_failure: str | None = None
        # This timestamp is produced by the session helper immediately after
        # it creates the first simulator process.  ``time.monotonic`` uses a
        # system-wide clock, so the parent can safely use it as the benchmark
        # startup origin without counting ROS listener setup.
        self.launch_started_monotonic: float | None = None

    def start(self) -> None:
        """Start all configured commands in one isolated session."""
        if self.supervisor_process is not None:
            raise RuntimeError("Process supervisor has already been started")

        ready_reader, ready_writer = os.pipe()
        status_reader, status_writer = os.pipe()
        os.set_blocking(status_reader, False)
        self._status_reader = status_reader
        try:
            try:
                self.supervisor_process = subprocess.Popen(
                    [
                        sys.executable,
                        str(Path(__file__).resolve()),
                        "--supervise",
                        json.dumps(self.commands),
                        json.dumps(self.environment),
                        str(ready_writer),
                        str(status_writer),
                    ],
                    start_new_session=True,
                    pass_fds=(ready_writer, status_writer),
                )
            except BaseException:
                os.close(ready_reader)
                self._close_status_reader()
                raise
        finally:
            os.close(ready_writer)
            os.close(status_writer)

        try:
            self.pgid = os.getpgid(self.supervisor_process.pid)
            self.sid = os.getsid(self.supervisor_process.pid)
            self.logger(
                f"Iteration session started: supervisor_pid={self.supervisor_process.pid}, "
                f"pgid={self.pgid}, sid={self.sid}"
            )
            try:
                ready = os.read(ready_reader, 4096)
            except BaseException:
                self.stop()
                raise
        finally:
            os.close(ready_reader)

        try:
            ready_payload = json.loads(ready.decode())
            launch_started_monotonic = ready_payload["launch_started_monotonic"]
            if not isinstance(launch_started_monotonic, (int, float)):
                raise ValueError("launch timestamp is not numeric")
        except (UnicodeDecodeError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            self.stop()
            raise RuntimeError("Process supervisor could not start all commands")
        self.launch_started_monotonic = float(launch_started_monotonic)

    @property
    def processes(self) -> tuple[subprocess.Popen[bytes], ...]:
        """Direct child processes held by this controller."""
        return () if self.supervisor_process is None else (self.supervisor_process,)

    @property
    def returncode(self) -> int | None:
        """Return the helper status, or ``None`` while commands are active."""
        return None if self.supervisor_process is None else self.supervisor_process.poll()

    @property
    def command_failure(self) -> str | None:
        """Describe the first top-level launch command that exited unexpectedly."""
        if self._command_failure is not None or self._status_reader is None:
            return self._command_failure
        try:
            message = os.read(self._status_reader, 4096)
        except BlockingIOError:
            return None
        except OSError:
            self._close_status_reader()
            return self._command_failure
        if message:
            self._command_failure = message.decode(errors="replace").strip()
        else:
            self._close_status_reader()
        return self._command_failure

    def _close_status_reader(self) -> None:
        if self._status_reader is None:
            return
        try:
            os.close(self._status_reader)
        except OSError:
            pass
        self._status_reader = None

    def owned_processes(self) -> list[psutil.Process]:
        """Return live session members plus descendants that called ``setsid``."""
        if self.sid is None or self.supervisor_process is None:
            return []

        members: dict[int, psutil.Process] = {}
        for process in psutil.process_iter(["pid", "status"]):
            try:
                if process.info["status"] == psutil.STATUS_ZOMBIE:
                    continue
                if os.getsid(process.info["pid"]) == self.sid:
                    members[process.pid] = process
            except (ProcessLookupError, PermissionError, psutil.Error, OSError):
                continue

        # Linux subreaper adoption keeps double-forked descendants below the
        # helper.  Recursive ancestry also catches a direct child that starts
        # its own session before it can be adopted.
        try:
            helper = psutil.Process(self.supervisor_process.pid)
            for process in (helper, *helper.children(recursive=True)):
                if process.status() != psutil.STATUS_ZOMBIE:
                    members[process.pid] = process
        except (psutil.Error, OSError):
            pass
        return list(members.values())

    def session_members(self) -> list[psutil.Process]:
        """Compatibility name for all owned processes, including SID escapees."""
        return self.owned_processes()

    def group_members(self) -> list[psutil.Process]:
        """Compatibility alias returning all session members, including subgroups."""
        return self.owned_processes()

    def _member_ids(self) -> list[int]:
        return sorted(process.pid for process in self.owned_processes())

    def _log_members(self, phase: str) -> list[int]:
        survivors = self._member_ids()
        self.logger(f"Iteration session {self.sid} after {phase}: survivors={survivors}")
        return survivors

    def _signal_session(self, sig: signal.Signals) -> bool:
        """Signal every process group currently belonging to the owned session."""
        groups: set[int] = set()
        for process in self.owned_processes():
            try:
                groups.add(os.getpgid(process.pid))
            except (ProcessLookupError, PermissionError, psutil.Error, OSError):
                continue

        sent = False
        for pgid in sorted(groups):
            try:
                os.killpg(pgid, sig)
                sent = True
                self.logger(f"Sent {sig.name} to iteration pgid={pgid}, sid={self.sid}")
            except ProcessLookupError:
                continue
            except PermissionError as exc:
                self.logger(f"Could not send {sig.name} to pgid={pgid}: {exc}")
        return sent

    def _wait_until_empty(self, timeout: float) -> bool:
        deadline = time.monotonic() + timeout
        next_update = 0.0
        while True:
            owned = self.owned_processes()
            if not owned:
                return True
            now = time.monotonic()
            if now >= deadline:
                return False
            if now >= next_update:
                self.logger(
                    f"Waiting for {len(owned)} owned processes: "
                    f"{max(0.0, deadline - now):.1f}s grace remaining"
                )
                next_update = now + 1.0
            time.sleep(min(0.05, max(0.0, deadline - now)))

    def stop(self) -> CleanupReport:
        """Idempotently stop the iteration with INT -> TERM -> KILL escalation."""
        if self._cleanup_report is not None:
            return self._cleanup_report

        started = time.monotonic()
        signals_sent: list[str] = []
        if self.sid is None or self.pgid is None:
            self._cleanup_report = CleanupReport(0, None, (), (), 0.0)
            return self._cleanup_report

        phases = (
            (signal.SIGINT, self.graceful_timeout, "SIGINT grace period"),
            (signal.SIGTERM, self.terminate_timeout, "SIGTERM grace period"),
            (signal.SIGKILL, self.kill_timeout, "SIGKILL grace period"),
        )
        survivors = self._member_ids()
        for sig, timeout, phase in phases:
            if not survivors:
                break
            if self._signal_session(sig):
                signals_sent.append(sig.name)
            self._wait_until_empty(timeout)
            survivors = self._log_members(phase)

        # A process can still be completing kernel I/O or disappearing from
        # psutil just after the initial SIGKILL grace period.  Do not let a
        # subsequent benchmark start while that session remains alive:
        # rescan it and repeat SIGKILL for a bounded final recovery period.
        # Repeated SIGKILL is harmless and also covers a child that forked in
        # the small interval between the initial group enumeration and signal.
        recovery_deadline = time.monotonic() + self.final_cleanup_timeout
        while survivors and time.monotonic() < recovery_deadline:
            self._signal_session(signal.SIGKILL)
            remaining = max(0.0, recovery_deadline - time.monotonic())
            self._wait_until_empty(min(1.0, remaining))
            survivors = self._log_members("final SIGKILL recovery")

        for process in self.processes:
            try:
                process.wait(timeout=0.5)
            except (subprocess.TimeoutExpired, ChildProcessError):
                pass
        self._close_status_reader()

        elapsed = time.monotonic() - started
        self._cleanup_report = CleanupReport(
            self.pgid,
            self.sid,
            tuple(signals_sent),
            tuple(survivors),
            elapsed,
        )
        self.logger(
            f"Iteration cleanup finished: pgid={self.pgid}, sid={self.sid}, "
            f"signals={signals_sent}, survivors={survivors}, elapsed={elapsed:.2f}s"
        )
        return self._cleanup_report


def _run_supervised(
    commands: Sequence[Sequence[str]],
    environment: dict[str, str] | None,
    ready_fd: int,
    status_fd: int,
) -> int:
    """Launch commands from inside the new session created by the parent."""
    children: list[subprocess.Popen[bytes]] = []
    parent_lost = False
    failure_reported = False

    def keep_helper_alive(_signum: int, _frame: object) -> None:
        # SIGINT is also delivered to the helper.  Children get their own
        # chance to shut down, while the helper remains able to reap them.
        return None

    def handle_parent_loss(_signum: int, _frame: object) -> None:
        nonlocal parent_lost
        parent_lost = True

    signal.signal(signal.SIGINT, keep_helper_alive)
    signal.signal(signal.SIGTERM, keep_helper_alive)
    signal.signal(signal.SIGHUP, handle_parent_loss)
    _enable_child_subreaper()
    _enable_parent_death_signal(signal.SIGHUP)
    try:
        launch_started_monotonic = None
        for index, command in enumerate(commands):
            children.append(subprocess.Popen(command, env=environment or None))
            # The first command is the simulator launch.  Record the instant
            # it has actually been created, rather than the time spent
            # preparing ROS subscriptions or launching optional companions.
            if index == 0:
                launch_started_monotonic = time.monotonic()
        if launch_started_monotonic is None:  # Defensive: commands is validated by the parent.
            raise RuntimeError("No launch commands were provided")
        os.write(
            ready_fd,
            json.dumps(
                {"launch_started_monotonic": launch_started_monotonic},
                separators=(",", ":"),
            ).encode(),
        )
        os.close(ready_fd)
        ready_fd = -1
        helper = psutil.Process()
        while True:
            direct_children_running = False
            for index, child in enumerate(children):
                returncode = child.poll()
                if returncode is None:
                    direct_children_running = True
                elif not failure_reported:
                    failure_reported = True
                    message = (
                        f"Launch command {index + 1} exited unexpectedly "
                        f"with status {returncode}"
                    )
                    try:
                        os.write(status_fd, message.encode())
                    except OSError:
                        pass
            _reap_adopted_zombies(helper, children)
            if not direct_children_running and not _live_children(helper):
                break
            if parent_lost:
                print(
                    "Benchmark controller disappeared; cleaning its iteration session.",
                    file=sys.stderr,
                    flush=True,
                )
                _stop_owned_from_helper(helper)
                return 1
            time.sleep(0.05)
        return 0 if all(child.returncode == 0 for child in children) else 1
    except (OSError, ValueError) as exc:
        print(f"Process supervisor could not launch a command: {exc}", file=sys.stderr)
        if ready_fd >= 0:
            try:
                os.write(ready_fd, b"E")
            except OSError:
                pass
            os.close(ready_fd)
            ready_fd = -1
        # Keep the helper/subreaper alive while the controller performs the
        # same scoped escalation used for an ordinary iteration shutdown.
        helper = psutil.Process()
        while True:
            direct_children_running = any(child.poll() is None for child in children)
            _reap_adopted_zombies(helper, children)
            if not direct_children_running and not _live_children(helper):
                break
            time.sleep(0.05)
        return 1
    finally:
        try:
            os.close(status_fd)
        except OSError:
            pass
        if ready_fd >= 0:
            try:
                os.write(ready_fd, b"E")
            except OSError:
                pass
            os.close(ready_fd)
        for child in children:
            if child.poll() is None:
                child.terminate()
        for child in children:
            try:
                child.wait(timeout=1)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()


def _enable_child_subreaper() -> None:
    """Adopt orphaned descendants on Linux so daemonization stays observable."""
    if not sys.platform.startswith("linux"):
        return
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER
            error_number = ctypes.get_errno()
            raise OSError(error_number, os.strerror(error_number))
    except (AttributeError, OSError) as exc:
        print(f"Warning: could not enable child subreaper: {exc}", file=sys.stderr)


def _enable_parent_death_signal(death_signal: signal.Signals) -> None:
    """Ask Linux to notify the helper if its benchmark controller disappears."""
    if not sys.platform.startswith("linux"):
        return
    parent_pid = os.getppid()
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(1, int(death_signal), 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
            error_number = ctypes.get_errno()
            raise OSError(error_number, os.strerror(error_number))
        # Close the race where the parent exits between getppid() and prctl().
        if os.getppid() != parent_pid:
            os.kill(os.getpid(), death_signal)
    except (AttributeError, OSError) as exc:
        print(f"Warning: could not configure parent-death signal: {exc}", file=sys.stderr)


def _helper_owned_processes(helper: psutil.Process) -> list[psutil.Process]:
    """Enumerate the helper session and adopted descendants without names."""
    owned: dict[int, psutil.Process] = {}
    try:
        sid = os.getsid(helper.pid)
    except OSError:
        return []
    for process in psutil.process_iter(["pid", "status"]):
        try:
            if process.info["status"] != psutil.STATUS_ZOMBIE and os.getsid(process.pid) == sid:
                owned[process.pid] = process
        except (ProcessLookupError, PermissionError, psutil.Error, OSError):
            continue
    try:
        for process in helper.children(recursive=True):
            if process.status() != psutil.STATUS_ZOMBIE:
                owned[process.pid] = process
    except (psutil.Error, OSError):
        pass
    return list(owned.values())


def _stop_owned_from_helper(helper: psutil.Process) -> None:
    """Fallback cleanup used only when the external controller has died."""
    helper_pid = helper.pid
    for sent_signal, timeout in (
        (signal.SIGINT, 2.0),
        (signal.SIGTERM, 2.0),
        (signal.SIGKILL, 1.0),
    ):
        processes = [
            process for process in _helper_owned_processes(helper)
            if process.pid != helper_pid
        ]
        if not processes:
            return
        groups: set[int] = set()
        for process in processes:
            try:
                groups.add(os.getpgid(process.pid))
            except (ProcessLookupError, PermissionError, psutil.Error, OSError):
                continue
        # Send the helper's own group last. It ignores INT/TERM; KILL may end
        # it together with a stubborn same-group descendant, which is correct
        # after both grace periods have expired.
        helper_group = os.getpgrp()
        ordered_groups = sorted(groups - {helper_group})
        if helper_group in groups:
            ordered_groups.append(helper_group)
        for pgid in ordered_groups:
            try:
                os.killpg(pgid, sent_signal)
            except ProcessLookupError:
                continue
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not any(
                process.pid != helper_pid
                for process in _helper_owned_processes(helper)
            ):
                return
            time.sleep(0.05)


def _live_children(helper: psutil.Process) -> bool:
    try:
        return any(
            child.status() != psutil.STATUS_ZOMBIE
            for child in helper.children(recursive=True)
        )
    except (psutil.Error, OSError):
        return False


def _reap_adopted_zombies(
    helper: psutil.Process,
    launched_children: Sequence[subprocess.Popen[bytes]],
) -> None:
    """Reap orphaned descendants adopted by the Linux subreaper.

    ``Popen.poll``/``wait`` owns the original direct children. Descendants
    that double-fork become direct children of the helper and otherwise remain
    zombies until the helper itself exits.
    """
    if not sys.platform.startswith("linux"):
        return
    launched_pids = {child.pid for child in launched_children}
    try:
        adopted_children = helper.children(recursive=False)
    except (psutil.Error, OSError):
        return
    for child in adopted_children:
        if child.pid in launched_pids:
            continue
        try:
            if child.status() == psutil.STATUS_ZOMBIE:
                os.waitpid(child.pid, os.WNOHANG)
        except (ChildProcessError, ProcessLookupError, psutil.Error, OSError):
            continue


if __name__ == "__main__" and len(sys.argv) == 6 and sys.argv[1] == "--supervise":
    raise SystemExit(
        _run_supervised(
            json.loads(sys.argv[2]),
            json.loads(sys.argv[3]),
            int(sys.argv[4]),
            int(sys.argv[5]),
        )
    )
