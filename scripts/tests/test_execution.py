import sys
from pathlib import Path
from unittest import mock

import pytest

pytest.importorskip("rclpy")

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

import execute.run_benchmark as benchmark  # noqa: E402


def test_retry_loop_retries_and_discards_failed_iterations():
    attempts = []
    benchmark.MAX_RETRIES = 2
    benchmark.RETRY_COOLDOWN = 0

    def run_once(iteration, attempt):
        attempts.append((iteration, attempt))
        if attempt < 2:
            raise RuntimeError("simulator crashed")
        return (1.0,)

    assert benchmark.run_iteration_with_retries(3, run_once, sleep=lambda _value: None) == (1.0,)
    assert attempts == [(3, 1), (3, 2)]


def test_keyboard_interrupt_is_not_retried():
    with pytest.raises(KeyboardInterrupt):
        benchmark.run_iteration_with_retries(1, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()), sleep=lambda _value: None)


def test_render_fps_policy_is_backend_specific():
    assert benchmark.render_fps_limit_method("unity") == "early"
    assert benchmark.render_fps_limit_method("mujoco") == "late"
    assert benchmark.render_fps_uses_mangohud_limiter("unity")
    assert not benchmark.render_fps_uses_mangohud_limiter("mujoco")
