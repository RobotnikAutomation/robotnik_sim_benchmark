# 📊 Performance Report (all simulators and categories)

## Simulator: gazebo_harmonic

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_empty_world | 5.11 s | 1.00 | 2428.85 MB | 17.25 % | 37.67 % | 1562.22 MB |
| two_robot_empty_world | 5.20 s | 1.00 | 2688.41 MB | 19.10 % | 24.38 % | 1719.38 MB |
| three_robot_empty_world | 8.11 s | 1.00 | 3003.28 MB | 19.90 % | 32.83 % | 1891.50 MB |
| one_robot_simple_world | 0.00 s | 1.00 | 1246.24 MB | 10.55 % | 22.35 % | 942.00 MB |
| two_robot_simple_world | 5.52 s | 0.70 | 2939.88 MB | 13.05 % | 39.50 % | 1716.25 MB |
| three_robot_simple_world | 0.00 s | 0.00 | 2486.16 MB | 12.71 % | 34.55 % | 1164.00 MB |
| one_robot_empty_world_rviz | 5.14 s | 0.99 | 2871.37 MB | 15.38 % | 26.00 % | 4092.22 MB |
| two_robot_empty_world_rviz | 5.76 s | 1.00 | 3541.31 MB | 19.96 % | 48.86 % | 6768.00 MB |
| three_robot_empty_world_rviz | 8.00 s | 0.60 | 4181.87 MB | 21.89 % | 61.00 % | 8582.67 MB |
| one_robot_simple_world_rviz | 5.10 s | 0.99 | 3105.83 MB | 14.98 % | 25.44 % | 4091.00 MB |
| two_robot_simple_world_rviz | 5.53 s | 1.00 | 3750.01 MB | 20.36 % | 50.86 % | 6895.29 MB |
| three_robot_simple_world_rviz | 8.21 s | 0.60 | 4534.53 MB | 24.06 % | 70.17 % | 9375.50 MB |
| one_robot_empty_world_headless | 6.07 s | 1.00 | 1475.46 MB | 9.20 % | 39.00 % | 1173.00 MB |
| two_robot_empty_world_headless | 5.21 s | 1.00 | 1734.20 MB | 13.98 % | 35.89 % | 1336.44 MB |
| three_robot_empty_world_headless | 0.00 s | 0.00 | 1288.55 MB | 0.50 % | 0.67 % | 780.00 MB |
| one_robot_simple_world_headless | 6.74 s | 0.99 | 1472.36 MB | 9.56 % | 40.17 % | 1129.08 MB |
| two_robot_simple_world_headless | 5.85 s | 1.00 | 1804.95 MB | 13.68 % | 37.00 % | 1330.33 MB |
| three_robot_simple_world_headless | 0.00 s | 0.07 | 2043.39 MB | 0.64 % | 1.09 % | 1327.00 MB |
| one_robot_empty_world_rviz_headless | 5.04 s | 1.00 | 1884.38 MB | 10.43 % | 23.60 % | 3631.00 MB |
| two_robot_empty_world_rviz_headless | 5.51 s | 0.90 | 2570.25 MB | 14.37 % | 41.50 % | 6241.25 MB |
| three_robot_empty_world_rviz_headless | 8.20 s | 0.66 | 3400.41 MB | 22.29 % | 63.17 % | 9074.33 MB |
| one_robot_simple_world_rviz_headless | 5.04 s | 1.00 | 1996.23 MB | 10.25 % | 22.80 % | 3675.40 MB |
| two_robot_simple_world_rviz_headless | 6.06 s | 1.00 | 2676.82 MB | 15.86 % | 46.25 % | 6404.75 MB |
| three_robot_simple_world_rviz_headless | 8.13 s | 0.53 | 3393.15 MB | 19.51 % | 59.67 % | 8794.33 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world</summary>

**Timestamp:** 2025-10-23T18:30:21.383737  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.11 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 17.25 %                    |
| RAM average               | 2428.85 MB (~2.37 GB) |
| GPU average               | 37.7 %                    |
| GPU Memory average        | 1562.22 MB (~1.53 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9955 (~100 % of real-time) |
| Average iteration time      | 66.02 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-23T18:49:37.469555  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.07 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 9.20 %                    |
| RAM average               | 1475.46 MB (~1.44 GB) |
| GPU average               | 39.0 %                    |
| GPU Memory average        | 1173.00 MB (~1.15 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9963 (~100 % of real-time) |
| Average iteration time      | 68.50 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T18:40:57.457897  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.14 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 15.38 %                    |
| RAM average               | 2871.37 MB (~2.80 GB) |
| GPU average               | 26.0 %                    |
| GPU Memory average        | 4092.22 MB (~4.00 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9933 (~99 % of real-time) |
| Average iteration time      | 71.43 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T18:59:56.944286  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.04 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 10.43 %                    |
| RAM average               | 1884.38 MB (~1.84 GB) |
| GPU average               | 23.6 %                    |
| GPU Memory average        | 3631.00 MB (~3.55 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9957 (~100 % of real-time) |
| Average iteration time      | 65.94 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-10-23T18:35:37.093606  
**Total iterations:** 1  
**Average measured duration per iteration:** 0.00 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 10.55 %                    |
| RAM average               | 1246.24 MB (~1.22 GB) |
| GPU average               | 22.4 %                    |
| GPU Memory average        | 942.00 MB (~0.92 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.0000 (~100 % of real-time) |
| Average iteration time      | 121.76 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-23T18:54:53.778532  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.74 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 9.56 %                    |
| RAM average               | 1472.36 MB (~1.44 GB) |
| GPU average               | 40.2 %                    |
| GPU Memory average        | 1129.08 MB (~1.10 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9944 (~99 % of real-time) |
| Average iteration time      | 69.39 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T18:45:14.148561  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.10 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 14.98 %                    |
| RAM average               | 3105.83 MB (~3.03 GB) |
| GPU average               | 25.4 %                    |
| GPU Memory average        | 4091.00 MB (~4.00 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9944 (~99 % of real-time) |
| Average iteration time      | 70.45 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T19:04:13.571819  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.04 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 10.25 %                    |
| RAM average               | 1996.23 MB (~1.95 GB) |
| GPU average               | 22.8 %                    |
| GPU Memory average        | 3675.40 MB (~3.59 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9964 (~100 % of real-time) |
| Average iteration time      | 66.78 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world</summary>

**Timestamp:** 2025-10-23T18:33:19.969210  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.11 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 19.90 %                    |
| RAM average               | 3003.28 MB (~2.93 GB) |
| GPU average               | 32.8 %                    |
| GPU Memory average        | 1891.50 MB (~1.85 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9965 (~100 % of real-time) |
| Average iteration time      | 75.42 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-23T18:53:29.035634  
**Total iterations:** 1  
**Average measured duration per iteration:** 0.00 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 0.50 %                    |
| RAM average               | 1288.55 MB (~1.26 GB) |
| GPU average               | 0.7 %                    |
| GPU Memory average        | 780.00 MB (~0.76 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.0000 (~0 % of real-time) |
| Average iteration time      | 129.40 s        |

> Simulation runs at ~0 % of real-time (1 s simulated → inf s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T18:43:48.343870  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.00 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 21.89 %                    |
| RAM average               | 4181.87 MB (~4.08 GB) |
| GPU average               | 61.0 %                    |
| GPU Memory average        | 8582.67 MB (~8.38 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5982 (~60 % of real-time) |
| Average iteration time      | 70.46 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T19:02:51.419754  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.20 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 22.29 %                    |
| RAM average               | 3400.41 MB (~3.32 GB) |
| GPU average               | 63.2 %                    |
| GPU Memory average        | 9074.33 MB (~8.86 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6635 (~66 % of real-time) |
| Average iteration time      | 71.87 s        |

> Simulation runs at ~66 % of real-time (1 s simulated → 1.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world</summary>

**Timestamp:** 2025-10-23T18:39:30.673201  
**Total iterations:** 1  
**Average measured duration per iteration:** 0.00 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 12.71 %                    |
| RAM average               | 2486.16 MB (~2.43 GB) |
| GPU average               | 34.5 %                    |
| GPU Memory average        | 1164.00 MB (~1.14 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.0000 (~0 % of real-time) |
| Average iteration time      | 130.94 s        |

> Simulation runs at ~0 % of real-time (1 s simulated → inf s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-23T18:58:35.651083  
**Total iterations:** 1  
**Average measured duration per iteration:** 0.00 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 0.64 %                    |
| RAM average               | 2043.39 MB (~2.00 GB) |
| GPU average               | 1.1 %                    |
| GPU Memory average        | 1327.00 MB (~1.30 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.0663 (~7 % of real-time) |
| Average iteration time      | 121.37 s        |

> Simulation runs at ~7 % of real-time (1 s simulated → 15.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T18:48:13.609918  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.21 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 24.06 %                    |
| RAM average               | 4534.53 MB (~4.43 GB) |
| GPU average               | 70.2 %                    |
| GPU Memory average        | 9375.50 MB (~9.16 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5983 (~60 % of real-time) |
| Average iteration time      | 77.38 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T19:07:08.575749  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.13 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 19.51 %                    |
| RAM average               | 3393.15 MB (~3.31 GB) |
| GPU average               | 59.7 %                    |
| GPU Memory average        | 8794.33 MB (~8.59 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5320 (~53 % of real-time) |
| Average iteration time      | 71.87 s        |

> Simulation runs at ~53 % of real-time (1 s simulated → 1.9 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world</summary>

**Timestamp:** 2025-10-23T18:31:49.193024  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.20 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 19.10 %                    |
| RAM average               | 2688.41 MB (~2.63 GB) |
| GPU average               | 24.4 %                    |
| GPU Memory average        | 1719.38 MB (~1.68 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9969 (~100 % of real-time) |
| Average iteration time      | 72.44 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-23T18:51:04.273792  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.21 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 13.98 %                    |
| RAM average               | 1734.20 MB (~1.69 GB) |
| GPU average               | 35.9 %                    |
| GPU Memory average        | 1336.44 MB (~1.31 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9951 (~100 % of real-time) |
| Average iteration time      | 71.46 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T18:42:22.525698  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.76 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 19.96 %                    |
| RAM average               | 3541.31 MB (~3.46 GB) |
| GPU average               | 48.9 %                    |
| GPU Memory average        | 6768.00 MB (~6.61 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9972 (~100 % of real-time) |
| Average iteration time      | 69.70 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T19:01:24.188471  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.51 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 14.37 %                    |
| RAM average               | 2570.25 MB (~2.51 GB) |
| GPU average               | 41.5 %                    |
| GPU Memory average        | 6241.25 MB (~6.09 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8958 (~90 % of real-time) |
| Average iteration time      | 71.89 s        |

> Simulation runs at ~90 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world</summary>

**Timestamp:** 2025-10-23T18:37:04.378059  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.52 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 13.05 %                    |
| RAM average               | 2939.88 MB (~2.87 GB) |
| GPU average               | 39.5 %                    |
| GPU Memory average        | 1716.25 MB (~1.68 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6978 (~70 % of real-time) |
| Average iteration time      | 71.91 s        |

> Simulation runs at ~70 % of real-time (1 s simulated → 1.4 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-23T18:56:18.917613  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.85 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 13.68 %                    |
| RAM average               | 1804.95 MB (~1.76 GB) |
| GPU average               | 37.0 %                    |
| GPU Memory average        | 1330.33 MB (~1.30 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9966 (~100 % of real-time) |
| Average iteration time      | 69.78 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T18:46:40.870561  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.53 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 20.36 %                    |
| RAM average               | 3750.01 MB (~3.66 GB) |
| GPU average               | 50.9 %                    |
| GPU Memory average        | 6895.29 MB (~6.73 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9973 (~100 % of real-time) |
| Average iteration time      | 71.37 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T19:05:41.332458  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.06 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 15.86 %                    |
| RAM average               | 2676.82 MB (~2.61 GB) |
| GPU average               | 46.2 %                    |
| GPU Memory average        | 6404.75 MB (~6.25 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9969 (~100 % of real-time) |
| Average iteration time      | 72.41 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>



## Simulator: isaac_sim

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_empty_world | 11.31 s | 1.00 | 4819.79 MB | 30.55 % | 56.97 % | 5143.69 MB |
| two_robot_empty_world | 12.03 s | 1.00 | 5140.30 MB | 37.52 % | 76.06 % | 5723.53 MB |
| three_robot_empty_world | 12.16 s | 0.60 | 5469.31 MB | 38.49 % | 75.89 % | 6359.44 MB |
| one_robot_simple_world | 11.84 s | 0.59 | 4863.17 MB | 38.90 % | 67.39 % | 5130.61 MB |
| two_robot_simple_world | 12.05 s | 0.60 | 5169.67 MB | 46.32 % | 75.67 % | 5816.78 MB |
| three_robot_simple_world | 12.48 s | 0.60 | 5512.47 MB | 49.81 % | 70.22 % | 6403.22 MB |
| one_robot_empty_world_rviz | 11.52 s | 0.80 | 5123.83 MB | 40.41 % | 61.24 % | 7204.07 MB |
| two_robot_empty_world_rviz | 12.09 s | 0.40 | 5509.06 MB | 45.64 % | 62.97 % | 7813.59 MB |
| three_robot_empty_world_rviz | 12.40 s | 0.60 | 5869.67 MB | 39.62 % | 73.66 % | 8362.72 MB |
| one_robot_simple_world_rviz | 11.65 s | 1.00 | 5183.99 MB | 49.79 % | 65.34 % | 7209.79 MB |
| two_robot_simple_world_rviz | 11.50 s | 0.60 | 5514.60 MB | 45.08 % | 77.52 % | 7898.93 MB |
| three_robot_simple_world_rviz | 12.37 s | 0.60 | 5880.84 MB | 41.94 % | 78.03 % | 8450.48 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world</summary>

**Timestamp:** 2025-10-23T19:43:55.675313  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.31 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 30.55 %                    |
| RAM average               | 4819.79 MB (~4.71 GB) |
| GPU average               | 57.0 %                    |
| GPU Memory average        | 5143.69 MB (~5.02 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9964 (~100 % of real-time) |
| Average iteration time      | 72.70 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T19:52:43.534333  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.52 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 40.41 %                    |
| RAM average               | 5123.83 MB (~5.00 GB) |
| GPU average               | 61.2 %                    |
| GPU Memory average        | 7204.07 MB (~7.04 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7964 (~80 % of real-time) |
| Average iteration time      | 72.45 s        |

> Simulation runs at ~80 % of real-time (1 s simulated → 1.3 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-10-23T19:48:19.632068  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.84 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 38.90 %                    |
| RAM average               | 4863.17 MB (~4.75 GB) |
| GPU average               | 67.4 %                    |
| GPU Memory average        | 5130.61 MB (~5.01 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5949 (~59 % of real-time) |
| Average iteration time      | 72.54 s        |

> Simulation runs at ~59 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T19:57:07.174689  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.65 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 49.79 %                    |
| RAM average               | 5183.99 MB (~5.06 GB) |
| GPU average               | 65.3 %                    |
| GPU Memory average        | 7209.79 MB (~7.04 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9951 (~100 % of real-time) |
| Average iteration time      | 72.55 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world</summary>

**Timestamp:** 2025-10-23T19:46:51.744977  
**Total iterations:** 1  
**Average measured duration per iteration:** 12.16 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 38.49 %                    |
| RAM average               | 5469.31 MB (~5.34 GB) |
| GPU average               | 75.9 %                    |
| GPU Memory average        | 6359.44 MB (~6.21 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5969 (~60 % of real-time) |
| Average iteration time      | 72.68 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T19:55:39.265828  
**Total iterations:** 1  
**Average measured duration per iteration:** 12.40 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 39.62 %                    |
| RAM average               | 5869.67 MB (~5.73 GB) |
| GPU average               | 73.7 %                    |
| GPU Memory average        | 8362.72 MB (~8.17 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5971 (~60 % of real-time) |
| Average iteration time      | 72.49 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world</summary>

**Timestamp:** 2025-10-23T19:51:15.704067  
**Total iterations:** 1  
**Average measured duration per iteration:** 12.48 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 49.81 %                    |
| RAM average               | 5512.47 MB (~5.38 GB) |
| GPU average               | 70.2 %                    |
| GPU Memory average        | 6403.22 MB (~6.25 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5979 (~60 % of real-time) |
| Average iteration time      | 72.67 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T20:00:03.004517  
**Total iterations:** 1  
**Average measured duration per iteration:** 12.37 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 41.94 %                    |
| RAM average               | 5880.84 MB (~5.74 GB) |
| GPU average               | 78.0 %                    |
| GPU Memory average        | 8450.48 MB (~8.25 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5977 (~60 % of real-time) |
| Average iteration time      | 72.54 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world</summary>

**Timestamp:** 2025-10-23T19:45:23.708164  
**Total iterations:** 1  
**Average measured duration per iteration:** 12.03 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 37.52 %                    |
| RAM average               | 5140.30 MB (~5.02 GB) |
| GPU average               | 76.1 %                    |
| GPU Memory average        | 5723.53 MB (~5.59 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9960 (~100 % of real-time) |
| Average iteration time      | 72.67 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T19:54:11.415022  
**Total iterations:** 1  
**Average measured duration per iteration:** 12.09 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 45.64 %                    |
| RAM average               | 5509.06 MB (~5.38 GB) |
| GPU average               | 63.0 %                    |
| GPU Memory average        | 7813.59 MB (~7.63 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.3979 (~40 % of real-time) |
| Average iteration time      | 72.53 s        |

> Simulation runs at ~40 % of real-time (1 s simulated → 2.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world</summary>

**Timestamp:** 2025-10-23T19:49:47.665988  
**Total iterations:** 1  
**Average measured duration per iteration:** 12.05 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 46.32 %                    |
| RAM average               | 5169.67 MB (~5.05 GB) |
| GPU average               | 75.7 %                    |
| GPU Memory average        | 5816.78 MB (~5.68 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5979 (~60 % of real-time) |
| Average iteration time      | 72.67 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T19:58:35.103500  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.50 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 45.08 %                    |
| RAM average               | 5514.60 MB (~5.39 GB) |
| GPU average               | 77.5 %                    |
| GPU Memory average        | 7898.93 MB (~7.71 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5978 (~60 % of real-time) |
| Average iteration time      | 72.57 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>



## Simulator: o3de

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_empty_world | 10.48 s | 1.35 | 1880.00 MB | 3.25 % | 13.00 % | 1536.00 MB |
| two_robot_empty_world | 11.81 s | 1.05 | 1605.96 MB | 3.83 % | 3.00 % | 1990.00 MB |
| three_robot_empty_world | 11.80 s | 1.00 | 4016.21 MB | 6.41 % | 30.00 % | 2705.00 MB |
| one_robot_simple_world | 9.24 s | 0.85 | 1899.28 MB | 3.50 % | 11.50 % | 1624.50 MB |
| two_robot_simple_world | 11.01 s | 0.80 | 2918.75 MB | 4.16 % | 23.00 % | 2442.00 MB |
| three_robot_simple_world | 11.19 s | 0.90 | 3987.55 MB | 6.33 % | 23.00 % | 3611.00 MB |
| one_robot_empty_world_rviz | 10.10 s | 1.00 | 1879.93 MB | 4.04 % | 8.00 % | 1430.50 MB |
| two_robot_empty_world_rviz | 10.06 s | 1.17 | 2669.93 MB | 4.25 % | 14.50 % | 2394.00 MB |
| three_robot_empty_world_rviz | 10.75 s | 0.73 | 4013.82 MB | 6.41 % | 34.00 % | 3292.00 MB |
| one_robot_simple_world_rviz | 9.29 s | 1.10 | 1891.71 MB | 2.75 % | 12.50 % | 1676.50 MB |
| two_robot_simple_world_rviz | 9.77 s | 1.07 | 1642.56 MB | 3.91 % | 4.00 % | 2007.00 MB |
| three_robot_simple_world_rviz | 10.23 s | 1.13 | 4009.11 MB | 6.16 % | 31.00 % | 3446.00 MB |
| one_robot_empty_world_headless | 9.28 s | 1.00 | 1892.45 MB | 3.29 % | 12.00 % | 1612.00 MB |
| two_robot_empty_world_headless | 9.75 s | 0.75 | 1952.70 MB | 4.33 % | 16.00 % | 1978.00 MB |
| three_robot_empty_world_headless | 8.89 s | 1.00 | 4192.43 MB | 6.08 % | 23.00 % | 3265.00 MB |
| one_robot_simple_world_headless | 8.14 s | 1.00 | 1895.26 MB | 2.46 % | 10.50 % | 1619.00 MB |
| two_robot_simple_world_headless | 9.58 s | 0.97 | 1970.97 MB | 4.33 % | 21.00 % | 2420.00 MB |
| three_robot_simple_world_headless | 10.43 s | 1.00 | 4094.24 MB | 6.08 % | 23.00 % | 3024.00 MB |
| one_robot_empty_world_rviz_headless | 8.54 s | 0.99 | 1901.71 MB | 2.79 % | 9.50 % | 1669.50 MB |
| two_robot_empty_world_rviz_headless | 9.50 s | 1.02 | 2729.25 MB | 4.70 % | 16.00 % | 2472.00 MB |
| three_robot_empty_world_rviz_headless | 10.35 s | 1.10 | 4009.37 MB | 6.24 % | 35.00 % | 3485.00 MB |
| one_robot_simple_world_rviz_headless | 9.02 s | 0.90 | 2610.98 MB | 3.25 % | 15.67 % | 1956.67 MB |
| two_robot_simple_world_rviz_headless | 9.36 s | 0.65 | 2753.01 MB | 4.75 % | 15.50 % | 2481.00 MB |
| three_robot_simple_world_rviz_headless | 10.12 s | 1.16 | 4196.49 MB | 7.24 % | 29.00 % | 3715.00 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world</summary>

**Timestamp:** 2025-10-24T10:46:42.168696  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.48 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 3.25 %                    |
| RAM average               | 1880.00 MB (~1.84 GB) |
| GPU average               | 13.0 %                    |
| GPU Memory average        | 1536.00 MB (~1.50 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.3454 (~135 % of real-time) |
| Average iteration time      | 74.40 s        |

> Simulation runs at ~135 % of real-time (1 s simulated → 0.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-24T11:04:33.261757  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.28 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 3.29 %                    |
| RAM average               | 1892.45 MB (~1.85 GB) |
| GPU average               | 12.0 %                    |
| GPU Memory average        | 1612.00 MB (~1.57 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9962 (~100 % of real-time) |
| Average iteration time      | 71.95 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-24T10:55:41.474218  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.10 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.04 %                    |
| RAM average               | 1879.93 MB (~1.84 GB) |
| GPU average               | 8.0 %                    |
| GPU Memory average        | 1430.50 MB (~1.40 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9952 (~100 % of real-time) |
| Average iteration time      | 72.88 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-24T11:13:23.048290  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.54 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 2.79 %                    |
| RAM average               | 1901.71 MB (~1.86 GB) |
| GPU average               | 9.5 %                    |
| GPU Memory average        | 1669.50 MB (~1.63 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9943 (~99 % of real-time) |
| Average iteration time      | 71.44 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-10-24T10:51:12.806671  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.24 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 3.50 %                    |
| RAM average               | 1899.28 MB (~1.85 GB) |
| GPU average               | 11.5 %                    |
| GPU Memory average        | 1624.50 MB (~1.59 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8462 (~85 % of real-time) |
| Average iteration time      | 71.92 s        |

> Simulation runs at ~85 % of real-time (1 s simulated → 1.2 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-24T11:08:56.117256  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.14 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 2.46 %                    |
| RAM average               | 1895.26 MB (~1.85 GB) |
| GPU average               | 10.5 %                    |
| GPU Memory average        | 1619.00 MB (~1.58 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9958 (~100 % of real-time) |
| Average iteration time      | 71.94 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-24T11:00:08.593569  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.29 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 2.75 %                    |
| RAM average               | 1891.71 MB (~1.85 GB) |
| GPU average               | 12.5 %                    |
| GPU Memory average        | 1676.50 MB (~1.64 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.0958 (~110 % of real-time) |
| Average iteration time      | 71.48 s        |

> Simulation runs at ~110 % of real-time (1 s simulated → 0.9 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-24T11:17:51.577769  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.02 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 3.25 %                    |
| RAM average               | 2610.98 MB (~2.55 GB) |
| GPU average               | 15.7 %                    |
| GPU Memory average        | 1956.67 MB (~1.91 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8961 (~90 % of real-time) |
| Average iteration time      | 73.98 s        |

> Simulation runs at ~90 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world</summary>

**Timestamp:** 2025-10-24T10:49:45.521299  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.80 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.41 %                    |
| RAM average               | 4016.21 MB (~3.92 GB) |
| GPU average               | 30.0 %                    |
| GPU Memory average        | 2705.00 MB (~2.64 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9976 (~100 % of real-time) |
| Average iteration time      | 75.63 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-24T11:07:28.801879  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.89 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.08 %                    |
| RAM average               | 4192.43 MB (~4.09 GB) |
| GPU average               | 23.0 %                    |
| GPU Memory average        | 3265.00 MB (~3.19 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9977 (~100 % of real-time) |
| Average iteration time      | 71.32 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-24T10:58:41.736880  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.75 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.41 %                    |
| RAM average               | 4013.82 MB (~3.92 GB) |
| GPU average               | 34.0 %                    |
| GPU Memory average        | 3292.00 MB (~3.21 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7312 (~73 % of real-time) |
| Average iteration time      | 73.93 s        |

> Simulation runs at ~73 % of real-time (1 s simulated → 1.4 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-24T11:16:22.243714  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.35 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.24 %                    |
| RAM average               | 4009.37 MB (~3.92 GB) |
| GPU average               | 35.0 %                    |
| GPU Memory average        | 3485.00 MB (~3.40 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.0970 (~110 % of real-time) |
| Average iteration time      | 73.40 s        |

> Simulation runs at ~110 % of real-time (1 s simulated → 0.9 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world</summary>

**Timestamp:** 2025-10-24T10:54:13.224849  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.19 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.33 %                    |
| RAM average               | 3987.55 MB (~3.89 GB) |
| GPU average               | 23.0 %                    |
| GPU Memory average        | 3611.00 MB (~3.53 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8967 (~90 % of real-time) |
| Average iteration time      | 75.65 s        |

> Simulation runs at ~90 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-24T11:11:56.222569  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.43 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.08 %                    |
| RAM average               | 4094.24 MB (~4.00 GB) |
| GPU average               | 23.0 %                    |
| GPU Memory average        | 3024.00 MB (~2.95 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9971 (~100 % of real-time) |
| Average iteration time      | 75.44 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-24T11:03:05.939863  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.23 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.16 %                    |
| RAM average               | 4009.11 MB (~3.92 GB) |
| GPU average               | 31.0 %                    |
| GPU Memory average        | 3446.00 MB (~3.37 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.1304 (~113 % of real-time) |
| Average iteration time      | 73.78 s        |

> Simulation runs at ~113 % of real-time (1 s simulated → 0.9 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-24T11:20:50.729286  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.12 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.24 %                    |
| RAM average               | 4196.49 MB (~4.10 GB) |
| GPU average               | 29.0 %                    |
| GPU Memory average        | 3715.00 MB (~3.63 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.1625 (~116 % of real-time) |
| Average iteration time      | 73.29 s        |

> Simulation runs at ~116 % of real-time (1 s simulated → 0.9 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world</summary>

**Timestamp:** 2025-10-24T10:48:14.519343  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.81 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 3.83 %                    |
| RAM average               | 1605.96 MB (~1.57 GB) |
| GPU average               | 3.0 %                    |
| GPU Memory average        | 1990.00 MB (~1.94 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.0464 (~105 % of real-time) |
| Average iteration time      | 76.98 s        |

> Simulation runs at ~105 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-24T11:06:02.097350  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.75 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.33 %                    |
| RAM average               | 1952.70 MB (~1.91 GB) |
| GPU average               | 16.0 %                    |
| GPU Memory average        | 1978.00 MB (~1.93 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7479 (~75 % of real-time) |
| Average iteration time      | 73.46 s        |

> Simulation runs at ~75 % of real-time (1 s simulated → 1.3 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-24T10:57:12.410609  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.06 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.25 %                    |
| RAM average               | 2669.93 MB (~2.61 GB) |
| GPU average               | 14.5 %                    |
| GPU Memory average        | 2394.00 MB (~2.34 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.1717 (~117 % of real-time) |
| Average iteration time      | 75.57 s        |

> Simulation runs at ~117 % of real-time (1 s simulated → 0.9 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-24T11:14:53.487047  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.50 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.70 %                    |
| RAM average               | 2729.25 MB (~2.67 GB) |
| GPU average               | 16.0 %                    |
| GPU Memory average        | 2472.00 MB (~2.41 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.0219 (~102 % of real-time) |
| Average iteration time      | 75.08 s        |

> Simulation runs at ~102 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world</summary>

**Timestamp:** 2025-10-24T10:52:42.170966  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.01 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.16 %                    |
| RAM average               | 2918.75 MB (~2.85 GB) |
| GPU average               | 23.0 %                    |
| GPU Memory average        | 2442.00 MB (~2.38 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7973 (~80 % of real-time) |
| Average iteration time      | 73.98 s        |

> Simulation runs at ~80 % of real-time (1 s simulated → 1.3 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-24T11:10:25.416314  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.58 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.33 %                    |
| RAM average               | 1970.97 MB (~1.92 GB) |
| GPU average               | 21.0 %                    |
| GPU Memory average        | 2420.00 MB (~2.36 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9721 (~97 % of real-time) |
| Average iteration time      | 73.95 s        |

> Simulation runs at ~97 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-24T11:01:36.792449  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.77 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 3.91 %                    |
| RAM average               | 1642.56 MB (~1.60 GB) |
| GPU average               | 4.0 %                    |
| GPU Memory average        | 2007.00 MB (~1.96 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.0717 (~107 % of real-time) |
| Average iteration time      | 72.82 s        |

> Simulation runs at ~107 % of real-time (1 s simulated → 0.9 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-24T11:19:22.061029  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.36 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.75 %                    |
| RAM average               | 2753.01 MB (~2.69 GB) |
| GPU average               | 15.5 %                    |
| GPU Memory average        | 2481.00 MB (~2.42 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6480 (~65 % of real-time) |
| Average iteration time      | 75.11 s        |

> Simulation runs at ~65 % of real-time (1 s simulated → 1.5 s real).

</details>



## Simulator: unity

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_empty_world | 4.07 s | 1.99 | 789.36 MB | 6.43 % | 37.63 % | 1067.05 MB |
| two_robot_empty_world | 7.19 s | 0.17 | 777.25 MB | 6.46 % | 19.70 % | 1081.20 MB |
| three_robot_empty_world | 6.97 s | 1.11 | 811.14 MB | 6.10 % | 14.45 % | 1110.00 MB |
| one_robot_simple_world | 4.08 s | 0.33 | 817.69 MB | 6.11 % | 33.56 % | 1053.89 MB |
| two_robot_simple_world | 6.61 s | 0.17 | 768.77 MB | 6.14 % | 15.85 % | 1081.85 MB |
| three_robot_simple_world | 7.93 s | 0.11 | 817.81 MB | 6.15 % | 13.38 % | 1095.10 MB |
| one_robot_empty_world_rviz | 4.12 s | 1.33 | 1029.07 MB | 8.48 % | 45.53 % | 3420.59 MB |
| two_robot_empty_world_rviz | 7.29 s | 0.17 | 1123.77 MB | 7.76 % | 34.17 % | 2927.11 MB |
| three_robot_empty_world_rviz | 7.81 s | 8.07 | 1056.26 MB | 7.65 % | 29.61 % | 1382.44 MB |
| one_robot_simple_world_rviz | 4.53 s | 1.66 | 1096.06 MB | 7.90 % | 41.12 % | 3208.06 MB |
| two_robot_simple_world_rviz | 8.15 s | 0.17 | 1107.24 MB | 7.87 % | 28.00 % | 1522.47 MB |
| three_robot_simple_world_rviz | 8.94 s | 0.11 | 1203.64 MB | 7.58 % | 27.27 % | 1335.13 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world</summary>

**Timestamp:** 2025-10-23T20:01:35.221585  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.07 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.43 %                    |
| RAM average               | 789.36 MB (~0.77 GB) |
| GPU average               | 37.6 %                    |
| GPU Memory average        | 1067.05 MB (~1.04 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.9932 (~199 % of real-time) |
| Average iteration time      | 66.40 s        |

> Simulation runs at ~199 % of real-time (1 s simulated → 0.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T20:09:50.578324  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.12 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 8.48 %                    |
| RAM average               | 1029.07 MB (~1.00 GB) |
| GPU average               | 45.5 %                    |
| GPU Memory average        | 3420.59 MB (~3.34 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.3282 (~133 % of real-time) |
| Average iteration time      | 65.03 s        |

> Simulation runs at ~133 % of real-time (1 s simulated → 0.8 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-10-23T20:05:40.761351  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.08 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.11 %                    |
| RAM average               | 817.69 MB (~0.80 GB) |
| GPU average               | 33.6 %                    |
| GPU Memory average        | 1053.89 MB (~1.03 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.3321 (~33 % of real-time) |
| Average iteration time      | 64.27 s        |

> Simulation runs at ~33 % of real-time (1 s simulated → 3.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T20:13:59.777044  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.53 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.90 %                    |
| RAM average               | 1096.06 MB (~1.07 GB) |
| GPU average               | 41.1 %                    |
| GPU Memory average        | 3208.06 MB (~3.13 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.6608 (~166 % of real-time) |
| Average iteration time      | 65.03 s        |

> Simulation runs at ~166 % of real-time (1 s simulated → 0.6 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world</summary>

**Timestamp:** 2025-10-23T20:04:21.146756  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.97 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.10 %                    |
| RAM average               | 811.14 MB (~0.79 GB) |
| GPU average               | 14.4 %                    |
| GPU Memory average        | 1110.00 MB (~1.08 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.1084 (~111 % of real-time) |
| Average iteration time      | 67.63 s        |

> Simulation runs at ~111 % of real-time (1 s simulated → 0.9 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T20:12:39.392883  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.81 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.65 %                    |
| RAM average               | 1056.26 MB (~1.03 GB) |
| GPU average               | 29.6 %                    |
| GPU Memory average        | 1382.44 MB (~1.35 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 8.0702 (~807 % of real-time) |
| Average iteration time      | 69.06 s        |

> Simulation runs at ~807 % of real-time (1 s simulated → 0.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world</summary>

**Timestamp:** 2025-10-23T20:08:30.180899  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.93 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.15 %                    |
| RAM average               | 817.81 MB (~0.80 GB) |
| GPU average               | 13.4 %                    |
| GPU Memory average        | 1095.10 MB (~1.07 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.1108 (~11 % of real-time) |
| Average iteration time      | 71.12 s        |

> Simulation runs at ~11 % of real-time (1 s simulated → 9.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T20:16:51.983100  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.94 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.58 %                    |
| RAM average               | 1203.64 MB (~1.18 GB) |
| GPU average               | 27.3 %                    |
| GPU Memory average        | 1335.13 MB (~1.30 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.1109 (~11 % of real-time) |
| Average iteration time      | 70.38 s        |

> Simulation runs at ~11 % of real-time (1 s simulated → 9.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world</summary>

**Timestamp:** 2025-10-23T20:02:58.159655  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.19 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.46 %                    |
| RAM average               | 777.25 MB (~0.76 GB) |
| GPU average               | 19.7 %                    |
| GPU Memory average        | 1081.20 MB (~1.06 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.1663 (~17 % of real-time) |
| Average iteration time      | 67.59 s        |

> Simulation runs at ~17 % of real-time (1 s simulated → 6.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T20:11:14.970007  
**Total iterations:** 1  
**Average measured duration per iteration:** 7.29 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.76 %                    |
| RAM average               | 1123.77 MB (~1.10 GB) |
| GPU average               | 34.2 %                    |
| GPU Memory average        | 2927.11 MB (~2.86 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.1662 (~17 % of real-time) |
| Average iteration time      | 69.04 s        |

> Simulation runs at ~17 % of real-time (1 s simulated → 6.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world</summary>

**Timestamp:** 2025-10-23T20:07:03.700402  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.61 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 6.14 %                    |
| RAM average               | 768.77 MB (~0.75 GB) |
| GPU average               | 15.8 %                    |
| GPU Memory average        | 1081.85 MB (~1.06 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.1663 (~17 % of real-time) |
| Average iteration time      | 67.59 s        |

> Simulation runs at ~17 % of real-time (1 s simulated → 6.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T20:15:26.255925  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.15 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 7.87 %                    |
| RAM average               | 1107.24 MB (~1.08 GB) |
| GPU average               | 28.0 %                    |
| GPU Memory average        | 1522.47 MB (~1.49 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.1663 (~17 % of real-time) |
| Average iteration time      | 71.12 s        |

> Simulation runs at ~17 % of real-time (1 s simulated → 6.0 s real).

</details>



## Simulator: webots

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_empty_world | 3.69 s | 0.99 | 1017.07 MB | 1.02 % | 16.62 % | 1092.00 MB |
| two_robot_empty_world | 5.64 s | 0.99 | 1421.14 MB | 1.50 % | 16.67 % | 1211.00 MB |
| three_robot_empty_world | 9.09 s | 0.99 | 1856.74 MB | 2.15 % | 14.75 % | 1295.00 MB |
| one_robot_simple_world | 3.75 s | 0.99 | 1095.98 MB | 1.03 % | 16.38 % | 1126.00 MB |
| two_robot_simple_world | 6.16 s | 0.99 | 1490.63 MB | 1.53 % | 15.67 % | 1245.00 MB |
| three_robot_simple_world | 10.06 s | 0.99 | 1905.50 MB | 2.19 % | 14.75 % | 1342.00 MB |
| one_robot_empty_world_rviz | 3.88 s | 0.99 | 1508.20 MB | 4.87 % | 30.22 % | 3742.22 MB |
| two_robot_empty_world_rviz | 6.03 s | 0.90 | 2731.23 MB | 15.41 % | 60.20 % | 6534.20 MB |
| three_robot_empty_world_rviz | 8.64 s | 0.66 | 4231.24 MB | 28.32 % | 71.50 % | 9362.50 MB |
| one_robot_simple_world_rviz | 4.91 s | 1.00 | 1592.67 MB | 4.82 % | 22.86 % | 3781.43 MB |
| two_robot_simple_world_rviz | 6.08 s | 1.00 | 2835.26 MB | 15.54 % | 61.00 % | 6594.20 MB |
| three_robot_simple_world_rviz | 10.30 s | 0.66 | 4382.09 MB | 27.49 % | 70.00 % | 9435.00 MB |
| one_robot_empty_world_headless | 3.71 s | 0.99 | 1110.06 MB | 0.65 % | 3.62 % | 1143.00 MB |
| two_robot_empty_world_headless | 5.99 s | 0.89 | 1511.97 MB | 0.98 % | 1.80 % | 1255.00 MB |
| three_robot_empty_world_headless | 9.56 s | 0.93 | 1894.53 MB | 1.52 % | 1.00 % | 1374.00 MB |
| one_robot_simple_world_headless | 3.72 s | 0.99 | 1183.55 MB | 0.68 % | 3.50 % | 1214.00 MB |
| two_robot_simple_world_headless | 6.24 s | 0.89 | 1575.93 MB | 1.01 % | 2.17 % | 1333.00 MB |
| three_robot_simple_world_headless | 9.38 s | 0.99 | 1951.96 MB | 1.67 % | 1.20 % | 1452.00 MB |
| one_robot_empty_world_rviz_headless | 3.93 s | 0.99 | 1600.11 MB | 4.76 % | 29.22 % | 3791.56 MB |
| two_robot_empty_world_rviz_headless | 6.32 s | 1.00 | 2811.86 MB | 15.32 % | 59.00 % | 6591.40 MB |
| three_robot_empty_world_rviz_headless | 10.77 s | 0.66 | 4321.70 MB | 28.23 % | 70.00 % | 9463.33 MB |
| one_robot_simple_world_rviz_headless | 4.89 s | 1.00 | 1695.20 MB | 4.88 % | 21.00 % | 3889.78 MB |
| two_robot_simple_world_rviz_headless | 6.48 s | 0.99 | 2927.08 MB | 14.92 % | 62.60 % | 6675.20 MB |
| three_robot_simple_world_rviz_headless | 10.15 s | 0.66 | 4414.23 MB | 28.02 % | 71.67 % | 9587.33 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world</summary>

**Timestamp:** 2025-10-23T19:08:39.729500  
**Total iterations:** 1  
**Average measured duration per iteration:** 3.69 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.02 %                    |
| RAM average               | 1017.07 MB (~0.99 GB) |
| GPU average               | 16.6 %                    |
| GPU Memory average        | 1092.00 MB (~1.07 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9902 (~99 % of real-time) |
| Average iteration time      | 65.59 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-23T19:26:05.100789  
**Total iterations:** 1  
**Average measured duration per iteration:** 3.71 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 0.65 %                    |
| RAM average               | 1110.06 MB (~1.08 GB) |
| GPU average               | 3.6 %                    |
| GPU Memory average        | 1143.00 MB (~1.12 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9916 (~99 % of real-time) |
| Average iteration time      | 66.12 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T19:17:24.458239  
**Total iterations:** 1  
**Average measured duration per iteration:** 3.88 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.87 %                    |
| RAM average               | 1508.20 MB (~1.47 GB) |
| GPU average               | 30.2 %                    |
| GPU Memory average        | 3742.22 MB (~3.65 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9938 (~99 % of real-time) |
| Average iteration time      | 71.31 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T19:35:03.877253  
**Total iterations:** 1  
**Average measured duration per iteration:** 3.93 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.76 %                    |
| RAM average               | 1600.11 MB (~1.56 GB) |
| GPU average               | 29.2 %                    |
| GPU Memory average        | 3791.56 MB (~3.70 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9943 (~99 % of real-time) |
| Average iteration time      | 71.30 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-10-23T19:12:55.800454  
**Total iterations:** 1  
**Average measured duration per iteration:** 3.75 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.03 %                    |
| RAM average               | 1095.98 MB (~1.07 GB) |
| GPU average               | 16.4 %                    |
| GPU Memory average        | 1126.00 MB (~1.10 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9910 (~99 % of real-time) |
| Average iteration time      | 65.60 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-23T19:30:32.542456  
**Total iterations:** 1  
**Average measured duration per iteration:** 3.72 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 0.68 %                    |
| RAM average               | 1183.55 MB (~1.16 GB) |
| GPU average               | 3.5 %                    |
| GPU Memory average        | 1214.00 MB (~1.19 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9914 (~99 % of real-time) |
| Average iteration time      | 70.18 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T19:21:43.193489  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.91 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.82 %                    |
| RAM average               | 1592.67 MB (~1.56 GB) |
| GPU average               | 22.9 %                    |
| GPU Memory average        | 3781.43 MB (~3.69 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9965 (~100 % of real-time) |
| Average iteration time      | 65.37 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T19:39:25.463394  
**Total iterations:** 1  
**Average measured duration per iteration:** 4.89 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.88 %                    |
| RAM average               | 1695.20 MB (~1.66 GB) |
| GPU average               | 21.0 %                    |
| GPU Memory average        | 3889.78 MB (~3.80 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9958 (~100 % of real-time) |
| Average iteration time      | 71.29 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world</summary>

**Timestamp:** 2025-10-23T19:11:34.833871  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.09 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 2.15 %                    |
| RAM average               | 1856.74 MB (~1.81 GB) |
| GPU average               | 14.8 %                    |
| GPU Memory average        | 1295.00 MB (~1.26 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9940 (~99 % of real-time) |
| Average iteration time      | 76.93 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-23T19:29:07.008614  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.56 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.52 %                    |
| RAM average               | 1894.53 MB (~1.85 GB) |
| GPU average               | 1.0 %                    |
| GPU Memory average        | 1374.00 MB (~1.34 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9280 (~93 % of real-time) |
| Average iteration time      | 82.16 s        |

> Simulation runs at ~93 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T19:20:22.456883  
**Total iterations:** 1  
**Average measured duration per iteration:** 8.64 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 28.32 %                    |
| RAM average               | 4231.24 MB (~4.13 GB) |
| GPU average               | 71.5 %                    |
| GPU Memory average        | 9362.50 MB (~9.14 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6631 (~66 % of real-time) |
| Average iteration time      | 78.94 s        |

> Simulation runs at ~66 % of real-time (1 s simulated → 1.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T19:37:58.810148  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.77 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 28.23 %                    |
| RAM average               | 4321.70 MB (~4.22 GB) |
| GPU average               | 70.0 %                    |
| GPU Memory average        | 9463.33 MB (~9.24 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6636 (~66 % of real-time) |
| Average iteration time      | 73.39 s        |

> Simulation runs at ~66 % of real-time (1 s simulated → 1.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world</summary>

**Timestamp:** 2025-10-23T19:15:57.800308  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.06 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 2.19 %                    |
| RAM average               | 1905.50 MB (~1.86 GB) |
| GPU average               | 14.8 %                    |
| GPU Memory average        | 1342.00 MB (~1.31 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9944 (~99 % of real-time) |
| Average iteration time      | 78.11 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-23T19:33:37.216727  
**Total iterations:** 1  
**Average measured duration per iteration:** 9.38 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.67 %                    |
| RAM average               | 1951.96 MB (~1.91 GB) |
| GPU average               | 1.2 %                    |
| GPU Memory average        | 1452.00 MB (~1.42 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9945 (~99 % of real-time) |
| Average iteration time      | 81.47 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T19:24:43.625546  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.30 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 27.49 %                    |
| RAM average               | 4382.09 MB (~4.28 GB) |
| GPU average               | 70.0 %                    |
| GPU Memory average        | 9435.00 MB (~9.21 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6633 (~66 % of real-time) |
| Average iteration time      | 75.37 s        |

> Simulation runs at ~66 % of real-time (1 s simulated → 1.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T19:42:17.386262  
**Total iterations:** 1  
**Average measured duration per iteration:** 10.15 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 28.02 %                    |
| RAM average               | 4414.23 MB (~4.31 GB) |
| GPU average               | 71.7 %                    |
| GPU Memory average        | 9587.33 MB (~9.36 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.6637 (~66 % of real-time) |
| Average iteration time      | 72.90 s        |

> Simulation runs at ~66 % of real-time (1 s simulated → 1.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world</summary>

**Timestamp:** 2025-10-23T19:10:02.547634  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.64 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.50 %                    |
| RAM average               | 1421.14 MB (~1.39 GB) |
| GPU average               | 16.7 %                    |
| GPU Memory average        | 1211.00 MB (~1.18 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9929 (~99 % of real-time) |
| Average iteration time      | 67.44 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_headless</summary>

**Timestamp:** 2025-10-23T19:27:29.493814  
**Total iterations:** 1  
**Average measured duration per iteration:** 5.99 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 0.98 %                    |
| RAM average               | 1511.97 MB (~1.48 GB) |
| GPU average               | 1.8 %                    |
| GPU Memory average        | 1255.00 MB (~1.23 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8939 (~89 % of real-time) |
| Average iteration time      | 69.03 s        |

> Simulation runs at ~89 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-23T19:18:48.154193  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.03 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 15.41 %                    |
| RAM average               | 2731.23 MB (~2.67 GB) |
| GPU average               | 60.2 %                    |
| GPU Memory average        | 6534.20 MB (~6.38 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8968 (~90 % of real-time) |
| Average iteration time      | 68.34 s        |

> Simulation runs at ~90 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T19:36:30.062151  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.32 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 15.32 %                    |
| RAM average               | 2811.86 MB (~2.75 GB) |
| GPU average               | 59.0 %                    |
| GPU Memory average        | 6591.40 MB (~6.44 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9964 (~100 % of real-time) |
| Average iteration time      | 70.83 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world</summary>

**Timestamp:** 2025-10-23T19:14:24.339484  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.16 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.53 %                    |
| RAM average               | 1490.63 MB (~1.46 GB) |
| GPU average               | 15.7 %                    |
| GPU Memory average        | 1245.00 MB (~1.22 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9928 (~99 % of real-time) |
| Average iteration time      | 73.16 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_headless</summary>

**Timestamp:** 2025-10-23T19:32:00.379953  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.24 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 1.01 %                    |
| RAM average               | 1575.93 MB (~1.54 GB) |
| GPU average               | 2.2 %                    |
| GPU Memory average        | 1333.00 MB (~1.30 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.8943 (~89 % of real-time) |
| Average iteration time      | 72.47 s        |

> Simulation runs at ~89 % of real-time (1 s simulated → 1.1 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-23T19:23:12.885269  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.08 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 15.54 %                    |
| RAM average               | 2835.26 MB (~2.77 GB) |
| GPU average               | 61.0 %                    |
| GPU Memory average        | 6594.20 MB (~6.44 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9964 (~100 % of real-time) |
| Average iteration time      | 74.33 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz_headless</summary>

**Timestamp:** 2025-10-23T19:40:49.147151  
**Total iterations:** 1  
**Average measured duration per iteration:** 6.48 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 14.92 %                    |
| RAM average               | 2927.08 MB (~2.86 GB) |
| GPU average               | 62.6 %                    |
| GPU Memory average        | 6675.20 MB (~6.52 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9945 (~99 % of real-time) |
| Average iteration time      | 68.34 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>

