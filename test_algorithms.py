import unittest
from tasks import Task, Container
from algorithms.fcfs import fcfs_scheduler
from algorithms.sjf import sjf_scheduler

class TestFCFSAlgorithm(unittest.TestCase):
    """测试FCFS调度算法"""
    
    def setUp(self):
        """设置测试数据"""
        self.tasks = [
            Task("task_1", 0, 5, 1),
            Task("task_2", 1, 3, 2),
            Task("task_3", 2, 8, 3)
        ]
    
    def test_fcfs_basic_functionality(self):
        """测试FCFS基本功能"""
        completed_tasks, containers, current_time = fcfs_scheduler(self.tasks, 2)
        
        # 验证任务完成
        self.assertEqual(len(completed_tasks), 3)
        
        # 验证任务按到达时间顺序执行
        self.assertEqual(completed_tasks[0].id, "task_1")
        self.assertEqual(completed_tasks[1].id, "task_2")
        self.assertEqual(completed_tasks[2].id, "task_3")
        
        # 验证容器数量
        self.assertEqual(len(containers), 2)
        
        # 验证时间推进
        self.assertGreater(current_time, 0)
    
    def test_fcfs_single_container(self):
        """测试单容器FCFS调度"""
        completed_tasks, containers, current_time = fcfs_scheduler(self.tasks, 1)
        
        self.assertEqual(len(containers), 1)
        self.assertEqual(len(completed_tasks), 3)
        
        # 验证任务顺序
        self.assertEqual(completed_tasks[0].id, "task_1")
        self.assertEqual(completed_tasks[1].id, "task_2")
        self.assertEqual(completed_tasks[2].id, "task_3")
    
    def test_fcfs_empty_tasks(self):
        """测试空任务列表"""
        completed_tasks, containers, current_time = fcfs_scheduler([], 2)
        
        self.assertEqual(len(completed_tasks), 0)
        self.assertEqual(len(containers), 2)
        self.assertEqual(current_time, 0)
    
    def test_fcfs_task_completion_times(self):
        """测试任务完成时间计算"""
        completed_tasks, containers, current_time = fcfs_scheduler(self.tasks, 2)
        
        for task in completed_tasks:
            self.assertIsNotNone(task.completion_time)
            self.assertIsNotNone(task.start_time)
            self.assertGreaterEqual(task.completion_time, task.start_time)
            self.assertGreaterEqual(task.turnaround_time, task.burst_time)
            self.assertGreaterEqual(task.waiting_time, 0)
    
    def test_fcfs_container_utilization(self):
        """测试容器利用率记录"""
        completed_tasks, containers, current_time = fcfs_scheduler(self.tasks, 2)
        
        for container in containers:
            self.assertEqual(len(container.utilization_history), current_time)
            # 利用率应该在0-100之间
            for utilization in container.utilization_history:
                self.assertGreaterEqual(utilization, 0)
                self.assertLessEqual(utilization, 100)

class TestSJFAlgorithm(unittest.TestCase):
    """测试SJF调度算法"""
    
    def setUp(self):
        """设置测试数据"""
        self.tasks = [
            Task("task_1", 0, 8, 1),  # 最长任务
            Task("task_2", 1, 3, 2),  # 最短任务
            Task("task_3", 2, 5, 3)   # 中等任务
        ]
    
    def test_sjf_basic_functionality(self):
        """测试SJF基本功能"""
        completed_tasks, containers, current_time = sjf_scheduler(self.tasks, 2)
        
        # 验证任务完成
        self.assertEqual(len(completed_tasks), 3)
        
        # 验证容器数量
        self.assertEqual(len(containers), 2)
        
        # 验证时间推进
        self.assertGreater(current_time, 0)
    
    def test_sjf_shortest_job_first(self):
        """测试最短作业优先原则"""
        # 创建同时到达的任务，验证SJF按作业长度排序
        tasks = [
            Task("task_1", 0, 8, 1),  # 最长
            Task("task_2", 0, 3, 2),  # 最短
            Task("task_3", 0, 5, 3)   # 中等
        ]
        
        completed_tasks, containers, current_time = sjf_scheduler(tasks, 2)
        
        # 最短任务应该先完成
        self.assertEqual(completed_tasks[0].id, "task_2")  # 最短任务
        self.assertEqual(completed_tasks[1].id, "task_3")  # 中等任务
        self.assertEqual(completed_tasks[2].id, "task_1")  # 最长任务
    
    def test_sjf_single_container(self):
        """测试单容器SJF调度"""
        completed_tasks, containers, current_time = sjf_scheduler(self.tasks, 1)
        
        self.assertEqual(len(containers), 1)
        self.assertEqual(len(completed_tasks), 3)
    
    def test_sjf_empty_tasks(self):
        """测试空任务列表"""
        completed_tasks, containers, current_time = sjf_scheduler([], 2)
        
        self.assertEqual(len(completed_tasks), 0)
        self.assertEqual(len(containers), 2)
        self.assertEqual(current_time, 0)
    
    def test_sjf_task_completion_times(self):
        """测试任务完成时间计算"""
        completed_tasks, containers, current_time = sjf_scheduler(self.tasks, 2)
        
        for task in completed_tasks:
            self.assertIsNotNone(task.completion_time)
            self.assertIsNotNone(task.start_time)
            self.assertGreaterEqual(task.completion_time, task.start_time)
            self.assertGreaterEqual(task.turnaround_time, task.burst_time)
            self.assertGreaterEqual(task.waiting_time, 0)

class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_single_task(self):
        """测试单个任务"""
        tasks = [Task("single_task", 0, 5, 1)]
        
        # 测试FCFS
        completed_fcfs, containers_fcfs, time_fcfs = fcfs_scheduler(tasks, 2)
        self.assertEqual(len(completed_fcfs), 1)
        self.assertEqual(completed_fcfs[0].id, "single_task")
        
        # 测试SJF
        completed_sjf, containers_sjf, time_sjf = sjf_scheduler(tasks, 2)
        self.assertEqual(len(completed_sjf), 1)
        self.assertEqual(completed_sjf[0].id, "single_task")
    
    def test_zero_burst_time(self):
        """测试零执行时间的任务"""
        tasks = [Task("zero_task", 0, 0, 1)]
        
        completed_tasks, containers, current_time = fcfs_scheduler(tasks, 2)
        
        # 零执行时间的任务应该立即完成
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].completion_time, 0)
    
    def test_high_priority_tasks(self):
        """测试高优先级任务（虽然FCFS和SJF不基于优先级）"""
        tasks = [
            Task("low_priority", 0, 5, 5),  # 低优先级
            Task("high_priority", 0, 3, 1)   # 高优先级
        ]
        
        # FCFS应该按到达时间排序，忽略优先级
        completed_fcfs, _, _ = fcfs_scheduler(tasks, 2)
        self.assertEqual(completed_fcfs[0].id, "low_priority")
        
        # SJF应该按作业长度排序，忽略优先级
        completed_sjf, _, _ = sjf_scheduler(tasks, 2)
        self.assertEqual(completed_sjf[0].id, "high_priority")  # 因为更短

if __name__ == "__main__":
    unittest.main()