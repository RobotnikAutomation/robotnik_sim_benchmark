import sys
from pathlib import Path

import pytest

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from simulators import SimulatorLaunchContext, get_adapter  # noqa: E402
from simulators.adapters import ADAPTERS, AdapterConfigurationError  # noqa: E402
from validate.validate_config import load_config  # noqa: E402


def context(simulator, entry, *, fps=60):
    return SimulatorLaunchContext(
        simulator=simulator,
        world=entry["world"],
        robot_count=entry["robot_count"],
        robot_model=entry["robot_model"],
        headless=entry["headless"],
        use_rviz=entry["use_rviz"],
        render_fps=fps,
    )


def entry_for(simulator):
    return load_config()[simulator]["two_robot_empty_world_rviz"]


def test_registry_contains_all_backends():
    assert set(ADAPTERS) == {"gazebo_harmonic", "webots", "isaac_sim", "unity", "o3de", "mujoco"}


@pytest.mark.parametrize("simulator", sorted(ADAPTERS))
def test_adapter_builds_a_common_declarative_launch_plan(simulator, tmp_path):
    entry = entry_for(simulator)
    plan = get_adapter(simulator, entry, tmp_path).build_launch_plan(context(simulator, entry))

    assert plan.commands
    assert plan.readiness_topics == entry["TOPICS_TO_LISTEN"]
    assert all(isinstance(command, list) for command in plan.commands)
    assert all("simulations/legacy" not in argument for command in plan.commands for argument in command)
    assert all("run_rviz:=true" not in command for command in plan.commands)


@pytest.mark.parametrize("simulator", ("gazebo_harmonic", "webots", "o3de"))
def test_world_and_multiple_backends_launch_world_and_robot_processes(simulator, tmp_path):
    entry = entry_for(simulator)
    plan = get_adapter(simulator, entry, tmp_path).build_launch_plan(context(simulator, entry))

    assert plan.commands[0][:3] == ["ros2", "launch", entry["backend"]["launch_package"]]
    assert plan.commands[1][:2] == ["bash", "-lc"]
    assert "scripts/multiple.sh" in plan.commands[1][2]
    assert "run_rviz:=false" in plan.commands[1][2]


@pytest.mark.parametrize("simulator", ("isaac_sim", "unity", "mujoco"))
def test_ros_launch_backends_build_one_direct_command(simulator, tmp_path):
    entry = entry_for(simulator)
    plan = get_adapter(simulator, entry, tmp_path).build_launch_plan(context(simulator, entry))

    assert len(plan.commands) == 1
    assert plan.commands[0][:4] == [
        "ros2", "launch", entry["backend"]["launch_package"], entry["backend"]["launch_file"],
    ]


def test_unity_and_mujoco_receive_backend_specific_arguments(tmp_path):
    unity_entry = entry_for("unity")
    unity = get_adapter("unity", unity_entry, tmp_path).build_launch_plan(
        context("unity", unity_entry, fps=60)
    )
    assert "render_fps:=60" in unity.commands[0]
    assert "robot_transport:=per_robot_transport" in unity.commands[0]

    mujoco_entry = entry_for("mujoco")
    mujoco = get_adapter("mujoco", mujoco_entry, tmp_path).build_launch_plan(
        context("mujoco", mujoco_entry, fps=60)
    )
    assert "render_fps:=60" in mujoco.commands[0]


def test_adapter_rejects_wrong_context(tmp_path):
    entry = entry_for("unity")
    with pytest.raises(AdapterConfigurationError):
        get_adapter("unity", entry, tmp_path).build_launch_plan(
            context("gazebo_harmonic", entry)
        )


def test_compact_isaac_and_unity_entries_preserve_backend_arguments(tmp_path):
    config = load_config()
    isaac_entry = config["isaac_sim"]["three_robot_simple_world_headless"]
    isaac_plan = get_adapter("isaac_sim", isaac_entry, tmp_path).build_launch_plan(
        context("isaac_sim", isaac_entry)
    )
    assert "world_file:=simple_world.usd" in isaac_plan.commands[0]
    assert "num_robots:=3" in isaac_plan.commands[0]
    assert "headless:=true" in isaac_plan.commands[0]
    assert "run_rviz:=false" in isaac_plan.commands[0]

    unity_entry = config["unity"]["two_robot_empty_world"]
    unity_plan = get_adapter("unity", unity_entry, tmp_path).build_launch_plan(
        context("unity", unity_entry, fps=30)
    )
    assert "world:=empty_world" in unity_plan.commands[0]
    assert "robot_count:=2" in unity_plan.commands[0]
    assert "headless:=false" in unity_plan.commands[0]
    assert "render_fps:=30" in unity_plan.commands[0]
    assert "robot_transport:=per_robot_transport" in unity_plan.commands[0]
