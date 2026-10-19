import os
import signal
import subprocess
import sys
import time
import unittest
from pathlib import Path

import psutil


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from execute.process_supervisor import ProcessGroupSupervisor


PYTHON = sys.executable


def python_command(*statements):
    return [PYTHON, "-c", "; ".join(statements)]


def sleeping_command(ignore_sigint=False, ignore_sigterm=False):
    statements = ["import os,signal,time"]
    if ignore_sigint:
        statements.append("signal.signal(signal.SIGINT, signal.SIG_IGN)")
    else:
        statements.append("signal.signal(signal.SIGINT, lambda *_: os._exit(0))")
    if ignore_sigterm:
        statements.append("signal.signal(signal.SIGTERM, signal.SIG_IGN)")
    statements.append("time.sleep(60)")
    return python_command(*statements)


def make_supervisor(commands, graceful=0.25, terminate=0.25):
    return ProcessGroupSupervisor(
        commands,
        graceful_timeout=graceful,
        terminate_timeout=terminate,
        kill_timeout=0.5,
        logger=lambda _message: None,
    )


class ProcessGroupSupervisorTests(unittest.TestCase):
    def test_single_integrated_launch_command_is_supported(self):
        supervisor = make_supervisor((sleeping_command(),))
        before_start = time.monotonic()
        supervisor.start()
        try:
            self.assertIsNotNone(supervisor.launch_started_monotonic)
            self.assertGreaterEqual(supervisor.launch_started_monotonic, before_start)
            self.assertLessEqual(supervisor.launch_started_monotonic, time.monotonic())
        finally:
            self.assertFalse(supervisor.stop().survivors)

    def test_three_launch_commands_are_supported(self):
        supervisor = make_supervisor((sleeping_command(), sleeping_command(), sleeping_command()))
        supervisor.start()
        self.assertFalse(supervisor.stop().survivors)

    def test_unrelated_identical_command_survives(self):
        command = sleeping_command()
        unrelated = subprocess.Popen(command, start_new_session=True)
        supervisor = make_supervisor((command, command))
        try:
            supervisor.start()
            report = supervisor.stop()
            self.assertFalse(report.survivors)
            self.assertIsNone(unrelated.poll())
            self.assertNotEqual(report.sid, os.getsid(unrelated.pid))
        finally:
            if unrelated.poll() is None:
                os.killpg(unrelated.pid, signal.SIGKILL)
                unrelated.wait()

    def test_sigint_handler_can_finish_gracefully(self):
        command = python_command(
            "import signal,sys,time",
            "signal.signal(signal.SIGINT, lambda *_: sys.exit(0))",
            "time.sleep(60)",
        )
        supervisor = make_supervisor((command, command), graceful=1.0)
        supervisor.start()
        time.sleep(0.1)
        report = supervisor.stop()
        self.assertEqual(report.signals_sent, ("SIGINT",))
        self.assertFalse(report.survivors)

    def test_escalates_to_sigterm(self):
        command = sleeping_command(ignore_sigint=True)
        supervisor = make_supervisor((command, command))
        supervisor.start()
        time.sleep(0.1)
        report = supervisor.stop()
        self.assertEqual(report.signals_sent[:2], ("SIGINT", "SIGTERM"))
        self.assertNotIn("SIGKILL", report.signals_sent)
        self.assertFalse(report.survivors)

    def test_escalates_to_sigkill(self):
        command = sleeping_command(ignore_sigint=True, ignore_sigterm=True)
        supervisor = make_supervisor((command, command))
        supervisor.start()
        time.sleep(0.1)
        report = supervisor.stop()
        self.assertEqual(report.signals_sent, ("SIGINT", "SIGTERM", "SIGKILL"))
        self.assertFalse(report.survivors)

    def test_first_command_launch_failure_leaves_nothing(self):
        supervisor = make_supervisor(
            (["/definitely/missing/first-benchmark-command"], sleeping_command())
        )
        with self.assertRaisesRegex(RuntimeError, "could not start"):
            supervisor.start()
        self.assertFalse(supervisor.session_members())

    def test_second_command_launch_failure_cleans_first(self):
        supervisor = make_supervisor(
            (sleeping_command(), ["/definitely/missing/second-benchmark-command"])
        )
        with self.assertRaisesRegex(RuntimeError, "could not start"):
            supervisor.start()
        self.assertFalse(supervisor.session_members())

    def test_exited_launch_command_is_reported_while_other_processes_live(self):
        failed_command = python_command("import sys", "sys.exit(7)")
        supervisor = make_supervisor((failed_command, sleeping_command()))
        supervisor.start()
        try:
            deadline = time.monotonic() + 2
            failure = None
            while time.monotonic() < deadline and failure is None:
                failure = supervisor.command_failure
                time.sleep(0.01)
            self.assertEqual(
                failure,
                "Launch command 1 exited unexpectedly with status 7",
            )
            self.assertTrue(supervisor.session_members())
        finally:
            self.assertFalse(supervisor.stop().survivors)

    def test_shell_wrapper_descendants_are_cleaned(self):
        wrapper = ["bash", "-c", "sleep 60 & child=$!; wait \"$child\""]
        supervisor = make_supervisor((wrapper, sleeping_command()))
        supervisor.start()
        time.sleep(0.1)
        self.assertGreaterEqual(len(supervisor.session_members()), 4)
        self.assertFalse(supervisor.stop().survivors)

    def test_job_control_subgroup_is_detected_and_cleaned(self):
        wrapper = ["bash", "-c", "set -m; sleep 60 & child=$!; wait \"$child\""]
        supervisor = make_supervisor((wrapper, sleeping_command()))
        supervisor.start()
        time.sleep(0.1)
        groups = {os.getpgid(process.pid) for process in supervisor.session_members()}
        self.assertGreaterEqual(len(groups), 2)
        self.assertFalse(supervisor.stop().survivors)

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux subreaper support")
    def test_double_fork_setsid_escape_is_adopted_and_cleaned(self):
        daemonizer = python_command(
            "import os,signal,time",
            "signal.signal(signal.SIGINT, lambda *_: os._exit(0))",
            "pid=os.fork()",
            "(os._exit(0) if pid else None)",
            "os.setsid()",
            "time.sleep(60)",
        )
        supervisor = make_supervisor((daemonizer, sleeping_command()))
        supervisor.start()
        time.sleep(0.15)
        owned_sessions = {os.getsid(process.pid) for process in supervisor.owned_processes()}
        self.assertIn(supervisor.sid, owned_sessions)
        self.assertGreaterEqual(len(owned_sessions), 2)
        self.assertFalse(supervisor.stop().survivors)

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux subreaper support")
    def test_adopted_exited_descendant_is_reaped(self):
        short_lived_daemon = python_command(
            "import os",
            "pid=os.fork()",
            "(os._exit(0) if pid else None)",
            "os._exit(0)",
        )
        supervisor = make_supervisor((short_lived_daemon, sleeping_command()))
        supervisor.start()
        try:
            time.sleep(0.2)
            helper = psutil.Process(supervisor.supervisor_process.pid)
            zombies = [
                child.pid
                for child in helper.children(recursive=True)
                if child.status() == psutil.STATUS_ZOMBIE
            ]
            self.assertFalse(zombies)
        finally:
            self.assertFalse(supervisor.stop().survivors)

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux PDEATHSIG")
    def test_helper_cleans_session_if_controller_is_killed(self):
        controller_code = (
            "import sys,time; "
            f"sys.path.insert(0, {str(SCRIPT_DIR)!r}); "
            "from execute.process_supervisor import ProcessGroupSupervisor; "
            f"command={sleeping_command()!r}; "
            "supervisor=ProcessGroupSupervisor((command,), logger=lambda *_: None); "
            "supervisor.start(); print(supervisor.sid, flush=True); time.sleep(60)"
        )
        controller = subprocess.Popen(
            [PYTHON, "-c", controller_code],
            stdout=subprocess.PIPE,
            text=True,
        )
        try:
            sid = int(controller.stdout.readline().strip())
            controller.kill()
            controller.wait(timeout=2)
            deadline = time.monotonic() + 7
            while time.monotonic() < deadline:
                owned = []
                for process in psutil.process_iter(["pid", "status"]):
                    try:
                        if process.info["status"] != "zombie" and os.getsid(process.pid) == sid:
                            owned.append(process.pid)
                    except (OSError, psutil.Error):
                        continue
                if not owned:
                    break
                time.sleep(0.05)
            self.assertFalse(owned)
        finally:
            if controller.poll() is None:
                controller.kill()
                controller.wait()
            if controller.stdout is not None:
                controller.stdout.close()

    def test_stop_is_idempotent(self):
        supervisor = make_supervisor((sleeping_command(), sleeping_command()))
        supervisor.start()
        first = supervisor.stop()
        second = supervisor.stop()
        self.assertIs(first, second)


if __name__ == "__main__":
    unittest.main()
