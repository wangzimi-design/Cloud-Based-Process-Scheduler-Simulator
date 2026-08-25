# Cloud-Based Process Scheduler Simulator (Core Engine)

**Authors:** Ziming Wang, Shuxin Sun  
**Advisor:** Hamza Djigal  
**Institution:** Department of Computer Science, Wenzhou-Kean University (WKU)  
**Cloud Demo:** [cloudscheduler.onrender.com](https://cloudscheduler.onrender.com)

---

## 📌 Project Overview

This repository houses the core scheduling engine and backend services for the **Cloud-Based Process Scheduler Simulator**. 

This system transitions a traditional local process scheduler into a production-like **cloud-powered web service**. Using a stack of **Python (Flask), React, Docker, and Render**, the simulator generates virtual tasks within containerized environments, computes comprehensive performance metrics, and visualizes scheduling results (including Gantt charts) via an interactive web interface.

---

## 🛠️ Tech Stack & System Architecture

### 1. Backend Engine (Flask & Python)
*   Implements the core logic for 5 classic Operating System scheduling algorithms.
*   Exposes lightweight REST APIs to receive user inputs (or automated simulation parameters) and returns computed metrics as JSON.
*   Handles task simulation and Gantt chart data generation.

### 2. Front-End Interface (React)
*   Presents real-time scheduler simulations, user-defined inputs, and performance charts.
*   Integrates with the Flask backend through built React assets (`npm build` outputs placed directly inside the Flask directory).

### 3. Containerization & Cloud Deployment (Docker & Render)
*   **Docker**: Packages the application into containerized environments to automate task isolation and simulate realistic environments.
*   **Render**: Deploys the production runtime with CI/CD integration, upgrading the project from a local "pseudo-cloud" to a fully scalable cloud infrastructure with global URL access.

---

## 🚀 Supported Scheduling Algorithms & Metrics

### Implemented Algorithms
*   **FCFS** (First-Come, First-Served): Simple non-preemptive queue-based scheduling.
*   **SJF** (Shortest Job First): Non-preemptive, minimizes average waiting time.
*   **SRTF** (Shortest Remaining Time First): Preemptive variant of SJF, ideal for dynamic environments.
*   **RR** (Round Robin): Time-slice (quantum) cyclic preemptive scheduling ensuring fairness.
*   **Priority**: Allocates execution time according to task urgency/priority levels.

### Computed Performance Metrics
*   **Turnaround Time (TAT)**: The interval from task arrival to completion.
*   **Waiting Time (WT)**: The total time a process spends waiting in the ready queue.
*   **CPU Utilization**: Measures the efficiency of CPU usage during task execution.

---

## 📂 Backend File Structure

```text
python_demo/
├── algorithms/               # Implementation of scheduling algorithms
│   ├── __init__.py           # Package marker
│   ├── fcfs.py               # First-Come, First-Served algorithm
│   ├── sjf.py                # Shortest Job First / SRTF
│   ├── priority.py           # Priority-based scheduler
│   └── round_robin.py        # Round Robin algorithm
├── test_scheduler.py         # Unit tests for core scheduler coordination
├── test_algorithms.py        # Unit tests for individual algorithms
├── test_tasks.py             # Unit tests for task validation
├── scheduler.py              # Main simulation scheduler controller
├── tasks.py                  # Defines Task classes & execution metadata
├── main.py                   # Local entry point for running core tests/simulations
└── hello.py                  # Quick environment verification script
