"""Loading, compact-matrix expansion, and validation for benchmark configuration."""

from __future__ import annotations

import argparse
import copy
import shutil
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from common.sensor_profile import camera_stream_fields, namespace, robot_name, topic


SIMULATORS = ("gazebo_harmonic", "webots", "isaac_sim", "unity", "o3de", "mujoco")
ROBOT_WORDS = {1: "one", 2: "two", 3: "three"}
CATEGORIES = tuple(
    f"{ROBOT_WORDS[robot_count]}_robot_{world}_world"
    f"{'_rviz' if use_rviz else ''}{'_headless' if headless else ''}"
    for headless in (False, True)
    for use_rviz in (False, True)
    for world in ("empty", "simple")
    for robot_count in (1, 2, 3)
)
REQUIRED_FIELDS = ("TOPICS_TO_LISTEN",)
DECLARATIVE_FIELDS = ("world", "robot_model", "robot_count", "headless", "use_rviz")
OPTIONAL_FIELDS = (*DECLARATIVE_FIELDS, "backend")
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPOSITORY_ROOT / "config" / "benchmark_config.yaml"


class ConfigurationError(ValueError):
    """Raised when benchmark configuration cannot be used safely."""


def _validate_string_list(value: Any, location: str) -> None:
    if not isinstance(value, list) or not value:
        raise ConfigurationError(f"{location} must be a non-empty list")
    if any(not isinstance(item, str) or not item for item in value):
        raise ConfigurationError(f"{location} must contain non-empty strings")


def _robot_count(category: str) -> int:
    return {word: count for count, word in ROBOT_WORDS.items()}[category.split("_", 1)[0]]


def _category_name(robot_count: int, world: str, headless: bool, use_rviz: bool) -> str:
    return (
        f"{ROBOT_WORDS[robot_count]}_robot_{world}_world"
        f"{'_rviz' if use_rviz else ''}{'_headless' if headless else ''}"
    )


def _canonical_readiness_topics(
    simulator: str,
    category: str,
    topic_overrides: Mapping[str, Mapping[str, str]] | None = None,
) -> list[str]:
    """Return enabled camera streams, optionally replacing backend-specific names."""
    overrides = topic_overrides or {}
    result = []
    for index in range(1, _robot_count(category) + 1):
        values = {
            "index": index,
            "robot_name": robot_name(simulator, index),
            "namespace": namespace(simulator, index),
        }
        for camera in ("camera_a", "camera_b"):
            for stream in camera_stream_fields(camera):
                template = overrides.get(camera, {}).get(stream)
                if template is None:
                    result.append(topic(simulator, index, camera, stream))
                else:
                    rendered = template.format(**values)
                    result.append(
                        rendered if rendered.startswith("/")
                        else f"{values['namespace']}/{rendered.lstrip('/')}"
                    )
    return result


def _validate_compact_topic_overrides(value: Any, location: str) -> dict[str, dict[str, str]]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ConfigurationError(f"{location} must map camera streams to topic templates")
    result: dict[str, dict[str, str]] = {}
    for camera, streams in value.items():
        if camera not in ("camera_a", "camera_b") or not isinstance(streams, Mapping):
            raise ConfigurationError(f"{location}.{camera} must be a camera stream mapping")
        allowed = set(camera_stream_fields(camera))
        unknown = sorted(set(streams) - allowed)
        if unknown:
            raise ConfigurationError(f"{location}.{camera} has unsupported streams: {unknown}")
        result[camera] = {}
        for stream, template in streams.items():
            if not isinstance(template, str) or not template:
                raise ConfigurationError(f"{location}.{camera}.{stream} must be a non-empty string")
            try:
                template.format(index=1, robot_name="robot", namespace="/robot")
            except (KeyError, ValueError) as exc:
                raise ConfigurationError(
                    f"{location}.{camera}.{stream} has an invalid template: {exc}"
                ) from exc
            result[camera][stream] = template
    return result


def _format_command(template: Any, values: Mapping[str, Any], location: str) -> list[str]:
    _validate_string_list(template, location)
    try:
        return [item.format(**values) for item in template]
    except (KeyError, ValueError) as exc:
        raise ConfigurationError(f"{location} has an invalid template: {exc}") from exc


def expand_compact_config(config: Any) -> dict[str, dict[str, dict[str, Any]]]:
    """Expand the compact benchmark matrix into its public normalized mapping."""
    if not isinstance(config, Mapping):
        raise ConfigurationError("Configuration root must be a mapping")
    if set(config) != {"benchmark", "simulators"}:
        raise ConfigurationError("Compact configuration root must contain benchmark and simulators")
    benchmark = config["benchmark"]
    simulators = config["simulators"]
    if not isinstance(benchmark, Mapping) or not isinstance(simulators, Mapping):
        raise ConfigurationError("benchmark and simulators must be mappings")

    allowed_benchmark = {"robot_counts", "worlds", "modes", "rviz", "robot_model"}
    unknown_benchmark = sorted(set(benchmark) - allowed_benchmark)
    if unknown_benchmark:
        raise ConfigurationError(f"benchmark has unknown fields: {unknown_benchmark}")
    robot_counts = benchmark.get("robot_counts")
    if robot_counts != [1, 2, 3]:
        raise ConfigurationError("benchmark.robot_counts must be [1, 2, 3]")
    robot_model = benchmark.get("robot_model", "rbwatcher")
    if not isinstance(robot_model, str) or not robot_model:
        raise ConfigurationError("benchmark.robot_model must be a non-empty string")

    worlds = benchmark.get("worlds")
    if not isinstance(worlds, Mapping) or set(worlds) != {"empty", "simple"}:
        raise ConfigurationError("benchmark.worlds must define exactly empty and simple")
    for world, per_simulator in worlds.items():
        if not isinstance(per_simulator, Mapping) or set(per_simulator) != set(SIMULATORS):
            raise ConfigurationError(f"benchmark.worlds.{world} must define every simulator")
        if any(not isinstance(value, str) or not value for value in per_simulator.values()):
            raise ConfigurationError(f"benchmark.worlds.{world} values must be non-empty strings")

    modes = benchmark.get("modes")
    if not isinstance(modes, Mapping) or set(modes) != {"gui", "headless"}:
        raise ConfigurationError("benchmark.modes must define exactly gui and headless")
    if modes["gui"] != {"headless": False} or modes["headless"] != {"headless": True}:
        raise ConfigurationError("benchmark.modes must map gui/headless to their headless boolean")
    rviz_options = benchmark.get("rviz")
    if rviz_options != [False, True]:
        raise ConfigurationError("benchmark.rviz must be [false, true]")

    missing_simulators = [name for name in SIMULATORS if name not in simulators]
    unknown_simulators = sorted(set(simulators) - set(SIMULATORS))
    if missing_simulators or unknown_simulators:
        raise ConfigurationError(
            f"Simulator mismatch: missing={missing_simulators}, unknown={unknown_simulators}"
        )

    normalized: dict[str, dict[str, dict[str, Any]]] = {}
    for simulator in SIMULATORS:
        simulator_config = simulators[simulator]
        location = f"simulators.{simulator}"
        if not isinstance(simulator_config, Mapping):
            raise ConfigurationError(f"{location} must be a mapping")
        allowed = {"robot_model", "backend", "topic_overrides"}
        unknown = sorted(set(simulator_config) - allowed)
        if unknown:
            raise ConfigurationError(f"{location} has unknown fields: {unknown}")
        backend = simulator_config.get("backend")
        if not isinstance(backend, Mapping):
            raise ConfigurationError(f"{location}.backend must be a mapping")
        strategy = backend.get("strategy", "launch")
        if strategy not in {"launch", "world_and_multiple"}:
            raise ConfigurationError(
                f"{location}.backend.strategy must be launch or world_and_multiple"
            )
        if not isinstance(backend.get("launch_package"), str) or not backend["launch_package"]:
            raise ConfigurationError(f"{location}.backend.launch_package must be a non-empty string")
        if strategy == "launch" and (
            not isinstance(backend.get("launch_file"), str) or not backend["launch_file"]
        ):
            raise ConfigurationError(f"{location}.backend.launch_file must be a non-empty string")
        if strategy == "world_and_multiple":
            for field in ("world_launch", "multiple_script"):
                if not isinstance(backend.get(field), str) or not backend[field]:
                    raise ConfigurationError(f"{location}.backend.{field} must be a non-empty string")
        if backend is not None and not isinstance(backend, Mapping):
            raise ConfigurationError(f"{location}.backend must be a mapping")
        overrides = _validate_compact_topic_overrides(
            simulator_config.get("topic_overrides"), f"{location}.topic_overrides"
        )
        model = simulator_config.get("robot_model", robot_model)
        if not isinstance(model, str) or not model:
            raise ConfigurationError(f"{location}.robot_model must be a non-empty string")

        categories: dict[str, dict[str, Any]] = {}
        for mode in ("gui", "headless"):
            headless = modes[mode]["headless"]
            for use_rviz in rviz_options:
                for world in ("empty", "simple"):
                    for count in robot_counts:
                        category = _category_name(count, world, headless, use_rviz)
                        values = {
                            "world": worlds[world][simulator],
                            "robot_count": count,
                            "robot_model": model,
                            "headless": str(headless).lower(),
                            "use_rviz": str(use_rviz).lower(),
                            "gui": str(not headless).lower(),
                        }
                        entry: dict[str, Any] = {
                            "TOPICS_TO_LISTEN": _canonical_readiness_topics(
                                simulator, category, overrides
                            )
                        }
                        entry.update(
                            world=values["world"],
                            robot_model=model,
                            robot_count=count,
                            headless=headless,
                            use_rviz=use_rviz,
                            backend=copy.deepcopy(dict(backend)),
                        )
                        categories[category] = entry
        normalized[simulator] = categories
    return normalized


def _validate_normalized_config(
    config: Any,
    expected_topics: Mapping[tuple[str, str], Sequence[str]] | None = None,
) -> Mapping[str, Mapping[str, Mapping[str, Sequence[str]]]]:
    if not isinstance(config, Mapping):
        raise ConfigurationError("Configuration root must be a mapping")
    missing_simulators = [name for name in SIMULATORS if name not in config]
    unknown_simulators = sorted(set(config) - set(SIMULATORS))
    if missing_simulators or unknown_simulators:
        raise ConfigurationError(
            f"Simulator mismatch: missing={missing_simulators}, unknown={unknown_simulators}"
        )

    for simulator in SIMULATORS:
        simulator_config = config[simulator]
        if not isinstance(simulator_config, Mapping):
            raise ConfigurationError(f"{simulator} must map categories to settings")
        missing_categories = [name for name in CATEGORIES if name not in simulator_config]
        unknown_categories = sorted(set(simulator_config) - set(CATEGORIES))
        if missing_categories or unknown_categories:
            raise ConfigurationError(
                f"{simulator} category mismatch: missing={missing_categories}, "
                f"unknown={unknown_categories}"
            )
        for category in CATEGORIES:
            entry = simulator_config[category]
            location = f"{simulator}.{category}"
            if not isinstance(entry, Mapping):
                raise ConfigurationError(f"{location} must be a mapping")
            obsolete = set(entry) & {"NODES_TO_KILL"}
            if obsolete:
                raise ConfigurationError(f"{location} contains obsolete fields: {sorted(obsolete)}")
            missing_fields = [field for field in REQUIRED_FIELDS if field not in entry]
            has_declarative = all(field in entry for field in DECLARATIVE_FIELDS)
            if not has_declarative:
                missing_fields.append("declarative simulator fields")
            unknown_fields = sorted(set(entry) - set(REQUIRED_FIELDS) - set(OPTIONAL_FIELDS))
            if missing_fields or unknown_fields:
                raise ConfigurationError(
                    f"{location} field mismatch: missing={missing_fields}, unknown={unknown_fields}"
                )
            for field in REQUIRED_FIELDS:
                _validate_string_list(entry[field], f"{location}.{field}")
            if has_declarative:
                if not isinstance(entry["world"], str) or not entry["world"]:
                    raise ConfigurationError(f"{location}.world must be a non-empty string")
                if not isinstance(entry["robot_model"], str) or not entry["robot_model"]:
                    raise ConfigurationError(f"{location}.robot_model must be a non-empty string")
                if not isinstance(entry["robot_count"], int) or entry["robot_count"] not in ROBOT_WORDS:
                    raise ConfigurationError(f"{location}.robot_count must be 1, 2, or 3")
                if not isinstance(entry["headless"], bool) or not isinstance(entry["use_rviz"], bool):
                    raise ConfigurationError(f"{location}.headless and use_rviz must be booleans")
                if not isinstance(entry.get("backend", {}), Mapping):
                    raise ConfigurationError(f"{location}.backend must be a mapping")
            expected = list((expected_topics or {}).get(
                (simulator, category), _canonical_readiness_topics(simulator, category)
            ))
            if list(entry["TOPICS_TO_LISTEN"]) != expected:
                raise ConfigurationError(
                    f"{location}.TOPICS_TO_LISTEN must match the enabled canonical camera streams: {expected}"
                )
    return config


def validate_config(config: Any) -> Mapping[str, Mapping[str, Mapping[str, Sequence[str]]]]:
    """Validate legacy config or expand and validate compact matrix config."""
    if isinstance(config, Mapping) and ("benchmark" in config or "simulators" in config):
        normalized = expand_compact_config(config)
        # Expansion itself derives topics from the canonical profile (and any
        # declared per-simulator override); this final pass verifies its public shape.
        return _validate_normalized_config(normalized, {
            (simulator, category): entry["TOPICS_TO_LISTEN"]
            for simulator, categories in normalized.items()
            for category, entry in categories.items()
        })
    return _validate_normalized_config(config)


def load_config(path: Path | str = DEFAULT_CONFIG_PATH):
    """Load YAML and return the fully validated, normalized configuration mapping."""
    config_path = Path(path).expanduser().resolve()
    try:
        with config_path.open(encoding="utf-8") as stream:
            config = yaml.safe_load(stream)
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigurationError(f"Could not load {config_path}: {exc}") from exc
    return validate_config(config)


def resolve_category(value: str | int) -> str:
    """Resolve the historical one-based category number or an exact name."""
    text = str(value)
    if text in CATEGORIES:
        return text
    try:
        index = int(text)
    except ValueError as exc:
        raise ConfigurationError(f"Unknown category: {value}") from exc
    if not 1 <= index <= len(CATEGORIES):
        raise ConfigurationError(f"Category index must be between 1 and {len(CATEGORIES)}")
    return CATEGORIES[index - 1]


def resolve_command(command: Sequence[str]) -> list[str]:
    """Resolve and validate a configured executable before launching anything."""
    resolved = list(command)
    executable = resolved[0]
    if executable.startswith("./"):
        path = (REPOSITORY_ROOT / executable[2:]).resolve()
        if not path.is_file():
            raise ConfigurationError(f"Configured executable does not exist: {path}")
        if not path.stat().st_mode & 0o111:
            raise ConfigurationError(f"Configured executable is not executable: {path}")
        resolved[0] = str(path)
    elif "/" in executable:
        path = Path(executable).expanduser().resolve()
        if not path.is_file():
            raise ConfigurationError(f"Configured executable does not exist: {path}")
        resolved[0] = str(path)
    elif shutil.which(executable) is None:
        raise ConfigurationError(f"Configured executable is not on PATH: {executable}")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate benchmark configuration")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--category-count", action="store_true")
    parser.add_argument("--list-categories", action="store_true")
    parser.add_argument("--category-names", action="store_true", help="Print category names only, one per line")
    parser.add_argument("--gui", action="store_true", help="With --category-names, select GUI categories")
    parser.add_argument("--headless", action="store_true", help="With --category-names, select headless categories")
    parser.add_argument("--rviz", action="store_true", help="With --category-names, select categories that use RViz")
    args = parser.parse_args()
    load_config(args.config)
    if args.category_count:
        print(len(CATEGORIES))
    elif args.list_categories:
        for index, category in enumerate(CATEGORIES, start=1):
            print(f"{index}: {category}")
    elif args.category_names:
        if args.gui and args.headless:
            parser.error("--gui and --headless cannot be used together")
        categories = CATEGORIES
        if args.gui:
            categories = tuple(category for category in categories if "headless" not in category)
        elif args.headless:
            categories = tuple(category for category in categories if "headless" in category)
        if args.rviz:
            categories = tuple(category for category in categories if "rviz" in category)
        print("\n".join(categories))
    else:
        print(f"Configuration valid: {len(SIMULATORS)} simulators, {len(CATEGORIES)} categories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
