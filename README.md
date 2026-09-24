# Robotnik simulation benchmark

Repositorio principal para ejecutar y comparar los benchmarks de Gazebo
Harmonic, Webots, Isaac Sim, MuJoCo, O3DE y Unity. Cada simulador conserva su
workspace independiente y sus dependencias están fijadas como submódulos Git.

## 1. Requisitos

El flujo está validado para Ubuntu con ROS 2 Jazzy. Instala como mínimo:

```bash
sudo apt update
sudo apt install git git-lfs build-essential cmake ninja-build python3-pip
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions
git lfs install
```

Cada simulador puede tener requisitos adicionales. Isaac Sim requiere su
instalación y entorno de ejecución propios; MuJoCo requiere sus dependencias y
licencia/configuración cuando corresponda; O3DE requiere una instalación de
O3DE compatible; Unity requiere un host Linux compatible con los Players
incluidos.

## 2. Clonado y preparación

Clona la rama reproducible e inicializa todos los submódulos:

```bash
git clone -b benchmarking-compatibility \
  https://github.com/RobotnikAutomation/robotnik_sim_benchmark.git
cd robotnik_sim_benchmark
./scripts/setup_workspace.sh
```

Para descargar también los assets administrados por Git LFS:

```bash
./scripts/setup_workspace.sh --pull-lfs
```

La estructura resultante es:

```text
robotnik_sim_benchmark/
├── benchmarks/                         # Resultados locales, no versionados
├── config/                             # Matriz y perfil común de sensores
├── scripts/                            # Preparación, compilación y ejecución
├── robotnik_benchmark_gazebo_ws/src/robotnik/
├── robotnik_benchmark_webots_ws/src/
├── robotnik_benchmark_isaac_ws/src/
├── robotnik_benchmark_mujoco_ws/src/
├── robotnik_benchmark_o3de_ws/src/
└── robotnik_benchmark_unity_ws/src/
```

La procedencia y el commit exacto de cada submódulo están en
[`docs/repositories.md`](docs/repositories.md). Los commits están fijados para
que dos clones produzcan el mismo entorno; la rama indicada allí sólo describe
el origen utilizado para seleccionar cada commit.

## 3. Compilar los workspaces

El script de compilación mantiene un workspace aislado por simulador:

```bash
./scripts/build_workspace.sh gazebo_harmonic
./scripts/build_workspace.sh webots
./scripts/build_workspace.sh isaac_sim
./scripts/build_workspace.sh mujoco
./scripts/build_workspace.sh o3de
./scripts/build_workspace.sh unity
```

Para compilar todos:

```bash
./scripts/build_workspace.sh all
```

Cada ejecución carga únicamente `/opt/ros/${ROS_DISTRO:-jazzy}/setup.bash` y
construye con `colcon build --symlink-install` dentro de su propio workspace.
No se deben reutilizar los directorios `build`, `install` o `log` entre
simuladores.

## 4. O3DE: generar el proyecto localmente

El proyecto O3DE no almacena en Git los binarios ni los directorios generados.
Se genera en la máquina de cada usuario a partir de `robotnik_o3de` y
`o3de-extras`.

Define las rutas:

```bash
export O3DE_HOME=/opt/O3DE/26.05
export O3DE_EXTRAS_HOME=$PWD/robotnik_benchmark_o3de_ws/src/o3de-extras
export PROJECT_PATH=$PWD/robotnik_benchmark_o3de_ws/src/robotnik_o3de/project/robotnik_roscon25
```

Descarga los assets y registra gems/templates:

```bash
git -C "$O3DE_EXTRAS_HOME" lfs pull

$O3DE_HOME/scripts/o3de.sh register \
  --all-gems-path "$O3DE_EXTRAS_HOME/Gems"
$O3DE_HOME/scripts/o3de.sh register \
  --all-templates-path "$O3DE_EXTRAS_HOME/Templates"
```

Genera y compila el proyecto:

```bash
cd "$PROJECT_PATH"
cmake -B build/linux \
  -G "Ninja Multi-Config" \
  -DLY_DISABLE_TEST_MODULES=ON \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DLY_STRIP_DEBUG_SYMBOLS=ON

cmake --build build/linux \
  --config profile \
  --target robotnik_roscon25 Editor \
  robotnik_roscon25.Assets robotnik_roscon25.GameLauncher
```

El wrapper ROS 2 se compila con:

```bash
./scripts/build_workspace.sh o3de
source robotnik_benchmark_o3de_ws/install/setup.bash
ros2 launch robotnik_o3de spawn_world.launch.py
```

También puede ejecutarse directamente el launcher generado desde
`build/linux/bin/profile`. Los directorios generados por CMake y O3DE no deben
añadirse al repositorio.

## 5. Unity: compilar el wrapper y usar los Players

El submódulo `robotnik_unity` contiene los Players de Unity distribuidos como
archivos comprimidos y el paquete ROS 2 `unity_sim`. El proyecto fuente
completo del Unity Editor no está actualmente publicado, por lo que no se
regenera el Player desde este repositorio.

Descarga y valida los archivos LFS:

```bash
git -C robotnik_benchmark_unity_ws/src/robotnik_unity lfs pull
python3 robotnik_benchmark_unity_ws/src/robotnik_unity/utils/verify_unity_archives.py \
  robotnik_benchmark_unity_ws/src/robotnik_unity/worlds/unity_simulation.tar.gz \
  robotnik_benchmark_unity_ws/src/robotnik_unity/worlds/unity_simulation_only.tar.gz
```

Compila el endpoint ROS y el wrapper Unity:

```bash
./scripts/build_workspace.sh unity
source robotnik_benchmark_unity_ws/install/setup.bash
```

Los launchers seleccionan automáticamente el Player correspondiente a
`empty_world` o `simple_world`, y permiten usar GUI/headless, número de robots,
RViz y límite de FPS. Si en el futuro se publica el proyecto fuente de Unity,
se añadirá como submódulo separado junto con su versión exacta del Unity
Editor.

## 6. Ejecutar benchmarks

Comprueba primero la matriz disponible:

```bash
python3 scripts/validate/validate_config.py --list-categories
```

Ejemplo con Gazebo:

```bash
source /opt/ros/jazzy/setup.bash
source robotnik_benchmark_gazebo_ws/install/setup.bash

python3 scripts/execute/run_benchmark.py gazebo_harmonic \
  --category one_robot_empty_world_headless \
  --iterations 1 --iteration_time 10 --warmup-time 5 \
  --startup_timeout 120 --max_retries 0 --monitor-ros
```

Se sustituye `gazebo_harmonic` y el `setup.bash` por el simulador deseado.
Para ejecutar la campaña completa de un simulador:

```bash
source /opt/ros/jazzy/setup.bash
source robotnik_benchmark_<simulador>_ws/install/setup.bash
./scripts/execute/run_simulator_campaign.sh <simulador>
```

Los resultados se guardan en `benchmarks/<simulador>/` y no se versionan.

## 7. Validación

```bash
./scripts/validate_workspace.sh
python3 -m pytest -q scripts/tests
python3 -m compileall -q scripts
```

La validación debe confirmar 24 categorías, submódulos inicializados en sus
commits fijados y presencia de todos los workspaces. Las pruebas unitarias no
lanzan simuladores reales; para la aceptación completa hay que ejecutar además
una prueba mínima en cada backend.

## 8. Actualizar una dependencia

Los submódulos no siguen automáticamente la rama remota. Para actualizar uno:

```bash
cd robotnik_benchmark_webots_ws/src/robotnik_webots
git fetch personal benchmarking-compatibility
git checkout benchmarking-compatibility
git pull --ff-only personal benchmarking-compatibility
cd ../../../../
git add robotnik_benchmark_webots_ws/src/robotnik_webots
```

Después de probar el workspace, actualiza el commit y la tabla de
`docs/repositories.md` en el mismo cambio del repositorio principal.

## 9. Publicar cambios

La rama de integración es `benchmarking-compatibility`. Los cambios del
repositorio principal se publican directamente en esa rama; no se requiere
crear un Pull Request para reproducir o ejecutar los benchmarks.

El repositorio `robotnik_isaac` contiene además un submódulo interno llamado
`robotnik_isaac_ros2_control`. No es necesario para este benchmark y por eso el
bootstrap inicializa sólo los submódulos directos declarados por este
repositorio, no sus dependencias anidadas.
