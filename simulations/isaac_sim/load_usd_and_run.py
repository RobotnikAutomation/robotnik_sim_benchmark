import omni.kit.app
from omni.usd import get_context
import omni.timeline

# Obtener la app
app = omni.kit.app.get_app()

# Ruta a tu archivo USD
usd_path = "/home/robotnik/rvasquez/RB-WATCHER/rbwatcher_demo2.usd"

# Abrir el stage
get_context().open_stage(usd_path)

# Obtener timeline y arrancar simulación
timeline = omni.timeline.get_timeline_interface()
timeline.play()  # activa la simulación

print("Simulación iniciada. Presiona Ctrl+C para salir.")

# Mantener la simulación corriendo
while app.is_running():
    app.update()
