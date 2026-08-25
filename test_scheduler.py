import unittest
from unittest.mock import patch, MagicMock
from scheduler import SchedulerSimulator
from tasks import Task, Container

class TestSchedulerSimulator(unittest.TestCase):
    """测试SchedulerSimulator类的功能"""
    
    def setUp(self):
        """设置测试数据"""
        self.simulator = SchedulerSimulator()
        
    def test_initialization(self):
        """测试模拟器正确初始化"""
        self.assertEqual(self.simulator.tasks, [])
        self.assertEqual(self.simulator.containers, [])
        self.assertEqual(self.simulator.completed_tasks, [])
        self.assertEqual(self.simulator.current_time, 0)
        self.assertEqual(self.simulator.metrics, {})
    
    @patch('scheduler.random.randint')
    def test_generate_random_tasks(self, mock_randint):
        """测试随机任务生成"""
        # 模拟随机数生成器
        mock_randint.side_effect = [0, 5, 3, 1, 3, 2, 2, 4, 1]  # 3个任务的数据
        
        self.simulator.generate_random_tasks(3)
        
        # 验证任务数量
        self.assertEqual(len(self.simulator.tasks), 3)
        
        # 验证任务属性
        self.assertEqual(self.simulator.tasks[0].id, "task_0")
        self.assertEqual(self.simulator.tasks[0].arrival_time, 0)
        self.assertEqual(self.simulator.tasks[0].burst_time, 5)
        self.assertEqual(self.simulator.tasks[0].priority, 3)
        
        self.assertEqual(self.simulator.tasks[1].id, "task_1")
        self.assertEqual(self.simulator.tasks[1].arrival_time, 1)
        self.assertEqual(self.simulator.tasks[1].burst_time, 3)
        self.assertEqual(self.simulator.tasks[1].priority, 2)
        
        self.assertEqual(self.simulator.tasks[2].id, "task_2")
        self.assertEqual(self.simulator.tasks[2].arrival_time, 2)
        self.assertEqual(self.simulator.tasks[2].burst_time, 4)
        self.assertEqual(self.simulator.tasks[2].priority, 1)
    
    @patch('scheduler.random.randint')
    def test_generate_random_tasks_default_count(self, mock_randint):
        """测试默认任务数量生成"""
        # 模拟10个任务的数据
        mock_randint.side_effect = [i % 10 for i in range(30)]  # 10个任务需要30个随机数
        
        self.simulator.generate_random_tasks()  # 使用默认值10
        
        self.assertEqual(len(self.simulator.tasks), 10)
    
    @patch('scheduler.fcfs_scheduler')
    @patch('scheduler.random.randint')
    def test_simulate_fcfs_algorithm(self, mock_randint, mock_fcfs):
        """测试FCFS算法模拟"""
        # 模拟随机任务生成
        mock_randint.side_effect = [0, 5, 3, 1, 3, 2]
        
        # 模拟FCFS调度器返回结果
        mock_task = Task("mock_task", 0, 5, 1)
        mock_task.start_time = 0
        mock_task.completion_time = 5
        mock_container = Container("mock_container")
        mock_container.utilization_history = [100, 100, 100, 100, 100]
        
        mock_fcfs.return_value = ([mock_task], [mock_container], 5)
        
        # 执行模拟
        result = self.simulator.simulate(algorithm="FCFS", num_tasks=2, num_containers=1)
        
        # 验证FCFS调度器被调用
        mock_fcfs.assert_called_once()
        
        # 验证结果结构
        self.assertIn("task_details", result)
        self.assertIn("performance_metrics", result)
        self.assertIn("container_status", result)
    
    @patch('scheduler.sjf_scheduler')
    @patch('scheduler.random.randint')
    def test_simulate_sjf_algorithm(self, mock_randint, mock_sjf):
        """测试SJF算法模拟"""
        # 模拟随机任务生成
        mock_randint.side_effect = [0, 5, 3, 1, 3, 2]
        
        # 模拟SJF调度器返回结果
        mock_task = Task("mock_task", 0, 5, 1)
        mock_task.start_time = 0
        mock_task.completion_time = 5
        mock_container = Container("mock_container")
        mock_container.utilization_history = [100, 100, 100, 100, 100]
        
        mock_sjf.return_value = ([mock_task], [mock_container], 5)
        
        # 执行模拟
        result = self.simulator.simulate(algorithm="SJF", num_tasks=2, num_containers=1)
        
        # 验证SJF调度器被调用
        mock_sjf.assert_called_once()
        
        # 验证结果结构
        self.assertIn("performance_metrics", result)
    
    @patch('scheduler.priority_scheduler')
    @patch('scheduler.random.randint')
    def test_simulate_priority_algorithm(self, mock_randint, mock_priority):
        """测试优先级算法模拟"""
        # 模拟随机任务生成
        mock_randint.side_effect = [0, 5, 3, 1, 3, 2]
        
        # 模拟优先级调度器返回结果
        mock_task = Task("mock_task", 0, 5, 1)
        mock_task.start_time = 0
        mock_task.completion_time = 5
        mock_container = Container("mock_container")
        mock_container.utilization_history = [100, 100, 100, 100, 100]
        
        mock_priority.return_value = ([mock_task], [mock_container], 5)
        
        # 执行模拟
        result = self.simulator.simulate(algorithm="PRIORITY", num_tasks=2, num_containers=1)
        
        # 验证优先级调度器被调用
        mock_priority.assert_called_once()
    
    @patch('scheduler.round_robin_scheduler')
    @patch('scheduler.random.randint')
    def test_simulate_round_robin_algorithm(self, mock_randint, mock_rr):
        """测试轮转算法模拟"""
        # 模拟随机任务生成
        mock_randint.side_effect = [0, 5, 3, 1, 3, 2]
        
        # 模拟轮转调度器返回结果
        mock_task = Task("mock_task", 0, 5, 1)
        mock_task.start_time = 0
        mock_task.completion_time = 5
        mock_container = Container("mock_container")
        mock_container.utilization_history = [100, 100, 100, 100, 100]
        
        mock_rr.return_value = ([mock_task], [mock_container], 5)
        
        # 执行模拟
        result = self.simulator.simulate(algorithm="RR", num_tasks=2, num_containers=1, time_quantum=2)
        
        # 验证轮转调度器被调用
        mock_rr.assert_called_once()
    
    def test_calculate_metrics_empty_tasks(self):
        """测试空任务列表的指标计算"""
        self.simulator.completed_tasks = []
        self.simulator.containers = [Container("container_1")]
        self.simulator.current_time = 0
        
        result = self.simulator.calculate_metrics()
        
        # 验证性能指标
        metrics = result["performance_metrics"]
        self.assertEqual(metrics["avg_turnaround_time"], 0)
        self.assertEqual(metrics["avg_waiting_time"], 0)
        self.assertEqual(metrics["avg_cpu_utilization"], 0)
        self.assertEqual(metrics["total_completion_time"], 0)
        
        # 验证任务详情
        self.assertEqual(result["task_details"], [])
        
        # 验证容器状态
        self.assertEqual(len(result["container_status"]), 1)
    
    def test_calculate_metrics_with_tasks(self):
        """测试有任务时的指标计算"""
        # 创建已完成的任务
        task1 = Task("task_1", 0, 5, 1)
        task1.start_time = 0
        task1.completion_time = 5
        
        task2 = Task("task_2", 1, 3, 2)
        task2.start_time = 5
        task2.completion_time = 8
        
        self.simulator.completed_tasks = [task1, task2]
        
        # 创建容器
        container = Container("container_1")
        container.utilization_history = [100, 100, 100, 100, 100, 100, 100, 100]
        self.simulator.containers = [container]
        self.simulator.current_time = 8
        
        result = self.simulator.calculate_metrics()
        
        # 验证性能指标
        metrics = result["performance_metrics"]
        self.assertEqual(metrics["avg_turnaround_time"], 5.5)  # (5 + 7) / 2 = 6
        self.assertEqual(metrics["avg_waiting_time"], 2.5)    # (0 + 5) / 2 = 2.5
        self.assertEqual(metrics["avg_cpu_utilization"], 100.0)
        self.assertEqual(metrics["total_completion_time"], 8)
        
        # 验证任务详情
        self.assertEqual(len(result["task_details"]), 2)
        
        # 验证容器状态
        self.assertEqual(result["container_status"][0]["cpu_utilization"], 100.0)
    
    def test_calculate_metrics_multiple_containers(self):
        """测试多容器时的指标计算"""
        # 创建任务
        task = Task("task_1", 0, 5, 1)
        task.start_time = 0
        task.completion_time = 5
        self.simulator.completed_tasks = [task]
        
        # 创建多个容器
        container1 = Container("container_1")
        container1.utilization_history = [100, 100, 100, 0, 0]
        
        container2 = Container("container_2")
        container2.utilization_history = [0, 0, 0, 100, 100]
        
        self.simulator.containers = [container1, container2]
        self.simulator.current_time = 5
        
        result = self.simulator.calculate_metrics()
        
        # 验证平均CPU利用率
        metrics = result["performance_metrics"]
        self.assertEqual(metrics["avg_cpu_utilization"], 60.0)  # (60 + 40) / 2 = 50
    
    def test_calculate_metrics_no_utilization_history(self):
        """测试无利用率历史时的指标计算"""
        task = Task("task_1", 0, 5, 1)
        task.start_time = 0
        task.completion_time = 5
        self.simulator.completed_tasks = [task]
        
        container = Container("container_1")
        container.utilization_history = []  # 空利用率历史
        self.simulator.containers = [container]
        self.simulator.current_time = 5
        
        result = self.simulator.calculate_metrics()
        
        metrics = result["performance_metrics"]
        self.assertEqual(metrics["avg_cpu_utilization"], 0)

class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_simulate_invalid_algorithm(self):
        """测试无效算法名称"""
        simulator = SchedulerSimulator()
        
        # 应该使用默认算法（FCFS）
        result = simulator.simulate(algorithm="INVALID", num_tasks=2)
        
        # 验证结果结构
        self.assertIn("performance_metrics", result)
    
    def test_simulate_zero_tasks(self):
        """测试零任务模拟"""
        simulator = SchedulerSimulator()
        
        result = simulator.simulate(num_tasks=0)
        
        metrics = result["performance_metrics"]
        self.assertEqual(metrics["avg_turnaround_time"], 0)
        self.assertEqual(metrics["avg_waiting_time"], 0)
        self.assertEqual(metrics["total_completion_time"], 0)
    
    def test_simulate_zero_containers(self):
        """测试零容器模拟"""
        simulator = SchedulerSimulator()
        
        # 零容器应该使用默认值
        result = simulator.simulate(num_containers=0)
        
        # 验证结果结构
        self.assertIn("performance_metrics", result)

if __name__ == "__main__":
    unittest.main()