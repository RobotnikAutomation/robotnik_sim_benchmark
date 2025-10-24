# 📊 Performance Report (all simulators and categories)

## Simulator: gazebo_harmonic

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_empty_world | 4.03 s | 1.00 | 2418.14 MB | 13.34 % | 34.20 % | 1722.30 MB |
| two_robot_empty_world | 5.58 s | 0.70 | 2654.71 MB | 14.98 % | 21.50 % | 1869.12 MB |
| three_robot_empty_world | 7.90 s | 0.40 | 2966.15 MB | 14.49 % | 26.17 % | 1990.83 MB |
| one_robot_simple_world | 4.64 s | 0.99 | 2649.34 MB | 12.07 % | 26.89 % | 1668.56 MB |
| two_robot_simple_world | 5.43 s | 0.99 | 2883.03 MB | 20.00 % | 24.75 % | 1824.25 MB |
| three_robot_simple_world | 8.16 s | 1.00 | 3186.29 MB | 19.50 % | 28.17 % | 1991.00 MB |
| one_robot_empty_world_rviz | 4.32 s | 1.00 | 2837.59 MB | 14.14 % | 36.11 % | 4133.11 MB |
| two_robot_empty_world_rviz | 5.07 s | 0.80 | 3521.06 MB | 17.06 % | 47.14 % | 6759.71 MB |
| three_robot_empty_world_rviz | 7.94 s | 0.73 | 4254.94 MB | 23.20 % | 75.50 % | 9539.33 MB |
| one_robot_simple_world_rviz | 4.70 s | 1.00 | 3077.67 MB | 13.89 % | 34.67 % | 4145.78 MB |
| two_robot_simple_world_rviz | 5.49 s | 1.00 | 3755.02 MB | 19.69 % | 53.43 % | 6962.29 MB |
| three_robot_simple_world_rviz | 7.98 s | 0.47 | 4472.12 MB | 22.98 % | 62.83 % | 9161.33 MB |
| one_robot_empty_world_headless | 4.33 s | 0.99 | 1451.54 MB | 9.62 % | 46.45 % | 1270.55 MB |
| two_robot_empty_world_headless | 5.32 s | 0.99 | 1759.66 MB | 12.97 % | 38.89 % | 1425.56 MB |
| three_robot_empty_world_headless | 7.99 s | 1.00 | 2021.84 MB | 15.55 % | 39.43 % | 1590.29 MB |
| one_robot_simple_world_headless | 4.28 s | 1.00 | 1553.04 MB | 8.89 % | 39.27 % | 1251.27 MB |
| two_robot_simple_world_headless | 5.18 s | 0.50 | 1803.91 MB | 8.92 % | 45.56 % | 1422.00 MB |
| three_robot_simple_world_headless | 8.13 s | 0.66 | 2102.48 MB | 15.34 % | 34.14 % | 1601.71 MB |
| one_robot_empty_world_rviz_headless | 4.72 s | 1.00 | 1851.60 MB | 9.63 % | 28.00 % | 3736.30 MB |
| two_robot_empty_world_rviz_headless | 5.28 s | 0.60 | 2542.55 MB | 14.46 % | 45.62 % | 6326.62 MB |
| three_robot_empty_world_rviz_headless | 7.95 s | 0.47 | 3270.55 MB | 19.85 % | 67.83 % | 8984.00 MB |
| one_robot_simple_world_rviz_headless | 0.00 s | 1.00 | 886.18 MB | 2.05 % | 42.42 % | 954.53 MB |
| two_robot_simple_world_rviz_headless | 5.63 s | 0.70 | 2656.30 MB | 14.91 % | 43.88 % | 6221.75 MB |
| three_robot_simple_world_rviz_headless | 8.33 s | 0.66 | 3387.48 MB | 19.87 % | 70.50 % | 8946.00 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world</summary>

**Timestamp:** 2025-10-23T12:20:35.027903  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.03 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 13.34 %                    |
| RAM average               | 2418.14 MB (~2.36 GB) |
| GPU average               | 34.2 %                    |
| GPU Memory average        | 1722.30 MB (~1.68 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9958 (~100 % of real-time) |
| Average iteration time      | 70.41 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-23T12:37:48.189738  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.33 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 9.62 %                    |
| RAM average               | 1451.54 MB (~1.42 GB) |
| GPU average               | 46.5 %                    |
| GPU Memory average        | 1270.55 MB (~1.24 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9911 (~99 % of real-time) |
| Average iteration time      | 65.96 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T12:29:04.414727  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.32 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 14.14 %                    |
| RAM average               | 2837.59 MB (~2.77 GB) |
| GPU average               | 36.1 %                    |
| GPU Memory average        | 4133.11 MB (~4.04 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9958 (~100 % of real-time) |
| Average iteration time      | 68.39 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T12:46:16.745901  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.72 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 9.63 %                    |
| RAM average               | 1851.60 MB (~1.81 GB) |
| GPU average               | 28.0 %                    |
| GPU Memory average        | 3736.30 MB (~3.65 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9956 (~100 % of real-time) |
| Average iteration time      | 65.41 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-10-23T12:24:48.609428  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.64 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 12.07 %                    |
| RAM average               | 2649.34 MB (~2.59 GB) |
| GPU average               | 26.9 %                    |
| GPU Memory average        | 1668.56 MB (~1.63 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9947 (~99 % of real-time) |
| Average iteration time      | 66.88 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-23T12:42:02.989377  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.28 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 8.89 %                    |
| RAM average               | 1553.04 MB (~1.52 GB) |
| GPU average               | 39.3 %                    |
| GPU Memory average        | 1251.27 MB (~1.22 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9959 (~100 % of real-time) |
| Average iteration time      | 65.96 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T12:33:27.537646  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.70 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 13.89 %                    |
| RAM average               | 3077.67 MB (~3.01 GB) |
| GPU average               | 34.7 %                    |
| GPU Memory average        | 4145.78 MB (~4.05 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9958 (~100 % of real-time) |
| Average iteration time      | 68.40 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T12:51:31.403105  
**Total iterations:** 1  
**Average measured duration per iteration:** 0.00 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 2.05 %                    |
| RAM average               | 886.18 MB (~0.87 GB) |
| GPU average               | 42.4 %                    |
| GPU Memory average        | 954.53 MB (~0.93 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.0000 (~100 % of real-time) |
| Average iteration time      | 125.78 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world</summary>

**Timestamp:** 2025-10-23T12:23:26.384698  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.90 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 14.49 %                    |
| RAM average               | 2966.15 MB (~2.90 GB) |
| GPU average               | 26.2 %                    |
| GPU Memory average        | 1990.83 MB (~1.94 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.3988 (~40 % of real-time) |
| Average iteration time      | 68.81 s        |

> Simulation runs at ~40 % of real-time (1 s simulated → 2.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-23T12:40:41.687462  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.99 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 15.55 %                    |
| RAM average               | 2021.84 MB (~1.97 GB) |
| GPU average               | 39.4 %                    |
| GPU Memory average        | 1590.29 MB (~1.55 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9962 (~100 % of real-time) |
| Average iteration time      | 71.39 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T12:32:03.788424  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.94 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 23.20 %                    |
| RAM average               | 4254.94 MB (~4.16 GB) |
| GPU average               | 75.5 %                    |
| GPU Memory average        | 9539.33 MB (~9.32 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7310 (~73 % of real-time) |
| Average iteration time      | 77.85 s        |

> Simulation runs at ~73 % of real-time (1 s simulated → 1.4 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T12:49:10.264159  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.95 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 19.85 %                    |
| RAM average               | 3270.55 MB (~3.19 GB) |
| GPU average               | 67.8 %                    |
| GPU Memory average        | 8984.00 MB (~8.77 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.4655 (~47 % of real-time) |
| Average iteration time      | 70.89 s        |

> Simulation runs at ~47 % of real-time (1 s simulated → 2.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world</summary>

**Timestamp:** 2025-10-23T12:27:40.664149  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.16 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 19.50 %                    |
| RAM average               | 3186.29 MB (~3.11 GB) |
| GPU average               | 28.2 %                    |
| GPU Memory average        | 1991.00 MB (~1.94 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9959 (~100 % of real-time) |
| Average iteration time      | 68.91 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-23T12:44:55.963976  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.13 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 15.34 %                    |
| RAM average               | 2102.48 MB (~2.05 GB) |
| GPU average               | 34.1 %                    |
| GPU Memory average        | 1601.71 MB (~1.56 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6647 (~66 % of real-time) |
| Average iteration time      | 71.41 s        |

> Simulation runs at ~66 % of real-time (1 s simulated → 1.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T12:36:26.897373  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.98 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 22.98 %                    |
| RAM average               | 4472.12 MB (~4.37 GB) |
| GPU average               | 62.8 %                    |
| GPU Memory average        | 9161.33 MB (~8.95 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.4652 (~47 % of real-time) |
| Average iteration time      | 77.84 s        |

> Simulation runs at ~47 % of real-time (1 s simulated → 2.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T12:54:25.307323  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.33 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 19.87 %                    |
| RAM average               | 3387.48 MB (~3.31 GB) |
| GPU average               | 70.5 %                    |
| GPU Memory average        | 8946.00 MB (~8.74 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6644 (~66 % of real-time) |
| Average iteration time      | 71.34 s        |

> Simulation runs at ~66 % of real-time (1 s simulated → 1.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world</summary>

**Timestamp:** 2025-10-23T12:22:02.234307  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.58 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 14.98 %                    |
| RAM average               | 2654.71 MB (~2.59 GB) |
| GPU average               | 21.5 %                    |
| GPU Memory average        | 1869.12 MB (~1.83 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6965 (~70 % of real-time) |
| Average iteration time      | 71.85 s        |

> Simulation runs at ~70 % of real-time (1 s simulated → 1.4 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-23T12:39:14.965939  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.32 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 12.97 %                    |
| RAM average               | 1759.66 MB (~1.72 GB) |
| GPU average               | 38.9 %                    |
| GPU Memory average        | 1425.56 MB (~1.39 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9943 (~99 % of real-time) |
| Average iteration time      | 71.42 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T12:30:30.582995  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.07 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 17.06 %                    |
| RAM average               | 3521.06 MB (~3.44 GB) |
| GPU average               | 47.1 %                    |
| GPU Memory average        | 6759.71 MB (~6.60 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7958 (~80 % of real-time) |
| Average iteration time      | 70.84 s        |

> Simulation runs at ~80 % of real-time (1 s simulated → 1.3 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T12:47:43.987726  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.28 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 14.46 %                    |
| RAM average               | 2542.55 MB (~2.48 GB) |
| GPU average               | 45.6 %                    |
| GPU Memory average        | 6326.62 MB (~6.18 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5974 (~60 % of real-time) |
| Average iteration time      | 71.88 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world</summary>

**Timestamp:** 2025-10-23T12:26:16.402524  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.43 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 20.00 %                    |
| RAM average               | 2883.03 MB (~2.82 GB) |
| GPU average               | 24.8 %                    |
| GPU Memory average        | 1824.25 MB (~1.78 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9927 (~99 % of real-time) |
| Average iteration time      | 72.44 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-23T12:43:29.205414  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.18 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 8.92 %                    |
| RAM average               | 1803.91 MB (~1.76 GB) |
| GPU average               | 45.6 %                    |
| GPU Memory average        | 1422.00 MB (~1.39 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.4985 (~50 % of real-time) |
| Average iteration time      | 70.88 s        |

> Simulation runs at ~50 % of real-time (1 s simulated → 2.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T12:34:53.711218  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.49 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 19.69 %                    |
| RAM average               | 3755.02 MB (~3.67 GB) |
| GPU average               | 53.4 %                    |
| GPU Memory average        | 6962.29 MB (~6.80 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9968 (~100 % of real-time) |
| Average iteration time      | 70.85 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T12:52:58.611435  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.63 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 14.91 %                    |
| RAM average               | 2656.30 MB (~2.59 GB) |
| GPU average               | 43.9 %                    |
| GPU Memory average        | 6221.75 MB (~6.08 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6977 (~70 % of real-time) |
| Average iteration time      | 71.85 s        |

> Simulation runs at ~70 % of real-time (1 s simulated → 1.4 s real).

</details>



## Simulator: isaac_sim

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_empty_world | 11.16 s | 0.99 | 4662.06 MB | 30.71 % | 54.95 % | 4937.85 MB |
| two_robot_empty_world | 11.69 s | 0.90 | 4975.73 MB | 32.01 % | 71.36 % | 5475.30 MB |
| three_robot_empty_world | 12.38 s | 0.50 | 5267.28 MB | 36.71 % | 68.26 % | 5981.55 MB |
| one_robot_simple_world | 11.23 s | 0.90 | 4688.84 MB | 38.63 % | 65.62 % | 4906.77 MB |
| two_robot_simple_world | 11.69 s | 0.70 | 5000.41 MB | 42.75 % | 75.14 % | 5541.64 MB |
| three_robot_simple_world | 12.24 s | 0.20 | 5287.95 MB | 51.52 % | 63.79 % | 6149.99 MB |
| one_robot_empty_world_rviz | 11.17 s | 0.90 | 4944.25 MB | 39.81 % | 59.29 % | 6850.47 MB |
| two_robot_empty_world_rviz | 11.26 s | 0.70 | 5294.95 MB | 43.83 % | 69.90 % | 7394.18 MB |
| three_robot_empty_world_rviz | 12.05 s | 0.60 | 5673.07 MB | 42.80 % | 65.83 % | 7997.56 MB |
| one_robot_simple_world_rviz | 11.25 s | 1.00 | 4959.40 MB | 47.59 % | 66.34 % | 6844.93 MB |
| two_robot_simple_world_rviz | 11.45 s | 0.90 | 5344.01 MB | 44.32 % | 77.07 % | 7464.20 MB |
| three_robot_simple_world_rviz | 12.15 s | 0.40 | 5660.10 MB | 41.34 % | 72.49 % | 7988.27 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world</summary>

**Timestamp:** 2025-10-22T17:39:38.251144  
**Total iterations:** 2  
**Average measured duration per iteration:** 11.16 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 30.71 %                    |
| RAM average               | 4662.06 MB (~4.55 GB) |
| GPU average               | 55.0 %                    |
| GPU Memory average        | 4937.85 MB (~4.82 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9928 (~99 % of real-time) |
| Average iteration time      | 57.42 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T17:48:27.759203  
**Total iterations:** 2  
**Average measured duration per iteration:** 11.17 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 39.81 %                    |
| RAM average               | 4944.25 MB (~4.83 GB) |
| GPU average               | 59.3 %                    |
| GPU Memory average        | 6850.47 MB (~6.69 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8964 (~90 % of real-time) |
| Average iteration time      | 57.40 s        |

> Simulation runs at ~90 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-10-22T17:44:04.100397  
**Total iterations:** 2  
**Average measured duration per iteration:** 11.23 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 38.63 %                    |
| RAM average               | 4688.84 MB (~4.58 GB) |
| GPU average               | 65.6 %                    |
| GPU Memory average        | 4906.77 MB (~4.79 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8964 (~90 % of real-time) |
| Average iteration time      | 57.42 s        |

> Simulation runs at ~90 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T17:52:51.348219  
**Total iterations:** 2  
**Average measured duration per iteration:** 11.25 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 47.59 %                    |
| RAM average               | 4959.40 MB (~4.84 GB) |
| GPU average               | 66.3 %                    |
| GPU Memory average        | 6844.93 MB (~6.68 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9961 (~100 % of real-time) |
| Average iteration time      | 57.29 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world</summary>

**Timestamp:** 2025-10-22T17:42:36.151092  
**Total iterations:** 2  
**Average measured duration per iteration:** 12.38 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 36.71 %                    |
| RAM average               | 5267.28 MB (~5.14 GB) |
| GPU average               | 68.3 %                    |
| GPU Memory average        | 5981.55 MB (~5.84 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.4978 (~50 % of real-time) |
| Average iteration time      | 58.41 s        |

> Simulation runs at ~50 % of real-time (1 s simulated → 2.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T17:51:23.534791  
**Total iterations:** 2  
**Average measured duration per iteration:** 12.05 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 42.80 %                    |
| RAM average               | 5673.07 MB (~5.54 GB) |
| GPU average               | 65.8 %                    |
| GPU Memory average        | 7997.56 MB (~7.81 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5969 (~60 % of real-time) |
| Average iteration time      | 58.63 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world</summary>

**Timestamp:** 2025-10-22T17:46:59.870928  
**Total iterations:** 2  
**Average measured duration per iteration:** 12.24 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 51.52 %                    |
| RAM average               | 5287.95 MB (~5.16 GB) |
| GPU average               | 63.8 %                    |
| GPU Memory average        | 6149.99 MB (~6.01 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.1992 (~20 % of real-time) |
| Average iteration time      | 58.40 s        |

> Simulation runs at ~20 % of real-time (1 s simulated → 5.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T17:55:47.039034  
**Total iterations:** 2  
**Average measured duration per iteration:** 12.15 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 41.34 %                    |
| RAM average               | 5660.10 MB (~5.53 GB) |
| GPU average               | 72.5 %                    |
| GPU Memory average        | 7988.27 MB (~7.80 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.3977 (~40 % of real-time) |
| Average iteration time      | 58.57 s        |

> Simulation runs at ~40 % of real-time (1 s simulated → 2.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world</summary>

**Timestamp:** 2025-10-22T17:41:06.188117  
**Total iterations:** 2  
**Average measured duration per iteration:** 11.69 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 32.01 %                    |
| RAM average               | 4975.73 MB (~4.86 GB) |
| GPU average               | 71.4 %                    |
| GPU Memory average        | 5475.30 MB (~5.35 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8955 (~90 % of real-time) |
| Average iteration time      | 57.40 s        |

> Simulation runs at ~90 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T17:49:55.598599  
**Total iterations:** 2  
**Average measured duration per iteration:** 11.26 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 43.83 %                    |
| RAM average               | 5294.95 MB (~5.17 GB) |
| GPU average               | 69.9 %                    |
| GPU Memory average        | 7394.18 MB (~7.22 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6974 (~70 % of real-time) |
| Average iteration time      | 57.31 s        |

> Simulation runs at ~70 % of real-time (1 s simulated → 1.4 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world</summary>

**Timestamp:** 2025-10-22T17:45:31.998298  
**Total iterations:** 2  
**Average measured duration per iteration:** 11.69 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 42.75 %                    |
| RAM average               | 5000.41 MB (~4.88 GB) |
| GPU average               | 75.1 %                    |
| GPU Memory average        | 5541.64 MB (~5.41 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6973 (~70 % of real-time) |
| Average iteration time      | 57.40 s        |

> Simulation runs at ~70 % of real-time (1 s simulated → 1.4 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T17:54:19.218403  
**Total iterations:** 2  
**Average measured duration per iteration:** 11.45 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 44.32 %                    |
| RAM average               | 5344.01 MB (~5.22 GB) |
| GPU average               | 77.1 %                    |
| GPU Memory average        | 7464.20 MB (~7.29 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8956 (~90 % of real-time) |
| Average iteration time      | 57.34 s        |

> Simulation runs at ~90 % of real-time (1 s simulated → 1.1 s real).

</details>



## Simulator: unity

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_empty_world | 3.20 s | 0.86 | 933.39 MB | 7.46 % | 43.40 % | 2941.26 MB |
| two_robot_empty_world | 5.64 s | 0.83 | 842.92 MB | 7.03 % | 30.91 % | 2128.68 MB |
| three_robot_empty_world | 7.87 s | 1.05 | 797.62 MB | 6.41 % | 18.74 % | 1262.52 MB |
| one_robot_simple_world | 4.02 s | 0.33 | 755.69 MB | 6.09 % | 41.95 % | 1120.40 MB |
| two_robot_simple_world | 7.21 s | 0.17 | 761.84 MB | 6.16 % | 19.80 % | 1192.45 MB |
| three_robot_simple_world | 7.67 s | 1.00 | 800.64 MB | 6.21 % | 12.10 % | 1215.90 MB |
| one_robot_empty_world_rviz | 4.05 s | 1.33 | 1027.60 MB | 8.09 % | 47.29 % | 3399.65 MB |
| two_robot_empty_world_rviz | 7.12 s | 1.33 | 1030.25 MB | 7.72 % | 33.89 % | 3153.33 MB |
| three_robot_empty_world_rviz | 7.57 s | 1.11 | 1035.73 MB | 7.12 % | 35.17 % | 1454.00 MB |
| one_robot_simple_world_rviz | 4.01 s | 1.66 | 1029.17 MB | 7.69 % | 42.65 % | 3379.65 MB |
| two_robot_simple_world_rviz | 6.88 s | 0.17 | 1011.68 MB | 7.32 % | 42.61 % | 1484.83 MB |
| three_robot_simple_world_rviz | 8.02 s | 1.00 | 1054.01 MB | 6.84 % | 37.17 % | 1475.39 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world</summary>

**Timestamp:** 2025-10-23T13:42:40.580090  
**Total iterations:** 5  
**Average measured duration per iteration:** 3.20 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.46 %                    |
| RAM average               | 933.39 MB (~0.91 GB) |
| GPU average               | 43.4 %                    |
| GPU Memory average        | 2941.26 MB (~2.87 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8637 (~86 % of real-time) |
| Average iteration time      | 75.89 s        |

> Simulation runs at ~86 % of real-time (1 s simulated → 1.2 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T13:51:02.577761  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.05 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 8.09 %                    |
| RAM average               | 1027.60 MB (~1.00 GB) |
| GPU average               | 47.3 %                    |
| GPU Memory average        | 3399.65 MB (~3.32 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.3287 (~133 % of real-time) |
| Average iteration time      | 65.01 s        |

> Simulation runs at ~133 % of real-time (1 s simulated → 0.8 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-10-23T13:46:52.830450  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.02 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.09 %                    |
| RAM average               | 755.69 MB (~0.74 GB) |
| GPU average               | 42.0 %                    |
| GPU Memory average        | 1120.40 MB (~1.09 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.3320 (~33 % of real-time) |
| Average iteration time      | 67.59 s        |

> Simulation runs at ~33 % of real-time (1 s simulated → 3.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T13:55:11.693634  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.01 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.69 %                    |
| RAM average               | 1029.17 MB (~1.01 GB) |
| GPU average               | 42.6 %                    |
| GPU Memory average        | 3379.65 MB (~3.30 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.6602 (~166 % of real-time) |
| Average iteration time      | 65.00 s        |

> Simulation runs at ~166 % of real-time (1 s simulated → 0.6 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world</summary>

**Timestamp:** 2025-10-23T13:45:29.901345  
**Total iterations:** 2  
**Average measured duration per iteration:** 7.87 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.41 %                    |
| RAM average               | 797.62 MB (~0.78 GB) |
| GPU average               | 18.7 %                    |
| GPU Memory average        | 1262.52 MB (~1.23 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.0533 (~105 % of real-time) |
| Average iteration time      | 71.08 s        |

> Simulation runs at ~105 % of real-time (1 s simulated → 0.9 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T13:53:51.348208  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.57 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.12 %                    |
| RAM average               | 1035.73 MB (~1.01 GB) |
| GPU average               | 35.2 %                    |
| GPU Memory average        | 1454.00 MB (~1.42 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.1085 (~111 % of real-time) |
| Average iteration time      | 69.04 s        |

> Simulation runs at ~111 % of real-time (1 s simulated → 0.9 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world</summary>

**Timestamp:** 2025-10-23T13:49:42.224349  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.67 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.21 %                    |
| RAM average               | 800.64 MB (~0.78 GB) |
| GPU average               | 12.1 %                    |
| GPU Memory average        | 1215.90 MB (~1.19 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9981 (~100 % of real-time) |
| Average iteration time      | 71.11 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T13:58:00.428792  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.02 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.84 %                    |
| RAM average               | 1054.01 MB (~1.03 GB) |
| GPU average               | 37.2 %                    |
| GPU Memory average        | 1475.39 MB (~1.44 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9975 (~100 % of real-time) |
| Average iteration time      | 69.03 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world</summary>

**Timestamp:** 2025-10-23T13:44:03.468444  
**Total iterations:** 3  
**Average measured duration per iteration:** 5.64 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.03 %                    |
| RAM average               | 842.92 MB (~0.82 GB) |
| GPU average               | 30.9 %                    |
| GPU Memory average        | 2128.68 MB (~2.08 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8308 (~83 % of real-time) |
| Average iteration time      | 66.71 s        |

> Simulation runs at ~83 % of real-time (1 s simulated → 1.2 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T13:52:26.956760  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.12 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.72 %                    |
| RAM average               | 1030.25 MB (~1.01 GB) |
| GPU average               | 33.9 %                    |
| GPU Memory average        | 3153.33 MB (~3.08 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.3300 (~133 % of real-time) |
| Average iteration time      | 69.03 s        |

> Simulation runs at ~133 % of real-time (1 s simulated → 0.8 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world</summary>

**Timestamp:** 2025-10-23T13:48:15.763674  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.21 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.16 %                    |
| RAM average               | 761.84 MB (~0.74 GB) |
| GPU average               | 19.8 %                    |
| GPU Memory average        | 1192.45 MB (~1.16 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.1662 (~17 % of real-time) |
| Average iteration time      | 67.57 s        |

> Simulation runs at ~17 % of real-time (1 s simulated → 6.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T13:56:36.047767  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.88 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.32 %                    |
| RAM average               | 1011.68 MB (~0.99 GB) |
| GPU average               | 42.6 %                    |
| GPU Memory average        | 1484.83 MB (~1.45 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.1661 (~17 % of real-time) |
| Average iteration time      | 69.01 s        |

> Simulation runs at ~17 % of real-time (1 s simulated → 6.0 s real).

</details>



## Simulator: webots

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_empty_world | 2.69 s | 0.99 | 993.32 MB | 0.98 % | 47.56 % | 1276.11 MB |
| two_robot_empty_world | 4.97 s | 1.00 | 1374.83 MB | 1.43 % | 36.71 % | 1323.43 MB |
| three_robot_empty_world | 8.87 s | 0.99 | 1762.23 MB | 1.90 % | 37.20 % | 1419.00 MB |
| one_robot_simple_world | 3.22 s | 1.23 | 1160.54 MB | 3.26 % | 21.85 % | 3499.03 MB |
| two_robot_simple_world | 5.16 s | 0.99 | 1412.51 MB | 1.42 % | 42.17 % | 1351.00 MB |
| three_robot_simple_world | 9.50 s | 0.99 | 1781.45 MB | 1.95 % | 38.80 % | 1456.20 MB |
| one_robot_empty_world_rviz | 3.74 s | 1.00 | 1482.22 MB | 4.51 % | 27.00 % | 3876.00 MB |
| two_robot_empty_world_rviz | 5.31 s | 1.00 | 2657.68 MB | 16.42 % | 63.00 % | 6649.00 MB |
| three_robot_empty_world_rviz | 9.14 s | 0.66 | 4121.18 MB | 27.99 % | 73.25 % | 9469.50 MB |
| one_robot_simple_world_rviz | 4.03 s | 0.99 | 1561.07 MB | 4.67 % | 34.12 % | 3897.50 MB |
| two_robot_simple_world_rviz | 5.31 s | 1.10 | 2779.23 MB | 16.67 % | 62.80 % | 6683.20 MB |
| three_robot_simple_world_rviz | 9.40 s | 0.60 | 4250.25 MB | 27.97 % | 70.60 % | 9528.40 MB |
| one_robot_empty_world_headless | 2.69 s | 0.99 | 1114.49 MB | 0.58 % | 15.56 % | 1238.89 MB |
| two_robot_empty_world_headless | 5.39 s | 0.89 | 1426.08 MB | 0.94 % | 7.50 % | 1357.00 MB |
| three_robot_empty_world_headless | 8.07 s | 0.99 | 1807.27 MB | 1.52 % | 4.80 % | 1470.00 MB |
| one_robot_simple_world_headless | 2.96 s | 0.99 | 1123.97 MB | 0.68 % | 15.33 % | 1311.00 MB |
| two_robot_simple_world_headless | 6.30 s | 0.99 | 1507.44 MB | 1.06 % | 14.33 % | 1434.33 MB |
| three_robot_simple_world_headless | 8.89 s | 0.93 | 1898.32 MB | 1.63 % | 3.20 % | 1548.00 MB |
| one_robot_empty_world_rviz_headless | 3.06 s | 0.80 | 1488.37 MB | 4.83 % | 25.50 % | 3919.88 MB |
| two_robot_empty_world_rviz_headless | 6.06 s | 1.00 | 2726.97 MB | 16.75 % | 63.00 % | 6759.83 MB |
| three_robot_empty_world_rviz_headless | 8.61 s | 0.66 | 4159.96 MB | 27.99 % | 69.00 % | 9618.75 MB |
| one_robot_simple_world_rviz_headless | 3.06 s | 0.80 | 1607.62 MB | 4.71 % | 25.25 % | 4000.25 MB |
| two_robot_simple_world_rviz_headless | 5.21 s | 1.00 | 2764.15 MB | 16.93 % | 62.00 % | 6832.00 MB |
| three_robot_simple_world_rviz_headless | 8.88 s | 0.60 | 4255.22 MB | 27.95 % | 71.25 % | 9613.75 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world</summary>

**Timestamp:** 2025-10-22T17:04:28.124232  
**Total iterations:** 1  
**Average measured duration per iteration:** 2.69 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 0.98 %                    |
| RAM average               | 993.32 MB (~0.97 GB) |
| GPU average               | 47.6 %                    |
| GPU Memory average        | 1276.11 MB (~1.25 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9881 (~99 % of real-time) |
| Average iteration time      | 68.00 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-22T17:21:59.205523  
**Total iterations:** 1  
**Average measured duration per iteration:** 2.69 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 0.58 %                    |
| RAM average               | 1114.49 MB (~1.09 GB) |
| GPU average               | 15.6 %                    |
| GPU Memory average        | 1238.89 MB (~1.21 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9920 (~99 % of real-time) |
| Average iteration time      | 68.06 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T17:13:13.860559  
**Total iterations:** 1  
**Average measured duration per iteration:** 3.74 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.51 %                    |
| RAM average               | 1482.22 MB (~1.45 GB) |
| GPU average               | 27.0 %                    |
| GPU Memory average        | 3876.00 MB (~3.79 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9953 (~100 % of real-time) |
| Average iteration time      | 64.83 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-22T17:30:42.136482  
**Total iterations:** 1  
**Average measured duration per iteration:** 3.06 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.83 %                    |
| RAM average               | 1488.37 MB (~1.45 GB) |
| GPU average               | 25.5 %                    |
| GPU Memory average        | 3919.88 MB (~3.83 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7957 (~80 % of real-time) |
| Average iteration time      | 64.81 s        |

> Simulation runs at ~80 % of real-time (1 s simulated → 1.3 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-10-22T17:08:54.540932  
**Total iterations:** 11  
**Average measured duration per iteration:** 3.22 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 3.26 %                    |
| RAM average               | 1160.54 MB (~1.13 GB) |
| GPU average               | 21.8 %                    |
| GPU Memory average        | 3499.03 MB (~3.42 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.2327 (~123 % of real-time) |
| Average iteration time      | 66.83 s        |

> Simulation runs at ~123 % of real-time (1 s simulated → 0.8 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-22T17:26:17.810893  
**Total iterations:** 1  
**Average measured duration per iteration:** 2.96 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 0.68 %                    |
| RAM average               | 1123.97 MB (~1.10 GB) |
| GPU average               | 15.3 %                    |
| GPU Memory average        | 1311.00 MB (~1.28 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9915 (~99 % of real-time) |
| Average iteration time      | 68.06 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T17:17:32.901098  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.03 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.67 %                    |
| RAM average               | 1561.07 MB (~1.52 GB) |
| GPU average               | 34.1 %                    |
| GPU Memory average        | 3897.50 MB (~3.81 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9950 (~99 % of real-time) |
| Average iteration time      | 69.86 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-22T17:35:01.162362  
**Total iterations:** 1  
**Average measured duration per iteration:** 3.06 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.71 %                    |
| RAM average               | 1607.62 MB (~1.57 GB) |
| GPU average               | 25.2 %                    |
| GPU Memory average        | 4000.25 MB (~3.91 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7972 (~80 % of real-time) |
| Average iteration time      | 64.83 s        |

> Simulation runs at ~80 % of real-time (1 s simulated → 1.3 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world</summary>

**Timestamp:** 2025-10-22T17:07:33.717588  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.87 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.90 %                    |
| RAM average               | 1762.23 MB (~1.72 GB) |
| GPU average               | 37.2 %                    |
| GPU Memory average        | 1419.00 MB (~1.39 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9925 (~99 % of real-time) |
| Average iteration time      | 80.44 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-22T17:24:54.382312  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.07 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.52 %                    |
| RAM average               | 1807.27 MB (~1.76 GB) |
| GPU average               | 4.8 %                    |
| GPU Memory average        | 1470.00 MB (~1.44 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9938 (~99 % of real-time) |
| Average iteration time      | 76.49 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T17:16:07.700584  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.14 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 27.99 %                    |
| RAM average               | 4121.18 MB (~4.02 GB) |
| GPU average               | 73.2 %                    |
| GPU Memory average        | 9469.50 MB (~9.25 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6639 (~66 % of real-time) |
| Average iteration time      | 69.34 s        |

> Simulation runs at ~66 % of real-time (1 s simulated → 1.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-22T17:33:40.993448  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.61 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 27.99 %                    |
| RAM average               | 4159.96 MB (~4.06 GB) |
| GPU average               | 69.0 %                    |
| GPU Memory average        | 9618.75 MB (~9.39 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6636 (~66 % of real-time) |
| Average iteration time      | 74.33 s        |

> Simulation runs at ~66 % of real-time (1 s simulated → 1.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world</summary>

**Timestamp:** 2025-10-22T17:11:53.680999  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.50 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.95 %                    |
| RAM average               | 1781.45 MB (~1.74 GB) |
| GPU average               | 38.8 %                    |
| GPU Memory average        | 1456.20 MB (~1.42 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9925 (~99 % of real-time) |
| Average iteration time      | 76.46 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-22T17:29:21.980534  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.89 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.63 %                    |
| RAM average               | 1898.32 MB (~1.85 GB) |
| GPU average               | 3.2 %                    |
| GPU Memory average        | 1548.00 MB (~1.51 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9277 (~93 % of real-time) |
| Average iteration time      | 80.50 s        |

> Simulation runs at ~93 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T17:20:35.790530  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.40 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 27.97 %                    |
| RAM average               | 4250.25 MB (~4.15 GB) |
| GPU average               | 70.6 %                    |
| GPU Memory average        | 9528.40 MB (~9.31 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5972 (~60 % of real-time) |
| Average iteration time      | 83.87 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-22T17:38:00.042279  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.88 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 27.95 %                    |
| RAM average               | 4255.22 MB (~4.16 GB) |
| GPU average               | 71.2 %                    |
| GPU Memory average        | 9613.75 MB (~9.39 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5972 (~60 % of real-time) |
| Average iteration time      | 74.33 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world</summary>

**Timestamp:** 2025-10-22T17:05:57.927295  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.97 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.43 %                    |
| RAM average               | 1374.83 MB (~1.34 GB) |
| GPU average               | 36.7 %                    |
| GPU Memory average        | 1323.43 MB (~1.29 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9973 (~100 % of real-time) |
| Average iteration time      | 74.46 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-22T17:23:22.536683  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.39 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 0.94 %                    |
| RAM average               | 1426.08 MB (~1.39 GB) |
| GPU average               | 7.5 %                    |
| GPU Memory average        | 1357.00 MB (~1.33 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8932 (~89 % of real-time) |
| Average iteration time      | 67.98 s        |

> Simulation runs at ~89 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T17:14:43.046861  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.31 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 16.42 %                    |
| RAM average               | 2657.68 MB (~2.60 GB) |
| GPU average               | 63.0 %                    |
| GPU Memory average        | 6649.00 MB (~6.49 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9968 (~100 % of real-time) |
| Average iteration time      | 73.83 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-22T17:32:11.319151  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.06 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 16.75 %                    |
| RAM average               | 2726.97 MB (~2.66 GB) |
| GPU average               | 63.0 %                    |
| GPU Memory average        | 6759.83 MB (~6.60 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9954 (~100 % of real-time) |
| Average iteration time      | 73.83 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world</summary>

**Timestamp:** 2025-10-22T17:10:21.845350  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.16 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.42 %                    |
| RAM average               | 1412.51 MB (~1.38 GB) |
| GPU average               | 42.2 %                    |
| GPU Memory average        | 1351.00 MB (~1.32 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9936 (~99 % of real-time) |
| Average iteration time      | 71.95 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-22T17:27:46.138953  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.30 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.06 %                    |
| RAM average               | 1507.44 MB (~1.47 GB) |
| GPU average               | 14.3 %                    |
| GPU Memory average        | 1434.33 MB (~1.40 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9926 (~99 % of real-time) |
| Average iteration time      | 72.98 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T17:18:56.550108  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.31 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 16.67 %                    |
| RAM average               | 2779.23 MB (~2.71 GB) |
| GPU average               | 62.8 %                    |
| GPU Memory average        | 6683.20 MB (~6.53 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.0957 (~110 % of real-time) |
| Average iteration time      | 68.30 s        |

> Simulation runs at ~110 % of real-time (1 s simulated → 0.9 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-22T17:36:30.364227  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.21 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 16.93 %                    |
| RAM average               | 2764.15 MB (~2.70 GB) |
| GPU average               | 62.0 %                    |
| GPU Memory average        | 6832.00 MB (~6.67 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9966 (~100 % of real-time) |
| Average iteration time      | 73.85 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>

