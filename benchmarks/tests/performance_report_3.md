# 📊 Performance Report (all simulators and categories)

## Simulator: isaac_sim

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_empty_world | 11.43 s | 1.20 | 4957.83 MB | 31.93 % | 59.00 % | 5220.69 MB |
| two_robot_empty_world | 0.00 s | 1.00 | 4265.10 MB | 89.38 % | 4.65 % | 1677.65 MB |
| three_robot_empty_world | 11.96 s | 0.60 | 5621.45 MB | 37.91 % | 79.18 % | 6501.43 MB |
| one_robot_simple_world | 11.23 s | 0.99 | 4971.86 MB | 37.52 % | 73.39 % | 5172.18 MB |
| two_robot_simple_world | 11.73 s | 0.80 | 5331.66 MB | 44.56 % | 83.86 % | 5905.18 MB |
| three_robot_simple_world | 12.12 s | 0.40 | 5670.27 MB | 51.59 % | 76.63 % | 6563.53 MB |
| one_robot_empty_world_rviz | 11.46 s | 0.80 | 5259.83 MB | 44.00 % | 65.73 % | 7397.20 MB |
| two_robot_empty_world_rviz | 11.32 s | 0.80 | 5662.81 MB | 43.15 % | 82.02 % | 8051.49 MB |
| three_robot_empty_world_rviz | 11.97 s | 0.40 | 6058.27 MB | 45.45 % | 68.56 % | 8700.88 MB |
| one_robot_simple_world_rviz | 11.12 s | 0.80 | 5260.01 MB | 49.95 % | 70.80 % | 7403.63 MB |
| two_robot_simple_world_rviz | 11.26 s | 0.40 | 5670.08 MB | 47.75 % | 75.56 % | 8097.66 MB |
| three_robot_simple_world_rviz | 12.70 s | 0.60 | 6044.09 MB | 43.42 % | 83.31 % | 8630.86 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world</summary>

**Timestamp:** 2025-10-22T11:34:49.287410  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.43 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 31.93 %                    |
| RAM average               | 4957.83 MB (~4.84 GB) |
| GPU average               | 59.0 %                    |
| GPU Memory average        | 5220.69 MB (~5.10 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.1952 (~120 % of real-time) |
| Average iteration time      | 103.09 s        |

> Simulation runs at ~120 % of real-time (1 s simulated → 0.8 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T11:49:00.095690  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.46 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 44.00 %                    |
| RAM average               | 5259.83 MB (~5.14 GB) |
| GPU average               | 65.7 %                    |
| GPU Memory average        | 7397.20 MB (~7.22 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7955 (~80 % of real-time) |
| Average iteration time      | 102.78 s        |

> Simulation runs at ~80 % of real-time (1 s simulated → 1.3 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-10-22T11:42:03.890161  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.23 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 37.52 %                    |
| RAM average               | 4971.86 MB (~4.86 GB) |
| GPU average               | 73.4 %                    |
| GPU Memory average        | 5172.18 MB (~5.05 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9939 (~99 % of real-time) |
| Average iteration time      | 103.01 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T11:55:56.057465  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.12 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 49.95 %                    |
| RAM average               | 5260.01 MB (~5.14 GB) |
| GPU average               | 70.8 %                    |
| GPU Memory average        | 7403.63 MB (~7.23 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7958 (~80 % of real-time) |
| Average iteration time      | 102.81 s        |

> Simulation runs at ~80 % of real-time (1 s simulated → 1.3 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world</summary>

**Timestamp:** 2025-10-22T11:39:45.063307  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.96 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 37.91 %                    |
| RAM average               | 5621.45 MB (~5.49 GB) |
| GPU average               | 79.2 %                    |
| GPU Memory average        | 6501.43 MB (~6.35 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5971 (~60 % of real-time) |
| Average iteration time      | 102.97 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T11:53:37.406161  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.97 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 45.45 %                    |
| RAM average               | 6058.27 MB (~5.92 GB) |
| GPU average               | 68.6 %                    |
| GPU Memory average        | 8700.88 MB (~8.50 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.3985 (~40 % of real-time) |
| Average iteration time      | 102.83 s        |

> Simulation runs at ~40 % of real-time (1 s simulated → 2.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world</summary>

**Timestamp:** 2025-10-22T11:46:41.480334  
**Total iterations:** 1  
**Average measured duration per iteration:** 12.12 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 51.59 %                    |
| RAM average               | 5670.27 MB (~5.54 GB) |
| GPU average               | 76.6 %                    |
| GPU Memory average        | 6563.53 MB (~6.41 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.3982 (~40 % of real-time) |
| Average iteration time      | 102.97 s        |

> Simulation runs at ~40 % of real-time (1 s simulated → 2.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T12:00:35.710479  
**Total iterations:** 1  
**Average measured duration per iteration:** 12.70 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 43.42 %                    |
| RAM average               | 6044.09 MB (~5.90 GB) |
| GPU average               | 83.3 %                    |
| GPU Memory average        | 8630.86 MB (~8.43 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5972 (~60 % of real-time) |
| Average iteration time      | 105.23 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world</summary>

**Timestamp:** 2025-10-22T11:37:26.262522  
**Total iterations:** 1  
**Average measured duration per iteration:** 0.00 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 89.38 %                    |
| RAM average               | 4265.10 MB (~4.17 GB) |
| GPU average               | 4.7 %                    |
| GPU Memory average        | 1677.65 MB (~1.64 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.0000 (~100 % of real-time) |
| Average iteration time      | 121.14 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T11:51:18.735572  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.32 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 43.15 %                    |
| RAM average               | 5662.81 MB (~5.53 GB) |
| GPU average               | 82.0 %                    |
| GPU Memory average        | 8051.49 MB (~7.86 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7961 (~80 % of real-time) |
| Average iteration time      | 102.79 s        |

> Simulation runs at ~80 % of real-time (1 s simulated → 1.3 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world</summary>

**Timestamp:** 2025-10-22T11:44:22.681876  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.73 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 44.56 %                    |
| RAM average               | 5331.66 MB (~5.21 GB) |
| GPU average               | 83.9 %                    |
| GPU Memory average        | 5905.18 MB (~5.77 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.7963 (~80 % of real-time) |
| Average iteration time      | 102.95 s        |

> Simulation runs at ~80 % of real-time (1 s simulated → 1.3 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T11:58:14.631251  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.26 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 47.75 %                    |
| RAM average               | 5670.08 MB (~5.54 GB) |
| GPU average               | 75.6 %                    |
| GPU Memory average        | 8097.66 MB (~7.91 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.3984 (~40 % of real-time) |
| Average iteration time      | 102.75 s        |

> Simulation runs at ~40 % of real-time (1 s simulated → 2.5 s real).

</details>



## Simulator: webots

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_simple_world | 3.24 s | 1.26 | 1170.36 MB | 3.49 % | 19.71 % | 3725.33 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-09-18T16:41:41.574716  
**Total iterations:** 10  
**Average measured duration per iteration:** 3.24 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 3.49 %                    |
| RAM average               | 1170.36 MB (~1.14 GB) |
| GPU average               | 19.7 %                    |
| GPU Memory average        | 3725.33 MB (~3.64 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.2570 (~126 % of real-time) |
| Average iteration time      | 66.97 s        |

> Simulation runs at ~126 % of real-time (1 s simulated → 0.8 s real).

</details>

