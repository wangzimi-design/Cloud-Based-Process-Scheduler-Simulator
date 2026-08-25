from scheduler import SchedulerSimulator

def main():
    simulator = SchedulerSimulator()
    
    print("Cloud-Based Process Scheduler Simulator")
    print("=" * 50)
    
    # Test different algorithms
    algorithms = ["FCFS", "SJF", "PRIORITY", "RR"]
    
    for algo in algorithms:
        print(f"\nTesting {algo} Algorithm:")
        print("-" * 30)
        
        results = simulator.simulate(algorithm=algo, num_tasks=8, num_containers=2)
        
        metrics = results["performance_metrics"]
        print(f"Average Turnaround Time: {metrics['avg_turnaround_time']}")
        print(f"Average Waiting Time: {metrics['avg_waiting_time']}")
        print(f"Average CPU Utilization: {metrics['avg_cpu_utilization']}%")
        print(f"Total Completion Time: {metrics['total_completion_time']}")

if __name__ == "__main__":
    main()