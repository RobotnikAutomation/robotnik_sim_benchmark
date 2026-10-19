"""Direct, declarative command builders for every benchmark simulator."""
from __future__ import annotations

import shlex
from pathlib import Path
from typing import Any, Mapping

from .interface import LaunchPlan, SimulatorAdapter, SimulatorLaunchContext


class AdapterConfigurationError(ValueError):
    """Raised when a simulator backend cannot represent the requested context."""


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _arguments(value: Any, location: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise AdapterConfigurationError(f"{location} must be a list of strings")
    return list(value)


class DeclarativeAdapter(SimulatorAdapter):
    """Build a process plan using a backend declared in benchmark_config.yaml."""

    simulator_name = ""

    def validate_context(self, context: SimulatorLaunchContext) -> None:
        if context.simulator != self.simulator_name:
            raise AdapterConfigurationError(
                f"Adapter {self.simulator_name} cannot handle {context.simulator}"
            )
        if context.robot_count not in (1, 2, 3):
            raise AdapterConfigurationError("robot_count must be one, two, or three")
        if not context.robot_model:
            raise AdapterConfigurationError("robot_model must not be empty")

    def _backend(self) -> Mapping[str, Any]:
        backend = self.entry.get("backend")
        if not isinstance(backend, Mapping):
            raise AdapterConfigurationError(
                f"{self.simulator_name} requires a declarative backend"
            )
        return backend

    @staticmethod
    def _render(arguments: list[str], values: Mapping[str, Any]) -> list[str]:
        try:
            return [argument.format(**values) for argument in arguments]
        except (KeyError, ValueError) as exc:
            raise AdapterConfigurationError(
                f"backend launch argument has an invalid template: {exc}"
            ) from exc

    def build_launch_plan(self, context: SimulatorLaunchContext) -> LaunchPlan:
        self.validate_context(context)
        backend = self._backend()
        strategy = backend.get("strategy", "launch")
        package = backend.get("launch_package")
        if not isinstance(package, str) or not package:
            raise AdapterConfigurationError("backend.launch_package must be a non-empty string")

        values = {
            "world": context.world,
            "robot_count": context.robot_count,
            "robot_model": context.robot_model,
            "headless": _bool(context.headless),
            "gui": _bool(not context.headless),
            # RViz belongs to the benchmark process and is never embedded in a backend.
            "use_rviz": "false",
            "render_fps": context.render_fps if context.render_fps is not None else 0,
        }

        if strategy == "launch":
            launch_file = backend.get("launch_file")
            if not isinstance(launch_file, str) or not launch_file:
                raise AdapterConfigurationError("backend.launch_file must be a non-empty string")
            arguments = self._render(
                _arguments(backend.get("launch_arguments", []), "backend.launch_arguments"),
                values,
            )
            commands = [[
                "ros2", "launch", package, launch_file, *arguments, *context.ros_args,
            ]]
        elif strategy == "world_and_multiple":
            world_launch = backend.get("world_launch")
            script = backend.get("multiple_script")
            if not isinstance(world_launch, str) or not world_launch:
                raise AdapterConfigurationError("backend.world_launch must be a non-empty string")
            if not isinstance(script, str) or not script or script.startswith("/"):
                raise AdapterConfigurationError(
                    "backend.multiple_script must be a relative installed-package path"
                )
            world_arguments = self._render(
                _arguments(backend.get("world_arguments", []), "backend.world_arguments"),
                values,
            )
            multiple_arguments = self._render(
                _arguments(backend.get("multiple_arguments", []), "backend.multiple_arguments"),
                values,
            )
            installed_script = (
                f'$(ros2 pkg prefix {shlex.quote(package)})/share/'
                f'{shlex.quote(package)}/{shlex.quote(script)}'
            )
            multiple_command = f'exec "{installed_script}" {shlex.join(multiple_arguments)}'
            commands = [
                ["ros2", "launch", package, world_launch, *world_arguments, *context.ros_args],
                ["bash", "-lc", multiple_command],
            ]
        else:
            raise AdapterConfigurationError(
                f"Unsupported backend.strategy for {self.simulator_name}: {strategy!r}"
            )

        environment = backend.get("environment", {})
        if not isinstance(environment, Mapping):
            raise AdapterConfigurationError("backend.environment must be a mapping")
        return LaunchPlan(
            commands=commands,
            environment={str(key): str(value) for key, value in environment.items()},
            readiness_topics=list(self.entry.get("TOPICS_TO_LISTEN", [])),
        )


class GazeboAdapter(DeclarativeAdapter):
    simulator_name = "gazebo_harmonic"


class WebotsAdapter(DeclarativeAdapter):
    simulator_name = "webots"


class IsaacSimAdapter(DeclarativeAdapter):
    simulator_name = "isaac_sim"


class UnityAdapter(DeclarativeAdapter):
    simulator_name = "unity"


class O3DEAdapter(DeclarativeAdapter):
    simulator_name = "o3de"


class MuJoCoAdapter(DeclarativeAdapter):
    simulator_name = "mujoco"


ADAPTERS = {
    "gazebo_harmonic": GazeboAdapter,
    "webots": WebotsAdapter,
    "isaac_sim": IsaacSimAdapter,
    "unity": UnityAdapter,
    "o3de": O3DEAdapter,
    "mujoco": MuJoCoAdapter,
}


def get_adapter(simulator: str, entry: Mapping[str, Any], repository_root: Path) -> SimulatorAdapter:
    """Create the registered adapter for a configured simulator."""
    try:
        adapter_type = ADAPTERS[simulator]
    except KeyError as exc:
        raise AdapterConfigurationError(f"Unsupported simulator: {simulator}") from exc
    return adapter_type(entry, repository_root)
