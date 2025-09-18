#!/usr/bin/env python3
# utils/load_usd_and_run.py
#
# Unpacks a Unity simulation archive into its own subfolder under ../worlds,
# ensures executable permissions, and runs the simulation.
#
# Usage:
#   python3 load_usd_and_run.py unity_simulation_only.tar.gz
#   python3 load_usd_and_run.py unity_simulation.tar.gz
#
# If no argument is given, it falls back to ARCHIVE_NAME.

import sys
import subprocess
from pathlib import Path
from typing import Optional

BINARY_NAME  = "PI_simulation_Unity_Robotnik.x86_64"
ARCHIVE_NAME = "unity_simulation_only.tar.gz"

def archive_to_world_id(archive_name: str) -> str:
    """Derive a stable folder name from the archive file name."""
    name = Path(archive_name).name
    # Handle common compressed tar suffixes
    for suffix in (".tar.gz", ".tgz", ".tar.bz2", ".tar.xz", ".tar.zst"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    # Fallback to stem if it's something unusual
    return Path(name).stem

def find_binary(root_dir: Path, binary_name: str) -> Optional[Path]:
    """Search for the binary inside root_dir only (not the whole worlds dir)."""
    direct = root_dir / binary_name
    if direct.exists() and direct.is_file():
        return direct
    for p in root_dir.rglob(binary_name):
        if p.is_file():
            return p
    return None

def ensure_extracted(worlds_dir: Path, archive_name: str, binary_name: str) -> Path:
    """
    Make sure the requested world is extracted into worlds/<world_id>/ and
    return the path to the binary inside that folder.
    """
    archive_path = worlds_dir / archive_name
    if not archive_path.exists():
        print(f"[ERROR] Archive not found: {archive_path}")
        print("        Place the Unity simulation tar.gz in the 'worlds' folder with this exact name.")
        sys.exit(1)

    world_id = archive_to_world_id(archive_name)
    world_root = worlds_dir / world_id
    world_root.mkdir(parents=True, exist_ok=True)

    # If the binary already exists inside this world's root, reuse it
    sim_binary = find_binary(world_root, binary_name)
    if sim_binary:
        return sim_binary

    # Otherwise (first time), extract into the world's dedicated folder
    print(f"[INFO] Extracting '{archive_path.name}' into '{world_root}'")
    try:
        # Note: we don't --strip-components here; structure varies between archives.
        subprocess.check_call(["tar", "-xvzf", str(archive_path), "-C", str(world_root)])
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Extraction failed: {e}")
        sys.exit(1)

    sim_binary = find_binary(world_root, binary_name)
    if not sim_binary:
        print("[ERROR] Extraction completed but the expected binary was not found.")
        print(f"        Looked for '{binary_name}' under: {world_root}")
        sys.exit(1)

    return sim_binary

def main(archive_name: str, binary_name: str = BINARY_NAME):
    # Base path is the folder of this script
    script_dir = Path(__file__).resolve().parent
    worlds_dir = script_dir.parent / "worlds"
    worlds_dir.mkdir(parents=True, exist_ok=True)

    # Ensure extracted world and get its binary
    sim_binary = ensure_extracted(worlds_dir, archive_name, binary_name)

    # Ensure executable permission (best-effort)
    try:
        sim_binary.chmod(0o755)
    except Exception as e:
        print(f"[WARN] Could not change executable permissions: {e}")

    # Run the simulation with its folder as CWD (keeps relative assets consistent)
    print(f"[INFO] Starting Unity simulation: {sim_binary}")
    try:
        subprocess.run([str(sim_binary)], cwd=sim_binary.parent, check=False)
    except Exception as e:
        print(f"[ERROR] Failed to start simulation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Read the archive name from the first command-line argument (optional).
    if len(sys.argv) >= 2 and sys.argv[1].strip():
        archive_to_load = sys.argv[1]
    else:
        archive_to_load = ARCHIVE_NAME
        print(f"[INFO] No archive name provided. Using default: {archive_to_load}")

    main(archive_name=archive_to_load)
