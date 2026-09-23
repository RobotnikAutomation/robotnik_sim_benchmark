"""Common data types and lifecycle boundary for simulator adapters."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class SimulatorLaunchContext:
    """Common simulator inputs required to build a benchmark launch plan."""

    simulator: str
    world: str
    robot_count: int
    robot_model: str
    headless: bool
    use_rviz: bool
    render_fps: int | None
    ros_args: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class LaunchPlan:
    """Commands and environment prepared for the process supervisor."""

    commands: list[list[str]]
    environment: dict[str, str] = field(default_factory=dict)
    readiness_topics: list[str] = field(default_factory=list)


class SimulatorAdapter(ABC):
    """Build commands without launching or supervising simulator processes."""

    def __init__(self, entry: Mapping[str, Any], repository_root):
        self.entry = entry
        self.repository_root = repository_root

    @abstractmethod
    def build_launch_plan(self, context: SimulatorLaunchContext) -> LaunchPlan:
        """Return the complete process plan for one benchmark iteration."""

    @abstractmethod
    def validate_context(self, context: SimulatorLaunchContext) -> None:
        """Reject unsupported worlds, models, or launch combinations."""
