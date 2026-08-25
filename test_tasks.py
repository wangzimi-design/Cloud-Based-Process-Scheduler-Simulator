import unittest
from tasks import Task, Container

class TestTask(unittest.TestCase):
    """测试Task类的功能"""
    
    def test_task_initialization(self):
        """测试Task对象正确初始化"""
        task = Task("task_1", 0, 10, 3)
        
        self.assertEqual(task.id, "task_1")
        self.assertEqual(task.arrival_time, 0)
        self.assertEqual(task.burst_time, 10)
        self.assertEqual(task.remaining_time, 10)
        self.assertEqual(task.priority, 3)
        self.assertIsNone(task.start_time)
        self.assertIsNone(task.completion_time)
        self.assertIsNone(task.container_id)
    
    def test_task_turnaround_time(self):
        """测试周转时间计算"""
        task = Task("task_1", 0, 10, 3)
        task.start_time = 5
        task.completion_time = 15
        
        self.assertEqual(task.turnaround_time, 15)  # 15 - 0 = 15
    
    def test_task_waiting_time(self):
        """测试等待时间计算"""
        task = Task("task_1", 0, 10, 3)
        task.start_time = 5
        task.completion_time = 15
        
        self.assertEqual(task.waiting_time, 5)  # 15 - 10 = 5
    
    def test_task_turnaround_time_no_completion(self):
        """测试未完成任务周转时间为0"""
        task = Task("task_1", 0, 10, 3)
        
        self.assertEqual(task.turnaround_time, 0)
    
    def test_task_waiting_time_no_completion(self):
        """测试未完成任务等待时间为0"""
        task = Task("task_1", 0, 10, 3)
        
        self.assertEqual(task.waiting_time, 0)

class TestContainer(unittest.TestCase):
    """测试Container类的功能"""
    
    def test_container_initialization(self):
        """测试Container对象正确初始化"""
        container = Container("container_1", 2, 2048)
        
        self.assertEqual(container.id, "container_1")
        self.assertEqual(container.cpu_cores, 2)
        self.assertEqual(container.memory, 2048)
        self.assertIsNone(container.current_task)
        self.assertEqual(container.utilization_history, [])
        self.assertFalse(container.is_running)
    
    def test_container_default_values(self):
        """测试Container默认值"""
        container = Container("container_1")
        
        self.assertEqual(container.cpu_cores, 1)
        self.assertEqual(container.memory, 1024)

if __name__ == "__main__":
    unittest.main()