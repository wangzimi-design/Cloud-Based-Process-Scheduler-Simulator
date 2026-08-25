import heapq
from tasks import Task, Container

def sjf_scheduler(tasks, num_containers=3):
    containers = [Container(f"container_{i}") for i in range(num_containers)]
    ready_queue = []
    task_index = 0
    total_tasks = len(tasks)
    completed_tasks = []
    current_time = 0
    
    sorted_tasks = sorted(tasks, key=lambda x: x.arrival_time)
    
    while task_index < total_tasks or ready_queue or any(container.current_task for container in containers):
        # Add arriving tasks to ready queue
        while task_index < total_tasks and sorted_tasks[task_index].arrival_time <= current_time:
            task = sorted_tasks[task_index]
            heapq.heappush(ready_queue, (task.burst_time, task_index, task))
            task_index += 1
        
        # Assign tasks to free containers
        for container in containers:
            if not container.current_task and ready_queue:
                _, _, task = heapq.heappop(ready_queue)
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