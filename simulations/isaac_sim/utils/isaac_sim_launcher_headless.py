from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": True, "sync_loads": True})

import os
from pathlib import Path

import omni
import omni.timeline
from omni.usd import get_context
from pxr import UsdGeom, Gf

from isaacsim.core.utils.extensions import enable_extension
import isaacsim.core.utils.prims as prim_utils
from isaacsim.core.utils.stage import is_stage_loading


# -------------------------------
# Leer variables de entorno
# -------------------------------
num_robots = int(os.environ.get("NUM_ROBOTS", 1))
world_file = os.environ.get("WORLD_FILE", "empty_world.usd")

# -------------------------------
# EXT: habilitar ROS2 Bridge
# -------------------------------
enable_extension("isaacsim.ros2.bridge")
enable_extension("omni.graph.action")  # solo si de verdad lo necesitas

# 🔥 workaround anti-segfault: steppea un par de frames tras habilitar ROS2
simulation_app.update()
simulation_app.update()

# -------------------------------
# Abrir mundo
# -------------------------------
script_path = Path(__file__).resolve()
usd_path = script_path.parent.parent / "worlds" / world_file
get_context().open_stage(str(usd_path))

# Dale 2 frames para empezar a cargar
simulation_app.update()
simulation_app.update()

# Esperar carga completa (importante en headless)
while is_stage_loading():
    simulation_app.update()

stage = get_context().get_stage()

# -------------------------------
# Spawn de robots
# -------------------------------
model_path = script_path.parent.parent / "models/rbwatcher.usd"

if num_robots > 0:
    print(f"Spawneando {num_robots} robot(s)...")
    for i in range(num_robots):
        robot_name = f"rbwatcher_{i+1}"
        position = Gf.Vec3d(0.0, i * 1.0, 0.2)

        prim_path = f"/World/{robot_name}"
        prim_utils.create_prim(prim_path, "Xform")

        robot_prim_path = f"{prim_path}/rbwatcher"
        if not stage.GetPrimAtPath(robot_prim_path):
            robot_prim = stage.DefinePrim(robot_prim_path, "Xform")
            robot_prim.GetReferences().AddReference(str(model_path))

        xform = UsdGeom.Xformable(stage.GetPrimAtPath(prim_path))
        xform.ClearXformOpOrder()
        xform.AddTranslateOp().Set(position)
else:
    print("No se spawnearon robots")

# -------------------------------
# Timeline: play SOLO cuando todo está cargado
# -------------------------------
timeline = omni.timeline.get_timeline_interface()
timeline.play()

print(f"Simulación iniciada con {usd_path}. Ctrl+C para salir.")

try:
    while simulation_app.is_running():
        simulation_app.update()
except KeyboardInterrupt:
    pass
finally:
    timeline.stop()
    simulation_app.close()
