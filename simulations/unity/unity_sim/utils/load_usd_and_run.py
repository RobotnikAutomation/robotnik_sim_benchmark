#!/usr/bin/env python3
# utils/load_usd_and_run.py
#
# Unpacks a pre-bundled Unity simulation archive from ../worlds (relative to this script),
# ensures executable permissions, and runs the simulation.

import sys
import subprocess
from pathlib import Path

# Configuration
ARCHIVE_NAME = "unity_simulation.tar.gz"
BINARY_NAME  = "PI_simulation_Unity_Robotnik.x86_64"

def find_binary(worlds_dir: Path, binary_name: str) -> Path | None:
    """Search for the binary in worlds_dir (top-level) and recursively if needed."""
    candidate = worlds_dir / binary_name
    if candidate.exists():
        return candidate

    for p in worlds_dir.rglob(binary_name):
        if p.is_file():
            return p

    return None

def ensure_extracted(worlds_dir: Path, archive_name: str, binary_name: str) -> Path:
    """If the binary isn't present, extract the tarball. Return the located binary path."""
    sim_binary = find_binary(worlds_dir, binary_name)
    if sim_binary:
        # Already extracted
        return sim_binary

    tar_path = worlds_dir / archive_name
    if not tar_path.exists():
        print(f"[ERROR] Archive not found: {tar_path}")
        print("        Place the Unity simulation tar.gz in the 'worlds' folder with this exact name.")
        sys.exit(1)

    print(f"[INFO] Extracting archive: {tar_path}")
    try:
        subprocess.check_call(["tar", "-xvzf", str(tar_path), "-C", str(worlds_dir)])
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Extraction failed: {e}")
        sys.exit(1)

    sim_binary = find_binary(worlds_dir, binary_name)
    if not sim_binary:
        print("[ERROR] Extraction completed but the expected binary was not found.")
        print(f"        Looked for '{binary_name}' somewhere inside: {worlds_dir}")
        sys.exit(1)

    return sim_binary

def main():
    # Base path is the folder of this script
    script_dir = Path(__file__).resolve().parent
    worlds_dir = script_dir.parent / "worlds"
    worlds_dir.mkdir(parents=True, exist_ok=True)

    # Ensure we have an extracted simulation and get the binary path
    sim_binary = ensure_extracted(worlds_dir, ARCHIVE_NAME, BINARY_NAME)

    # Ensure executable permission
    try:
        sim_binary.chmod(0o755)
    except Exception as e:
        print(f"[WARN] Could not change executable permissions: {e}")

    # Run the simulation
    print(f"[INFO] Starting Unity simulation: {sim_binary}")
    try:
        # Use cwd=sim_binary.parent to keep relative paths consistent for the app
        subprocess.run([str(sim_binary)], cwd=sim_binary.parent, check=False)
    except Exception as e:
        print(f"[ERROR] Failed to start simulation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
