import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
import yaml

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from validate.validate_config import (  # noqa: E402
    CATEGORIES,
    DEFAULT_CONFIG_PATH,
    SIMULATORS,
    ConfigurationError,
    expand_compact_config,
    load_config,
    resolve_category,
    resolve_command,
    validate_config,
)


def test_repository_configuration_is_complete():
    config = load_config()
    assert set(config) == set(SIMULATORS)
    assert all(tuple(config[name]) == CATEGORIES for name in SIMULATORS)


def test_compact_matrix_expands_all_public_categories():
    raw_config = yaml.safe_load(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
    config = expand_compact_config(raw_config)

    assert set(config) == set(SIMULATORS)
    assert all(tuple(config[simulator]) == CATEGORIES for simulator in SIMULATORS)
    assert all(len(config[simulator]) == 24 for simulator in SIMULATORS)
    for robot in ("one", "two", "three"):
        for world in ("empty", "simple"):
            for suffix in ("", "_rviz", "_headless", "_rviz_headless"):
                assert f"{robot}_robot_{world}_world{suffix}" in CATEGORIES


def test_compact_topic_overrides_replace_only_the_selected_stream():
    raw_config = yaml.safe_load(DEFAULT_CONFIG_PATH.read_text(encoding="utf-8"))
    raw_config = deepcopy(raw_config)
    raw_config["simulators"]["unity"]["topic_overrides"] = {
        "camera_a": {"color_topic": "custom/{robot_name}/image"}
    }

    config = validate_config(raw_config)
    topics = config["unity"]["two_robot_empty_world"]["TOPICS_TO_LISTEN"]
    assert topics[0] == "/robot/custom/robot/image"
    assert topics[3] == "/robot_2/custom/robot_2/image"
    assert "/robot/top_rgbd_camera/color/image_raw" in topics


def test_normalized_configuration_is_declarative_only():
    config = load_config()
    assert validate_config(config) is config
    for simulator in SIMULATORS:
        for entry in config[simulator].values():
            assert "LAUNCH_SIMULATOR_CMD" not in entry
            assert "LAUNCH_ROBOT_CMD" not in entry
            assert "backend" in entry


def test_categories_resolve_by_index_and_name():
    for index, category in enumerate(CATEGORIES, start=1):
        assert resolve_category(index) == category
        assert resolve_category(category) == category
    for invalid in (0, len(CATEGORIES) + 1, "missing"):
        with pytest.raises(ConfigurationError):
            resolve_category(invalid)


def test_required_fields_and_obsolete_fields_are_validated():
    config = load_config()
    entry = config[SIMULATORS[0]][CATEGORIES[0]]
    del entry["TOPICS_TO_LISTEN"]
    with pytest.raises(ConfigurationError, match="TOPICS_TO_LISTEN"):
        validate_config(config)

    config = load_config()
    config[SIMULATORS[0]][CATEGORIES[0]]["NODES_TO_KILL"] = ["obsolete"]
    with pytest.raises(ConfigurationError, match="obsolete"):
        validate_config(config)


def test_commands_are_resolved_before_launch():
    assert resolve_command(["python3"])[0] == "python3"
    with pytest.raises(ConfigurationError, match="not on PATH"):
        resolve_command(["definitely-not-a-real-benchmark-command"])


@pytest.mark.parametrize(
    ("filters", "expected"),
    [
        (("--gui",), 12),
        (("--headless",), 12),
        (("--gui", "--rviz"), 6),
    ],
)
def test_campaign_category_filters(filters, expected):
    runner = Path(__file__).resolve().parents[1] / "execute/run_simulator_campaign.sh"
    result = subprocess.run(
        [str(runner), "--simulator", "gazebo_harmonic", "--list-only", *filters],
        check=True,
        capture_output=True,
        text=True,
    )
    assert len(result.stdout.splitlines()) == expected


def test_campaign_rejects_gui_and_headless_together():
    runner = Path(__file__).resolve().parents[1] / "execute/run_simulator_campaign.sh"
    result = subprocess.run(
        [str(runner), "--list-only", "--gui", "--headless"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
