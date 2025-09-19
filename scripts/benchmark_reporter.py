import os
import glob
import pandas as pd

bench_dir = os.path.join(os.getcwd(), "benchmarks")
if not os.path.exists(bench_dir):
    raise FileNotFoundError(f"The folder '{bench_dir}' does not exist.")

# Orden fijo de categorías
CATEGORY_ORDER = [
    "",
    "one_robot_emtpy_world",
    "two_robot_emtpy_world",
    "three_robot_emtpy_world",
    "one_robot_simple_world",
    "two_robot_simple_world",
    "three_robot_simple_world",
    "one_robot_emtpy_world_rviz",
    "two_robot_emtpy_world_rviz",
    "three_robot_emtpy_world_rviz",
    "one_robot_simple_world_rviz",
    "two_robot_simple_world_rviz",
    "three_robot_simple_world_rviz",
]

md_blocks = []

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
        mean_data = all_data.mean(numeric_only=True)

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

        # Guardar métricas para la tabla resumen
        summary_table[category_folder] = {
            "Startup time (s)": f"{duration:.2f} s",
            "RealTime Factor": f"{rtf:.2f}",
            "RAM": f"{ram:.2f} MB",
            "CPU": f"{cpu:.2f} %",
            "GPU": f"{gpu:.2f} %"
        }

        # Bloque de detalle de la categoría dentro de un acordeón
        cat_block = f"""<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: {category_folder}</summary>

**Timestamp:** {timestamp}  
**Total iterations:** {iterations}  
**Average measured duration per iteration:** {duration:.2f} s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | {cpu:.2f} %                    |
| RAM average               | {ram:.2f} MB (~{ram_gb:.2f} GB) |
| GPU average               | {gpu:.1f} %                    |
| GPU Memory average        | {gpu_mem:.2f} MB (~{gpu_mem_gb:.2f} GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | {rtf:.4f} (~{rtf*100:.0f} % of real-time) |
| Average iteration time      | {iter_total_time:.2f} s        |

> Simulation runs at ~{rtf*100:.0f} % of real-time (1 s simulated → {1/rtf:.1f} s real).

</details>
"""
        category_blocks.append(cat_block)

    if category_blocks:
        # Tabla resumen siempre visible, usando el orden definido
        metrics = ["Startup time (s)", "RealTime Factor", "RAM", "CPU", "GPU"]
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
