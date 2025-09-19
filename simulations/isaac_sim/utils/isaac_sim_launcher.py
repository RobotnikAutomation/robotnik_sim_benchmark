import os
import omni.kit.app
from omni.usd import get_context
import omni.timeline
from pathlib import Path
from pxr import UsdGeom, Gf
import omni.isaac.core.utils.prims as prim_utils

# -------------------------------
# Leer variables de entorno
# -------------------------------
num_robots = int(os.environ.get('NUM_ROBOTS', 0))
world_file = os.environ.get('WORLD_FILE', 'empty_world.usd')  # nombre del USD del mundo

# -------------------------------
# Inicializar app
# -------------------------------
app = omni.kit.app.get_app()

# Abrir mundo
script_path = Path(__file__).resolve()
usd_path = script_path.parent.parent / "worlds" / world_file
get_context().open_stage(str(usd_path))

# Timeline
timeline = omni.timeline.get_timeline_interface()
timeline.play()

# Spawn de robots
model_path = script_path.parent.parent / "models/rbwatcher.usd"
stage = get_context().get_stage()

if num_robots > 0:
    print(f"Spawneando {num_robots} robot(s)...")
    for i in range(num_robots):
        robot_name = f"rbwatcher_{i+1}"
        position = Gf.Vec3d(0.0, i * 1.0, 0.2)

        # Crear prim contenedor
        prim_path = f"/World/{robot_name}"
        prim_utils.create_prim(prim_path, "Xform")

        # Referenciar el USD del robot
        robot_prim_path = f"{prim_path}/rbwatcher"
        if not stage.GetPrimAtPath(robot_prim_path):
            robot_prim = stage.DefinePrim(robot_prim_path, "Xform")
            robot_prim.GetReferences().AddReference(str(model_path))

        # Aplicar posición usando XformOps
        xform = UsdGeom.Xformable(stage.GetPrimAtPath(prim_path))
        xform.ClearXformOpOrder()  # Limpiar ops existentes para evitar errores
        translate_op = xform.AddTranslateOp()
        translate_op.Set(position)
else:
    print("No se spawnearon robots")

print(f"Simulación iniciada con {usd_path}. Presiona Ctrl+C para salir.")

# Loop de actualización
while app.is_running():
    app.update()