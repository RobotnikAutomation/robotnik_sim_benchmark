import os
import glob
import pandas as pd

bench_dir = os.path.join(os.getcwd(), "benchmarks")
if not os.path.exists(bench_dir):
    raise FileNotFoundError(f"The folder '{bench_dir}' does not exist.")

# Orden fijo de categorías
CATEGORY_ORDER = [
    "",
    "one_robot_empty_world",
    "two_robot_empty_world",
    "three_robot_empty_world",
    "one_robot_simple_world",
    "two_robot_simple_world",
    "three_robot_simple_world",
    "one_robot_empty_world_rviz",
    "two_robot_empty_world_rviz",
    "three_robot_empty_world_rviz",
    "one_robot_simple_world_rviz",
    "two_robot_simple_world_rviz",
    "three_robot_simple_world_rviz",
    "one_robot_empty_world_headless",
    "two_robot_empty_world_headless",
    "three_robot_empty_world_headless",
    "one_robot_simple_world_headless",
    "two_robot_simple_world_headless",
    "three_robot_simple_world_headless",
    "one_robot_empty_world_rviz_headless",
    "two_robot_empty_world_rviz_headless",
    "three_robot_empty_world_rviz_headless",
    "one_robot_simple_world_rviz_headless",
    "two_robot_simple_world_rviz_headless",
    "three_robot_simple_world_rviz_headless",
]

md_blocks = []


def mean_metric(dataframe, column):
    """Return a numeric mean, or None when a CSV does not provide the metric."""
    if column not in dataframe:
        return None
    values = pd.to_numeric(dataframe[column], errors="coerce")
    mean = values.mean()
    return None if pd.isna(mean) else mean


def format_metric(value, decimals=2, unit=""):
    """Format optional metrics consistently in Markdown."""
    if value is None:
        return "n/d"
    return f"{value:.{decimals}f}{unit}"

for sim_folder in sorted(os.listdir(bench_dir)):
    sim_path = os.path.join(bench_dir, sim_folder)
    if not os.path.isdir(sim_path):
        continue

    category_blocks = []
    summary_table = {}  # Para la tabla resumen

    for category_folder in sorted(os.listdir(sim_path)):
        cat_path = os.path.join(sim_path, category_folder)
        if not os.path.isdir(cat_path):
            continue

        csv_files = glob.glob(os.path.join(cat_path, "ros2_launch_timings*.csv"))
        if not csv_files:
            continue

        dfs = [pd.read_csv(f) for f in csv_files]
        all_data = pd.concat(dfs, ignore_index=True)
        timestamp = all_data['timestamp'].max()
        iterations = len(all_data)
        duration = mean_metric(all_data, 'elapsed_seconds')
        cpu = mean_metric(all_data, 'cpu_mean_percent')
        ram = mean_metric(all_data, 'ram_mean_mb')
        gpu = mean_metric(all_data, 'gpu_mean_percent')
        gpu_memory_util = mean_metric(all_data, 'gpu_memory_util_mean_percent')
        gpu_temperature = mean_metric(all_data, 'gpu_temperature_mean_c')
        gpu_power = mean_metric(all_data, 'gpu_power_mean_w')
        gpu_clock = mean_metric(all_data, 'gpu_clock_mean_mhz')
        gpu_mem = mean_metric(all_data, 'gpu_mem_mean_mb')
        rtf = mean_metric(all_data, 'real_time_factor_mean')
        iter_total_time = mean_metric(all_data, 'iteration_total_time')

        ram_gb = None if ram is None else ram / 1024
        gpu_mem_gb = None if gpu_mem is None else gpu_mem / 1024

        # Guardar métricas para la tabla resumen
        summary_table[category_folder] = {
            "Startup time (s)": format_metric(duration, 2, " s"),
            "RealTime Factor": format_metric(rtf, 2),
            "RAM": format_metric(ram, 2, " MB"),
            "CPU": format_metric(cpu, 2, " %"),
            "GPU": format_metric(gpu, 2, " %"),
            "GPU memory bandwidth activity": format_metric(gpu_memory_util, 2, " %"),
            "GPU Temp.": format_metric(gpu_temperature, 1, " °C"),
            "GPU Potencia": format_metric(gpu_power, 2, " W"),
            "GPU Reloj": format_metric(gpu_clock, 1, " MHz"),
            "GPU RAM": "n/d" if gpu_mem is None else f"{gpu_mem:.2f} MB",
        }

        # Bloque de detalle de la categoría dentro de un acordeón
        cat_block = f"""<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: {category_folder}</summary>

**Timestamp:** {timestamp}  
**Total iterations:** {iterations}  
**Average measured duration per iteration:** {format_metric(duration, 2, ' s')}<br>

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | {format_metric(cpu, 2, ' %')}                    |
| RAM average               | {format_metric(ram, 2, ' MB')} (~{format_metric(ram_gb, 2, ' GB')}) |
| GPU average               | {format_metric(gpu, 1, ' %')}                    |
| GPU memory bandwidth activity | {format_metric(gpu_memory_util, 1, ' %')} |
| GPU temperature           | {format_metric(gpu_temperature, 1, ' °C')} |
| GPU power                 | {format_metric(gpu_power, 2, ' W')} |
| GPU graphics clock        | {format_metric(gpu_clock, 1, ' MHz')} |
| GPU Memory average        | {format_metric(gpu_mem, 2, ' MB')} (~{format_metric(gpu_mem_gb, 2, ' GB')}) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | {format_metric(rtf, 4)} (~{format_metric(None if rtf is None else rtf * 100, 0, ' %')} of real-time) |
| Average iteration time      | {format_metric(iter_total_time, 2, ' s')}        |

{'' if rtf is None or rtf == 0 else f'> Simulation runs at ~{rtf*100:.0f} % of real-time (1 s simulated → {1/rtf:.1f} s real).'}

</details>
"""
        category_blocks.append(cat_block)

    if category_blocks:
        # Tabla resumen siempre visible, usando el orden definido
        metrics = [
            "Startup time (s)", "RealTime Factor", "RAM", "CPU", "GPU",
            "GPU memory bandwidth activity", "GPU Temp.", "GPU Potencia", "GPU Reloj", "GPU RAM",
        ]
        table_header = "| Category | " + " | ".join(metrics) + " |"
        table_sep = "|" + "---|"*(len(metrics)+1)
        table_rows = []
        for cat in CATEGORY_ORDER:
            if cat in summary_table:
                values = summary_table[cat]
                row = f"| {cat} "
                for m in metrics:
                    row += f"| {values[m]} "
                row += "|"
                table_rows.append(row)
        table_md = "\n".join([table_header, table_sep] + table_rows)

        # Bloque del simulador: título + tabla + categorías plegables
        category_text = "\n\n".join(category_blocks)
        sim_block = f"""## Simulator: {sim_folder}

### Summary Table

{table_md}

{category_text}
"""
        md_blocks.append(sim_block)

# Generar Markdown final
if md_blocks:
    markdown = "# 📊 Performance Report (all simulators and categories)\n\n" + "\n\n".join(md_blocks)
    md_file = os.path.join(bench_dir, "performance_report.md")
    with open(md_file, "w") as f:
        f.write(markdown)
    print(f"✅ Markdown report generated: {md_file}")
else:
    print("⚠️ No CSV data found in any simulator/category folder. Markdown not generated.")
