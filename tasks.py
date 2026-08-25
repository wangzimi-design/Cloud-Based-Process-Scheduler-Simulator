# tasks.py

class Task:
    def __init__(self, task_id, arrival_time, burst_time, priority=1):
        self.id = task_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.start_time = None
        self.completion_time = None
        self.container_id = None
    
    @property
    def turnaround_time(self):
        if self.completion_time:
            return self.completion_time - self.arrival_time
        return 0
    
    @property
    def waiting_time(self):
        if self.completion_time:
            return self.turnaround_time - self.burst_time
        return 0

class Container:
    def __init__(self, container_id, cpu_cores=1, memory=1024):
        self.id = container_id
        self.cpu_cores = cpu_cores
        self.memory = memory
        self.current_task = None
        self.utilization_history = []
        self.is_running = False