import random
import sys
import os

# Add algorithms directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithms'))

from fcfs import fcfs_scheduler
from sjf import sjf_scheduler
from priority import priority_scheduler
from round_robin import round_robin_scheduler
from tasks import Task, Container

class SchedulerSimulator:
    def __init__(self):
        self.tasks = []
        self.containers = []
        self.completed_tasks = []
        self.current_time = 0
        self.metrics = {}
    
    def generate_random_tasks(self, num_tasks=10):
        self.tasks = []
        for i in range(num_tasks):
            arrival_time = random.randint(0, 20)
            burst_time = random.randint(1, 10)
            priority = random.randint(1, 5)
            self.tasks.append(Task(f"task_{i}", arrival_time, burst_time, priority))
    
    def simulate(self, algorithm="FCFS", num_tasks=10, num_containers=3, time_quantum=2):
        self.generate_random_tasks(num_tasks)
        
        if algorithm == "FCFS":
            self.completed_tasks, self.containers, self.current_time = fcfs_scheduler(
                self.tasks, num_containers)
        elif algorithm == "SJF":
            self.completed_tasks, self.containers, self.current_time = sjf_scheduler(
                self.tasks, num_containers)
        elif algorithm == "PRIORITY":
            self.completed_tasks, self.containers, self.current_time = priority_scheduler(
                self.tasks, num_containers)
        elif algorithm == "RR":
            self.completed_tasks, self.containers, self.current_time = round_robin_scheduler(
                self.tasks, time_quantum, num_containers)
        
        return self.calculate_metrics()
    
    def calculate_metrics(self):
        total_turnaround = sum(task.turnaround_time for task in self.completed_tasks)
        total_waiting = sum(task.waiting_time for task in self.completed_tasks)
        avg_turnaround = total_turnaround / len(self.completed_tasks) if self.completed_tasks else 0
        avg_waiting = total_waiting / len(self.completed_tasks) if self.completed_tasks else 0
        
        # Calculate CPU utilization
        cpu_utilization = []
        for container in self.containers:
            if container.utilization_history:
                container_util = sum(container.utilization_history) / len(container.utilization_history)
                cpu_utilization.append(container_util)
        avg_cpu_utilization = sum(cpu_utilization) / len(cpu_utilization) if cpu_utilization else 0
        
        self.metrics = {
            "task_details": [
                {
                    "task_id": task.id,
                    "arrival_time": task.arrival_time,
                    "burst_time": task.burst_time,
                    "start_time": task.start_time,
                    "completion_time": task.completion_time,
                    "turnaround_time": task.turnaround_time,
                    "waiting_time": task.waiting_time,
                    "priority": task.priority
                } for task in self.completed_tasks
            ],
            "performance_metrics": {
                "avg_turnaround_time": round(avg_turnaround, 2),
                "avg_waiting_time": round(avg_waiting, 2),
                "avg_cpu_utilization": round(avg_cpu_utilization, 2),
                "total_completion_time": self.current_time
            },
            "container_status": [
                {
                    "container_id": container.id,
                    "cpu_utilization": round(sum(container.utilization_history) / len(container.utilization_history), 2) if container.utilization_history else 0
                } for container in self.containers
            ]
        }
        
        return self.metrics