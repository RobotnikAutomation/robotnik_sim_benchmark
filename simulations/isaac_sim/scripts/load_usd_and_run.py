import omni.kit.app
from omni.usd import get_context
import omni.timeline
from pathlib import Path

# Obtener la app
app = omni.kit.app.get_app()

# Ruta al script actual
script_path = Path(__file__).resolve()

# Subir un nivel (a repo/) y apuntar a isaac.usd
usd_path = script_path.parent.parent / "worlds/rbwatcher_sim.usd"

# Abrir el stage
get_context().open_stage(str(usd_path))

# Obtener timeline y arrancar simulación
timeline = omni.timeline.get_timeline_interface()
timeline.play()  # activa la simulación

print(f"Simulación iniciada con {usd_path}. Presiona Ctrl+C para salir.")

# Mantener la simulación corriendo
while app.is_running():
    app.update()


# import omni.kit.app
# from omni.usd import get_context
# import omni.timeline

# # Obtener la app
# app = omni.kit.app.get_app()

# # Ruta a tu archivo USD
# usd_path = "/home/robotnik/rvasquez/RB-WATCHER/rbwatcher_demo2.usd"

# # Abrir el stage
# get_context().open_stage(usd_path)

# # Obtener timeline y arrancar simulación
# timeline = omni.timeline.get_timeline_interface()
# timeline.play()  # activa la simulación

# print("Simulación iniciada. Presiona Ctrl+C para salir.")

# # Mantener la simulación corriendo
# while app.is_running():
#     app.update()
