# 📊 Performance Report (all simulators and categories)

## Simulator: isaac_sim

### Summary Table

| Category | Startup time (s) | RealTime Factor | RAM | CPU | GPU | GPU RAM |
|---|---|---|---|---|---|---|
| one_robot_empty_world | 11.25 s | 0.99 | 4521.31 MB | 29.46 % | 51.57 % | 4661.14 MB |
| two_robot_empty_world | 11.65 s | 1.00 | 4901.56 MB | 33.29 % | 70.52 % | 5105.33 MB |
| three_robot_empty_world | 0.00 s | 1.00 | 194.90 MB | 4.08 % | 6.75 % | 606.59 MB |
| one_robot_simple_world | 11.22 s | 0.99 | 4480.41 MB | 35.00 % | 61.71 % | 4554.48 MB |
| two_robot_simple_world | 11.70 s | 0.60 | 4799.97 MB | 42.75 % | 69.10 % | 5189.43 MB |
| three_robot_simple_world | 12.17 s | 0.60 | 5097.40 MB | 48.49 % | 62.82 % | 5728.64 MB |
| one_robot_empty_world_rviz | 11.22 s | 1.00 | 4837.73 MB | 43.93 % | 54.76 % | 6361.24 MB |
| two_robot_empty_world_rviz | 11.16 s | 0.40 | 5123.39 MB | 45.17 % | 59.00 % | 6888.82 MB |
| three_robot_empty_world_rviz | 11.53 s | 0.40 | 5437.59 MB | 43.16 % | 66.24 % | 7435.00 MB |
| one_robot_simple_world_rviz | 11.09 s | 0.60 | 4809.89 MB | 48.18 % | 58.47 % | 6363.65 MB |
| two_robot_simple_world_rviz | 11.28 s | 0.20 | 5134.00 MB | 46.20 % | 64.53 % | 6897.53 MB |
| three_robot_simple_world_rviz | 11.73 s | 0.60 | 5536.39 MB | 47.78 % | 71.59 % | 7468.12 MB |

<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world</summary>

**Timestamp:** 2025-10-22T10:26:16.714505  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.25 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 29.46 %                    |
| RAM average               | 4521.31 MB (~4.42 GB) |
| GPU average               | 51.6 %                    |
| GPU Memory average        | 4661.14 MB (~4.55 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9922 (~99 % of real-time) |
| Average iteration time      | 42.20 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T10:32:25.562966  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.22 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 43.93 %                    |
| RAM average               | 4837.73 MB (~4.72 GB) |
| GPU average               | 54.8 %                    |
| GPU Memory average        | 6361.24 MB (~6.21 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9958 (~100 % of real-time) |
| Average iteration time      | 42.12 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world</summary>

**Timestamp:** 2025-10-22T10:29:59.543209  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.22 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 35.00 %                    |
| RAM average               | 4480.41 MB (~4.38 GB) |
| GPU average               | 61.7 %                    |
| GPU Memory average        | 4554.48 MB (~4.45 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9945 (~99 % of real-time) |
| Average iteration time      | 42.26 s        |

> Simulation runs at ~99 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: one_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T10:34:49.572441  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.09 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 48.18 %                    |
| RAM average               | 4809.89 MB (~4.70 GB) |
| GPU average               | 58.5 %                    |
| GPU Memory average        | 6363.65 MB (~6.21 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5971 (~60 % of real-time) |
| Average iteration time      | 42.16 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world</summary>

**Timestamp:** 2025-10-22T10:29:11.464503  
**Total iterations:** 1  
**Average measured duration per iteration:** 0.00 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 4.08 %                    |
| RAM average               | 194.90 MB (~0.19 GB) |
| GPU average               | 6.8 %                    |
| GPU Memory average        | 606.59 MB (~0.59 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 1.0000 (~100 % of real-time) |
| Average iteration time      | 120.95 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T10:34:01.590257  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.53 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 43.16 %                    |
| RAM average               | 5437.59 MB (~5.31 GB) |
| GPU average               | 66.2 %                    |
| GPU Memory average        | 7435.00 MB (~7.26 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.3982 (~40 % of real-time) |
| Average iteration time      | 42.15 s        |

> Simulation runs at ~40 % of real-time (1 s simulated → 2.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world</summary>

**Timestamp:** 2025-10-22T10:31:37.626238  
**Total iterations:** 1  
**Average measured duration per iteration:** 12.17 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 48.49 %                    |
| RAM average               | 5097.40 MB (~4.98 GB) |
| GPU average               | 62.8 %                    |
| GPU Memory average        | 5728.64 MB (~5.59 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5970 (~60 % of real-time) |
| Average iteration time      | 44.23 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: three_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T10:36:25.488378  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.73 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 47.78 %                    |
| RAM average               | 5536.39 MB (~5.41 GB) |
| GPU average               | 71.6 %                    |
| GPU Memory average        | 7468.12 MB (~7.29 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5956 (~60 % of real-time) |
| Average iteration time      | 42.15 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world</summary>

**Timestamp:** 2025-10-22T10:27:04.683697  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.65 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 33.29 %                    |
| RAM average               | 4901.56 MB (~4.79 GB) |
| GPU average               | 70.5 %                    |
| GPU Memory average        | 5105.33 MB (~4.99 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.9951 (~100 % of real-time) |
| Average iteration time      | 42.13 s        |

> Simulation runs at ~100 % of real-time (1 s simulated → 1.0 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_empty_world_rviz</summary>

**Timestamp:** 2025-10-22T10:33:13.613348  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.16 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 45.17 %                    |
| RAM average               | 5123.39 MB (~5.00 GB) |
| GPU average               | 59.0 %                    |
| GPU Memory average        | 6888.82 MB (~6.73 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.3982 (~40 % of real-time) |
| Average iteration time      | 42.23 s        |

> Simulation runs at ~40 % of real-time (1 s simulated → 2.5 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world</summary>

**Timestamp:** 2025-10-22T10:30:47.582082  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.70 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 42.75 %                    |
| RAM average               | 4799.97 MB (~4.69 GB) |
| GPU average               | 69.1 %                    |
| GPU Memory average        | 5189.43 MB (~5.07 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.5975 (~60 % of real-time) |
| Average iteration time      | 42.21 s        |

> Simulation runs at ~60 % of real-time (1 s simulated → 1.7 s real).

</details>


<details>
<summary style="font-size:1.25em; font-weight:bold;">Category: two_robot_simple_world_rviz</summary>

**Timestamp:** 2025-10-22T10:35:37.503406  
**Total iterations:** 1  
**Average measured duration per iteration:** 11.28 s  

#### System Resources

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| CPU average               | 46.20 %                    |
| RAM average               | 5134.00 MB (~5.01 GB) |
| GPU average               | 64.5 %                    |
| GPU Memory average        | 6897.53 MB (~6.74 GB) |

#### Simulation Performance

| Metric                    | Value                          |
|---------------------------|--------------------------------|
| Real Time Factor (RTF)     | 0.1991 (~20 % of real-time) |
| Average iteration time      | 42.11 s        |

> Simulation runs at ~20 % of real-time (1 s simulated → 5.0 s real).

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

