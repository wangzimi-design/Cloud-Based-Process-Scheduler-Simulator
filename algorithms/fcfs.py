from collections import deque
from tasks import Task, Container

def fcfs_scheduler(tasks, num_containers=3):
    containers = [Container(f"container_{i}") for i in range(num_containers)]
    ready_queue = deque(sorted(tasks, key=lambda x: x.arrival_time))
    completed_tasks = []
    current_time = 0
    
    while ready_queue or any(container.current_task for container in containers):
        # Assign tasks to free containers
        for container in containers:
            if not container.current_task and ready_queue and ready_queue[0].arrival_time <= current_time:
                task = ready_queue.popleft()
                task.start_time = current_time
                container.current_task = task
                container.is_running = True
        
        # Execute tasks
        for container in containers:
            if container.current_task:
                task = container.current_task
                task.remaining_time -= 1
                container.utilization_history.append(100)
                
                if task.remaining_time <= 0:
                    task.completion_time = current_time
                    completed_tasks.append(task)
                    container.current_task = None
                    container.is_running = False
            else:
                container.utilization_history.append(0)
        
        current_time += 1
    
    return completed_tasks, containers, current_time