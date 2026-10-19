#!/usr/bin/env python3
"""Create the selected, reproducible robot-simulator benchmark graphics.

Input layout: ``<input-dir>/<simulator>/<scenario>[/...].csv``.  Every
simulator/scenario/mode combination must contain precisely one five-iteration
``ros2_launch_timings_*.csv`` file.  The program deliberately fails early on
incomplete runs instead of making comparison charts from partial data.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SIMULATORS = ["gazebo_harmonic", "isaac_sim", "mujoco", "o3de", "unity", "webots"]
SIMULATOR_LABELS = dict(zip(SIMULATORS, ["Gazebo Harmonic", "Isaac Sim", "MuJoCo", "O3DE", "Unity", "Webots"]))
# Kept in sync with SELECTED_GRAPHICS_BENCHMARKS_04092026_MIDCOST.
SIMULATOR_COLORS = dict(zip(SIMULATORS, ["#E9A400", "#00A37A", "#CC78A5", "#7A3296", "#55ACE0", "#D95F00"]))
SCENARIOS = [
    ("one_robot_empty_world", "Empty · 1 robot"), ("two_robot_empty_world", "Empty · 2 robots"),
    ("three_robot_empty_world", "Empty · 3 robots"), ("one_robot_simple_world", "Simple · 1 robot"),
    ("two_robot_simple_world", "Simple · 2 robots"), ("three_robot_simple_world", "Simple · 3 robots"),
]
SCENARIO_LABELS = dict(SCENARIOS)
SCENARIO_COLORS = dict(zip(SCENARIO_LABELS, ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00"]))
MODES = {"gui": "", "headless": "_headless", "gui_rviz": "_rviz", "headless_rviz": "_rviz_headless"}
INPUT_ARTIFACT_DIRECTORIES = {"summary", "selected_graphics"}
MODE_TITLES = {"gui": "Simulador GUI", "headless": "Simulador Headless", "gui_rviz": "Simulador GUI + RViz2", "headless_rviz": "Simulador Headless + RViz2"}
METRICS = {
 "first_frame_seconds": ("Tiempo hasta el primer frame", "s", "lower"), "startup_time": ("Startup time", "s", "lower"),
 "real_time_factor_mean": ("Real-time factor (RTF)", "", "higher"), "render_fps_mean": ("Rendering FPS", "FPS", "higher"),
 "cpu_mean_percent": ("Session CPU (host)", "%", "lower"), "cpu_core_peak_mean_percent": ("Pico de CPU por core (host)", "%", "lower"),
 "cpu_core_saturated_mean_count": ("Cores host ≥90 %", "cores", "lower"), "ram_mean_mb": ("Session RAM", "MB", "lower"),
 "gpu_mean_percent": ("GPU usage (global)", "%", "lower"), "gpu_mem_mean_mb": ("Session VRAM", "MB", "lower"),
 "gpu_power_mean_w": ("GPU power", "W", "lower"), "gpu_temperature_mean_c": ("GPU temperature", "°C", "lower"),
 "gpu_clock_mean_mhz": ("GPU clock", "MHz", "neutral"), "iteration_total_time": ("Total iteration time", "s", "lower"),
}
METRIC_NAMES = list(METRICS)
ABSOLUTE_METRICS = ["startup_time", "real_time_factor_mean", "render_fps_mean", "cpu_mean_percent", "ram_mean_mb", "gpu_mem_mean_mb", "gpu_mean_percent"]
COST_METRICS = ["cpu_mean_percent", "gpu_mean_percent", "ram_mean_mb", "gpu_mem_mean_mb", "startup_time"]
WEIGHTS = {"cpu_mean_percent": .27, "gpu_mean_percent": .22, "ram_mean_mb": .22, "gpu_mem_mean_mb": .18, "startup_time": .11}
GUI_METRICS = ["startup_time", "real_time_factor_mean", "render_fps_mean", "cpu_mean_percent", "ram_mean_mb", "gpu_mem_mean_mb", "gpu_mean_percent"]
BUDGETS = {"startup_time": 10, "real_time_factor_mean": 1, "render_fps_mean": 60, "cpu_mean_percent": 25, "ram_mean_mb": 8000, "gpu_mem_mean_mb": 4000, "gpu_mean_percent": 50}
# (horizontal line reach, text reach, vertical offset) for small donut labels.
CALLOUT_LAYOUT = {
    ("gpu_mem_mean_mb", "webots"): (1.10, 1.25, .12),
    ("gpu_mem_mean_mb", "unity"): (1.15, 1.31, -.10),
    ("cpu_mean_percent", "webots"): (1.10, 1.25, 0.),
    ("startup_time", "mujoco"): (1.10, 1.25, 0.),
}

def style():
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "font.size": 10, "axes.grid": False})

def fail(message: str) -> None:
    raise ValueError(f"Invalid benchmark input: {message}")

def load_raw(input_dir: Path, *, require_five_iterations: bool = False) -> pd.DataFrame:
    if not input_dir.is_dir(): fail(f"input directory does not exist: {input_dir}")
    found = [p.name for p in input_dir.iterdir() if p.is_dir()]
    simulator_dirs = [name for name in found if name not in INPUT_ARTIFACT_DIRECTORIES]
    if set(simulator_dirs) != set(SIMULATORS):
        fail(f"expected exactly simulators {SIMULATORS}; found {sorted(simulator_dirs)} (ignored output directories: {sorted(set(found) & INPUT_ARTIFACT_DIRECTORIES)})")
    frames = []
    for simulator in SIMULATORS:
        simulator_dir = input_dir / simulator
        expected_dirs = {scenario + suffix for scenario, _ in SCENARIOS for suffix in MODES.values()}
        actual_dirs = {p.name for p in simulator_dir.iterdir() if p.is_dir()}
        if actual_dirs != expected_dirs: fail(f"{simulator}: expected 24 scenario/mode directories; missing={sorted(expected_dirs-actual_dirs)}, unexpected={sorted(actual_dirs-expected_dirs)}")
        for scenario, _ in SCENARIOS:
            for mode, suffix in MODES.items():
                directory = simulator_dir / f"{scenario}{suffix}"
                files = sorted(directory.glob("ros2_launch_timings_*.csv"))
                if not files: fail(f"{directory}: no ros2_launch_timings CSV found")
                run_frames = []
                for file in files:
                    try:
                        frame = pd.read_csv(file)
                    except (OSError, pd.errors.ParserError, pd.errors.EmptyDataError) as error:
                        fail(f"cannot read {file}: {error}")
                    missing = set(METRIC_NAMES) - set(frame.columns)
                    if missing: fail(f"{file}: missing metrics {sorted(missing)}")
                    run_frames.append(frame)
                frame = pd.concat(run_frames, ignore_index=True)
                if frame.empty: fail(f"{directory}: timing CSV files contain no iterations")
                if require_five_iterations and len(frame) != 5:
                    fail(f"{directory}: expected 5 combined iterations, found {len(frame)}")
                frame = frame.copy(); frame["simulator"] = simulator; frame["scenario"] = scenario; frame["mode"] = mode; frame["iteration_count"] = len(frame)
                frames.append(frame)
    raw = pd.concat(frames, ignore_index=True)
    raw[METRIC_NAMES] = raw[METRIC_NAMES].apply(pd.to_numeric, errors="coerce")
    allowed_missing = (raw["mode"].isin(["headless", "headless_rviz"]))
    invalid_missing = raw[METRIC_NAMES].isna()
    invalid_missing["render_fps_mean"] &= ~allowed_missing
    if invalid_missing.any().any():
        bad_columns = invalid_missing.columns[invalid_missing.any()].tolist()
        fail(f"one or more required metric values are non-numeric or missing: {bad_columns}")
    return raw

def ordered(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["simulator"] = pd.Categorical(result["simulator"], SIMULATORS, ordered=True)
    result["scenario"] = pd.Categorical(result["scenario"], list(SCENARIO_LABELS), ordered=True)
    return result.sort_values(["mode", "simulator", "scenario"])

def savefig(fig, path: Path, dpi: int):
    path.parent.mkdir(parents=True, exist_ok=True); fig.tight_layout(); fig.savefig(path, dpi=dpi, bbox_inches="tight"); plt.close(fig)

def remove_temporary_csvs(output: Path) -> int:
    """Remove calculation exports once their corresponding images are saved."""
    paths = list(output.rglob("*.csv"))
    for path in paths:
        path.unlink()
    return len(paths)

def ylabel(metric):
    name, unit, _ = METRICS[metric]; return f"{name} ({unit})" if unit else name

def absolute(summary, output, dpi, benchmark_date):
    x = np.arange(len(SIMULATORS)); width = .12
    for mode in MODES:
        data = summary[summary["mode"] == mode]
        for metric in ABSOLUTE_METRICS:
            fig, ax = plt.subplots(figsize=(14, 7)); ymax = data[metric].max()
            if data[metric].notna().sum() == 0:
                ax.text(.5, .5, "Metric not recorded for this mode", ha="center", va="center", transform=ax.transAxes)
                ax.set(xticks=x, xticklabels=[SIMULATOR_LABELS[s] for s in SIMULATORS], ylabel=ylabel(metric), title=f"{benchmark_date} — {METRICS[metric][0]} · {MODE_TITLES[mode]}")
                metric_path = output / "absolute_metrics" / mode / f"{metric}"; metric_path.parent.mkdir(parents=True, exist_ok=True)
                data[["simulator", "scenario", metric]].to_csv(metric_path.with_suffix(".csv"), index=False); savefig(fig, metric_path.with_suffix(".png"), dpi)
                continue
            for index, scenario in enumerate(SCENARIO_LABELS):
                values = data[data["scenario"] == scenario].set_index("simulator").reindex(SIMULATORS)[metric].to_numpy()
                ax.bar(x + (index-2.5)*width, values, width, color=SCENARIO_COLORS[scenario], label=SCENARIO_LABELS[scenario])
            means = data.groupby("simulator", observed=True)[metric].mean().reindex(SIMULATORS)
            metric_path = output / "absolute_metrics" / mode / f"{metric}"
            metric_path.parent.mkdir(parents=True, exist_ok=True)
            data[["simulator", "scenario", metric]].to_csv(metric_path.with_suffix(".csv"), index=False)
            for index, value in enumerate(means):
                ax.hlines(value, index-.44, index+.44, colors="#FF6B6B", linestyles="--", linewidth=1.8)
                ax.text(index, value, f"{value:.3f}" if metric == "real_time_factor_mean" else f"{value:.2f}", color="#FF6B6B", ha="center", va="bottom", fontsize=12, fontweight="bold", bbox={"facecolor":"white", "edgecolor":"#FF6B6B", "boxstyle":"round,pad=0.18", "alpha":.96})
            if metric == "real_time_factor_mean": ax.axhline(1, color="black", linewidth=.9, alpha=.6); ax.set_ylim(top=1.4)
            else: ax.set_ylim(top=ymax * 1.14 if ymax > 0 else 1)
            ax.set_xticks(x, [SIMULATOR_LABELS[s] for s in SIMULATORS], rotation=15); ax.set_ylabel(ylabel(metric)); ax.set_title(f"{benchmark_date} — {METRICS[metric][0]} · {MODE_TITLES[mode]}")
            ax.grid(axis="y", linestyle="--", alpha=.28); ax.legend(title="Scenario", ncol=2, fontsize=8)
            savefig(fig, metric_path.with_suffix(".png"), dpi)

def gui_averages(summary):
    return summary[summary["mode"] == "gui"].groupby("simulator", observed=True)[METRIC_NAMES].mean().reindex(SIMULATORS)

def normalized_comparison(averages, output, dpi):
    selected = ["cpu_mean_percent", "gpu_mean_percent", "ram_mean_mb", "gpu_mem_mean_mb", "real_time_factor_mean"]
    absolute = averages[selected].copy(); norm = pd.DataFrame(index=SIMULATORS)
    for metric in selected:
        low, high = absolute[metric].min(), absolute[metric].max()
        values = pd.Series(1., index=SIMULATORS) if np.isclose(low, high) else (absolute[metric]-low)/(high-low)
        norm[metric] = 1-values if metric in COST_METRICS else values
    norm["overall_mean"] = norm.mean(axis=1); directory = output / "comparisons" / "normalized_metrics"; directory.mkdir(parents=True, exist_ok=True)
    norm.rename_axis("simulator").reset_index().to_csv(directory / "normalized_metrics.csv", index=False); absolute.rename_axis("simulator").reset_index().to_csv(directory / "absolute_gui_metrics.csv", index=False)
    fig, ax = plt.subplots(figsize=(14, 7)); x=np.arange(6); width=.14
    palette=["#0072B2", "#009E73", "#E69F00", "#CC79A7", "#56B4E9"]
    for i, metric in enumerate(selected): ax.bar(x+(i-2)*width, norm[metric], width, label=METRICS[metric][0], color=palette[i])
    ax.scatter(x, norm["overall_mean"], marker="D", color="#E31A1C", s=76, zorder=4, label="Overall mean")
    for i,v in enumerate(norm["overall_mean"]): ax.annotate(f"{v:.2f}", (i, v), xytext=(0, 12), textcoords="offset points", color="#E31A1C", ha="center", fontsize=11, fontweight="bold", bbox={"facecolor":"white", "edgecolor":"none", "boxstyle":"round,pad=0.18", "alpha":.92})
    ax.set(xlim=(-.5,5.5), ylim=(0,1), xticks=x, xticklabels=[SIMULATOR_LABELS[s] for s in SIMULATORS], ylabel="Normalized score (higher is better)", title="Normalized metric comparison")
    ax.title.set_y(1.06)
    fig.subplots_adjust(top=.84)
    ax.grid(axis="y", linestyle="--", alpha=.28); ax.legend(ncol=2); savefig(fig, directory / "normalized_metrics.png", dpi)

def heat_table(matrix, title, path, dpi, positive_good=False, row_labels=None):
    fig, ax = plt.subplots(figsize=(14, max(3.5, 1.15*len(matrix)+2))); ax.axis("off")
    values=matrix.to_numpy(float); cells=[[f"{v:+.2f}%" for v in row] for row in values]
    labels = row_labels or [METRICS[m][0] for m in matrix.index]
    table=ax.table(cellText=cells, rowLabels=labels, colLabels=[SIMULATOR_LABELS.get(s, s) for s in matrix.columns], loc="center", cellLoc="center")
    table.auto_set_font_size(False); table.set_fontsize(10); table.scale(1,2)
    cmap=plt.get_cmap("RdYlGn" if positive_good else "RdYlGn_r")
    for r, metric in enumerate(matrix.index, 1):
        limit=max(abs(values[r-1]).max(), 1e-12); normal=mcolors.TwoSlopeNorm(vmin=-limit, vcenter=0, vmax=limit)
        for c in range(len(matrix.columns)): table[(r,c)].set_facecolor(cmap(normal(values[r-1,c])))
    ax.set_title(title, fontsize=16, fontweight="bold", pad=24); savefig(fig,path,dpi)

def presentation(summary, output, dpi):
    directory=output/"comparisons"/"cost_and_savings"; directory.mkdir(parents=True,exist_ok=True)
    modes={m: summary[summary["mode"]==m].set_index(["simulator","scenario"])[COST_METRICS] for m in ("gui","gui_rviz","headless")}
    rviz=(100*(modes["gui_rviz"]-modes["gui"])/modes["gui"]).groupby(level="simulator", observed=True).mean().T.reindex(columns=SIMULATORS)
    headless=(-100*(modes["headless"]-modes["gui"])/modes["gui"]).groupby(level="simulator", observed=True).mean().T.reindex(columns=SIMULATORS)
    rviz.to_csv(directory/"rviz2_additional_cost.csv"); headless.to_csv(directory/"headless_savings.csv")
    def global_bar(values, title, xlabel, filename):
        fig, ax = plt.subplots(figsize=(14, 7)); y=np.arange(len(SIMULATORS)); values=values.reindex(SIMULATORS)
        ax.barh(y, values, color=[SIMULATOR_COLORS[s] for s in SIMULATORS], height=.58)
        ax.set(yticks=y, yticklabels=[SIMULATOR_LABELS[s] for s in SIMULATORS], xlabel=xlabel, title=title); ax.invert_yaxis(); ax.grid(axis="x", alpha=.3); ax.set_axisbelow(True)
        pad=max(float(values.abs().max())*.025, .25)
        for i,value in enumerate(values): ax.text(value + (pad if value >= 0 else -pad), i, f"{value:+.1f}%", va="center", ha="left" if value >= 0 else "right", fontsize=13, fontweight="bold")
        ax.set_xlim(min(0, values.min()-pad*4), max(0, values.max()+pad*7)); savefig(fig, directory/filename, dpi)
    rviz_global=rviz.T.mul(pd.Series(WEIGHTS), axis=1).sum(axis=1)
    headless_global=headless.T.mul(pd.Series(WEIGHTS), axis=1).sum(axis=1)
    global_bar(rviz_global, "Additional cost of RViz2", "Global additional cost (%)", "rviz2_additional_cost.png")
    global_bar(headless_global, "Global savings with Headless", "Global improvement / saving (%)", "headless_savings.png")
    weights=pd.DataFrame({"Metric":[METRICS[m][0] for m in COST_METRICS],"Weight": [WEIGHTS[m] for m in COST_METRICS],"Percentage":[100*WEIGHTS[m] for m in COST_METRICS]})
    if not np.isclose(weights.Percentage.sum(),100): raise RuntimeError("weights must total 100%")
    weights.to_csv(directory/"global_cost_weights.csv",index=False)
    fig,ax=plt.subplots(figsize=(8,8)); ax.axis("off")
    t=ax.table(cellText=[[r.Metric,f"{r.Percentage:.0f} %"] for _,r in weights.iterrows()],colLabels=["Metric","Weight"],bbox=[.22,.23,.56,.55],cellLoc="center")
    t.auto_set_font_size(False);t.set_fontsize(14)
    for c in range(2): t[(0,c)].set_facecolor("#F3D2DA"); t[(0,c)].get_text().set_fontweight("bold")
    for r in range(1,len(weights)+1): t[(r,1)].get_text().set_fontweight("bold")
    ax.text(.5,.82,"Global weighted average",ha="center",va="center",color="white",fontsize=16,fontweight="bold",bbox={"facecolor":"#C9003D","edgecolor":"none","boxstyle":"square,pad=.52"})
    savefig(fig,directory/"global_cost_weights.png",dpi)
    indexes={}
    for transition, pairs in {"1→2 robots":[("one_robot_empty_world","two_robot_empty_world"),("one_robot_simple_world","two_robot_simple_world")],"2→3 robots":[("two_robot_empty_world","three_robot_empty_world"),("two_robot_simple_world","three_robot_simple_world")]}.items():
        source=modes["gui_rviz"]
        indexes[transition]=pd.concat([100*(source.xs(b,level="scenario")-source.xs(a,level="scenario"))/source.xs(a,level="scenario") for a,b in pairs]).groupby(level=0, observed=True).mean().mul(pd.Series(WEIGHTS)).sum(axis=1)
    robot=pd.DataFrame(indexes).reindex(SIMULATORS); robot.to_csv(directory/"robot_scaling_cost.csv",index_label="simulator")
    global_bar(robot.mean(axis=1), "Average weighted global cost of adding one robot", "Average global weighted cost (%)", "robot_scaling_cost.png")

def gui_options(averages, output, dpi):
    directory=output/"gui_overview"; directory.mkdir(parents=True,exist_ok=True)
    panel_metrics=["cpu_mean_percent","gpu_mean_percent","gpu_mem_mean_mb","ram_mean_mb","render_fps_mean","startup_time"]
    panel_names=["CPU","GPU","VRAM","RAM","FPS","Startup"]
    panel_units=["Usage (%)","Usage (%)","Memory (MB)","Memory (MB)","FPS","Time (s)"]
    def stacked(ax, metric, name, unit, normalized=False):
        bottom=0.
        for simulator in SIMULATORS:
            value=float(averages.loc[simulator,metric]) * (100 / BUDGETS[metric] if normalized else 1)
            bar=ax.bar([0],[value],bottom=bottom,color=SIMULATOR_COLORS[simulator],width=.55,edgecolor="white",linewidth=1)
            label=f"{bottom+value:.1f}%" if normalized else f"{bottom+value:.1f}"
            ax.annotate(label,xy=(.28,bottom+value),xytext=(12, 8 if value < max(averages[metric])*.2 else 0),textcoords="offset points",va="center",fontsize=10,fontweight="bold",bbox={"facecolor":"white","edgecolor":SIMULATOR_COLORS[simulator],"boxstyle":"round,pad=.16"},arrowprops={"arrowstyle":"-","color":SIMULATOR_COLORS[simulator],"lw":1} if value < max(averages[metric])*.2 else None)
            bottom += value
        ax.set(xlim=(-.75,.95),xticks=[0],xticklabels=[name],ylabel=unit); ax.get_xticklabels()[0].set_fontweight("bold");ax.grid(axis="y",alpha=.25);ax.set_axisbelow(True)
    fig,axes=plt.subplots(2,3,figsize=(16,10))
    for ax,metric,name,unit in zip(axes.flat,panel_metrics,panel_names,panel_units): stacked(ax,metric,name,unit)
    fig.suptitle("Absolute GUI averages\nCompact grouped segmented bars",fontsize=17,fontweight="bold");fig.legend([plt.Rectangle((0,0),1,1,color=SIMULATOR_COLORS[s]) for s in SIMULATORS],[SIMULATOR_LABELS[s] for s in SIMULATORS],loc="lower center",ncol=3,fontsize=11);fig.subplots_adjust(bottom=.22);savefig(fig,directory/"absolute_gui_stacks.png",dpi)
    averages[panel_metrics].rename_axis("simulator").reset_index().to_csv(directory/"absolute_gui_stacks.csv",index=False)
    fig,ax=plt.subplots(figsize=(17,9)); x=np.arange(len(panel_metrics)); width=.12
    for simulator_index,simulator in enumerate(SIMULATORS):
        raw_values=np.array([100*averages.loc[simulator,metric]/BUDGETS[metric] for metric in panel_metrics],dtype=float)
        drawn_values=np.minimum(raw_values,100)
        bars=ax.bar(x+(simulator_index-2.5)*width,drawn_values,width,color=SIMULATOR_COLORS[simulator],label=SIMULATOR_LABELS[simulator],edgecolor="white",linewidth=.8)
        for bar,raw_value,drawn_value in zip(bars,raw_values,drawn_values):
            if raw_value >= 100:
                ax.text(bar.get_x()+bar.get_width()/2, 101.5, f"{raw_value:.0f}%",ha="center",va="bottom",fontsize=8,fontweight="bold",color=SIMULATOR_COLORS[simulator],rotation=90)
    ax.axhline(100,color="#555555",linestyle="--",label="Budget limit (100%)");ax.set(ylim=(0,108),xticks=x,xticklabels=panel_names,ylabel="Budget used (%)",title="Reference-normalized GUI averages (per simulator)");ax.grid(axis="y",alpha=.25);ax.set_axisbelow(True);ax.legend(ncol=7,loc="upper center",bbox_to_anchor=(.5,-.12),fontsize=9);fig.subplots_adjust(bottom=.2);savefig(fig,directory/"gui_budget_utilization.png",dpi)
    (100*averages[panel_metrics]/pd.Series(BUDGETS)).rename_axis("simulator").reset_index().to_csv(directory/"gui_budget_utilization.csv",index=False)
    fig,axes=plt.subplots(2,3,figsize=(19,12)); pie_names={"cpu_mean_percent":"CPU","gpu_mean_percent":"GPU","gpu_mem_mean_mb":"VRAM","ram_mean_mb":"RAM","render_fps_mean":"FPS","startup_time":"Startup"}; pie_units={"cpu_mean_percent":"%","gpu_mean_percent":"%","gpu_mem_mean_mb":"MB","ram_mean_mb":"MB","render_fps_mean":"FPS","startup_time":"s"}; short={"Gazebo Harmonic":"Gazebo"}
    for ax,metric in zip(axes.flat,panel_metrics):
        values=averages.loc[SIMULATORS,metric].to_numpy(float);wedges,_=ax.pie(values,colors=[SIMULATOR_COLORS[s] for s in SIMULATORS],startangle=90,counterclock=False,wedgeprops={"width":.62,"edgecolor":"white","linewidth":1.4})
        for wedge,simulator,value in zip(wedges,SIMULATORS,values):
            angle=(wedge.theta1+wedge.theta2)/2; rad=np.deg2rad(angle); fraction=(wedge.theta2-wedge.theta1)/360; label=f"{short.get(SIMULATOR_LABELS[simulator],SIMULATOR_LABELS[simulator])}\n{value:.1f}"
            if fraction < .09:
                line_reach, text_reach, y_offset = CALLOUT_LAYOUT.get((metric, simulator), (1.15, 1.34, 0.))
                start=(.75*np.cos(rad),.75*np.sin(rad)); elbow=(1.03*np.cos(rad),1.03*np.sin(rad)+y_offset); line_end=(line_reach*np.sign(np.cos(rad)),elbow[1]); label_point=(text_reach*np.sign(np.cos(rad)),elbow[1])
                ax.plot([start[0],elbow[0]],[start[1],elbow[1]],color="white",lw=6.2,solid_capstyle="round",zorder=3)
                ax.plot([start[0],elbow[0],line_end[0]],[start[1],elbow[1],line_end[1]],color=SIMULATOR_COLORS[simulator],lw=3.2,solid_capstyle="round",zorder=4)
                ax.text(*label_point,label,ha="center",va="center",multialignment="center",fontsize=15,fontweight="bold")
                ax.scatter(*start,s=88,color="white",zorder=4)
                ax.scatter(*start,s=28,color=SIMULATOR_COLORS[simulator],edgecolors="white",linewidths=.8,zorder=5)
            else:
                text_color="white" if simulator in {"isaac_sim","o3de","unity","webots"} else "black";ax.text(.72*np.cos(rad),.72*np.sin(rad),label,ha="center",va="center",multialignment="center",fontsize=15,fontweight="bold",color=text_color)
        ax.text(0, .06, pie_names[metric],ha="center",va="center",fontsize=22,fontweight="bold");ax.text(0,-.13,pie_units[metric],ha="center",va="center",fontsize=15,color="#666666")
    savefig(fig,directory/"gui_metric_donuts.png",dpi)
    (100*averages[panel_metrics].div(averages[panel_metrics].sum(axis=0))).rename_axis("simulator").reset_index().to_csv(directory/"gui_metric_donuts.csv",index=False)

def simulator_table(averages, output, dpi):
    limits={"startup_time":(5,12),"real_time_factor_mean":(.5,1),"render_fps_mean":(30,60),"cpu_mean_percent":(0,25),"ram_mean_mb":(0,8000),"gpu_mem_mean_mb":(0,4000),"gpu_mean_percent":(20,50)}
    fig,ax=plt.subplots(figsize=(18,5));ax.axis("off"); rows=[]; quality=[]
    for s in SIMULATORS:
        rows.append([SIMULATOR_LABELS[s]]+[f"{averages.loc[s,m]:.2f}" for m in GUI_METRICS]); q=[]
        for m in GUI_METRICS:
            lo,hi=limits[m];v=np.clip((averages.loc[s,m]-lo)/(hi-lo),0,1);q.append(v if METRICS[m][2]=="higher" else 1-v)
        quality.append(q)
    t=ax.table(cellText=rows,colLabels=["Simulator","Startup time (s)","Real-time factor","FPS","CPU (%)","RAM (MB)","VRAM (MB)","GPU (%)"],loc="center",cellLoc="center");t.auto_set_font_size(False);t.set_fontsize(9);t.scale(1,2.2);cmap=plt.get_cmap("RdYlGn")
    for r,s in enumerate(SIMULATORS,1): t[(r,0)].set_facecolor(SIMULATOR_COLORS[s]);[t[(r,c)].set_facecolor(cmap(quality[r-1][c-1])) for c in range(1,8)]
    ax.set_title("Simulator comparison table — GUI average",pad=22);savefig(fig,output/"simulator_summary"/"simulator_comparison.png",dpi)
    averages[GUI_METRICS].rename_axis("simulator").reset_index().to_csv(output/"simulator_summary"/"simulator_comparison.csv",index=False)

def main():
    root=Path(__file__).resolve().parents[2]; p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input-dir","--benchmarks-dir",dest="input_dir",type=Path,default=root/"benchmarks");p.add_argument("--output-dir","--output",dest="output_dir",type=Path,default=root/"benchmarks"/"summary"/"graphics");p.add_argument("--dpi",type=int,default=180);p.add_argument("--keep-existing",action="store_true");p.add_argument("--require-five-iterations",action="store_true",help="fail unless every simulator/scenario/mode has exactly five combined timing rows");args=p.parse_args()
    if args.output_dir.exists() and not args.keep_existing: shutil.rmtree(args.output_dir)
    style();print("Loading and validating benchmark CSV files...");raw=load_raw(args.input_dir,require_five_iterations=args.require_five_iterations);summary=ordered(raw.groupby(["mode","simulator","scenario"],as_index=False,observed=True)[METRIC_NAMES].mean());args.output_dir.mkdir(parents=True,exist_ok=True);raw.to_csv(args.output_dir/"raw_benchmarks.csv",index=False);summary.to_csv(args.output_dir/"summary.csv",index=False)
    iteration_counts=raw.groupby(["mode","simulator","scenario"],observed=True)["iteration_count"].first().reset_index();iteration_counts.to_csv(args.output_dir/"iteration_counts.csv",index=False)
    nonstandard=iteration_counts[iteration_counts["iteration_count"] != 5]
    if not nonstandard.empty: print(f"Warning: {len(nonstandard)} of {len(iteration_counts)} combinations do not have five iterations (use --require-five-iterations to reject them).")
    timestamps=pd.to_datetime(raw.get("timestamp"),errors="coerce") if "timestamp" in raw else pd.Series(dtype="datetime64[ns]")
    benchmark_date=timestamps.min().strftime("%d %b %Y").lstrip("0") if not timestamps.empty and pd.notna(timestamps.min()) else "Benchmark date unavailable"
    print("Generating absolute charts...");absolute(summary,args.output_dir,args.dpi,benchmark_date); averages=gui_averages(summary);print("Generating general comparisons...");normalized_comparison(averages,args.output_dir,args.dpi);presentation(summary,args.output_dir,args.dpi);print("Generating GUI and table summaries...");gui_options(averages,args.output_dir,args.dpi);simulator_table(averages,args.output_dir,args.dpi);temporary_count=remove_temporary_csvs(args.output_dir);print(f"Graphics generated: {len(list(args.output_dir.rglob('*.png')))} PNG files");print(f"Temporary CSV files removed: {temporary_count}");return 0
if __name__ == "__main__": raise SystemExit(main())
