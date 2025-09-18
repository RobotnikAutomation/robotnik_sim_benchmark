import os
import glob
import pandas as pd

# Carpeta de benchmarks
bench_dir = os.path.join(os.getcwd(), "benchmarks")

if not os.path.exists(bench_dir):
    raise FileNotFoundError(f"The folder '{bench_dir}' does not exist.")

# Inicializar lista de bloques Markdown
md_blocks = []

# Recorrer subcarpetas
for sim_folder in sorted(os.listdir(bench_dir)):
    sim_path = os.path.join(bench_dir, sim_folder)
    if not os.path.isdir(sim_path):
        continue

    # Buscar archivos CSV
    csv_files = glob.glob(os.path.join(sim_path, "ros2_launch_timings*.csv"))
    if not csv_files:
        continue  # No hay datos, se salta esta carpeta

    # Combinar todos los CSV de esta carpeta
    dfs = [pd.read_csv(f) for f in csv_files]
    all_data = pd.concat(dfs, ignore_index=True)

    # Calcular medias
    mean_data = all_data.mean(numeric_only=True)

    simulator = all_data['simulator'].iloc[0]
    timestamp = all_data['timestamp'].max()
    iterations = int(all_data['iteration'].sum())
    duration = mean_data['elapsed_seconds']
    cpu = mean_data['cpu_mean_percent']
    ram = mean_data['ram_mean_mb']
    gpu = mean_data['gpu_mean_percent']
    gpu_mem = mean_data['gpu_mem_mean_mb']
    rtf = mean_data['real_time_factor_mean']
    iter_total_time = mean_data['iteration_total_time']

    ram_gb = ram / 1024
    gpu_mem_gb = gpu_mem / 1024

    # Crear bloque Markdown para este simulador
    block = f"""## Simulator: {simulator}

**Timestamp:** {timestamp}  
**Total iterations:** {iterations}  
**Average measured duration per iteration:** {duration:.2f} s  

### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | {cpu:.2f} %                    |
| RAM average               | {ram:.2f} MB (~{ram_gb:.2f} GB) |
| GPU average               | {gpu:.1f} %                    |
| GPU Memory average        | {gpu_mem:.2f} MB (~{gpu_mem_gb:.2f} GB) |

### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | {rtf:.4f} (~{rtf*100:.0f} % of real-time) |
| Average iteration time      | {iter_total_time:.2f} s        |

> This means the simulation runs at ~{rtf*100:.0f} % of real-time speed (e.g., 1 second in the simulated world → {1/rtf:.1f} seconds in real-time).
"""
    md_blocks.append(block)

# Generar Markdown final
if md_blocks:
    markdown = "# 📊 Performance Report (all simulators)\n\n" + "\n---\n".join(md_blocks)

    md_file = os.path.join(bench_dir, "performance_report.md")
    with open(md_file, "w") as f:
        f.write(markdown)

    print(f"✅ Markdown report generated: {md_file}")
else:
    print("⚠️ No CSV data found in any simulator folder. Markdown not generated.")