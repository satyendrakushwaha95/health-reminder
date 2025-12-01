import unittest
import os
import sys
sys.path.append(os.getcwd())
import json
from datetime import datetime, timedelta
from src.models.task_model import Task
from src.data.repository import TaskRepository
from src.services.scheduler_service import SchedulerService

class TestToDoApp(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_tasks.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.repo = TaskRepository(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_and_load_task(self):
        task = Task(title="Test Task", due_time=datetime.now())
        self.repo.add_task(task)
        
        # Reload
        new_repo = TaskRepository(self.test_file)
        tasks = new_repo.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test Task")
        self.assertEqual(tasks[0].id, task.id)

    def test_scheduler_alerts(self):
        # Create a task due in 2 minutes
        now = datetime.now()
        due_time = now + timedelta(minutes=2)
        task = Task(title="Alert Task", due_time=due_time)
        self.repo.add_task(task)

        scheduler = SchedulerService(self.repo)
        scheduler.pre_alert_minutes = 5 # Should alert immediately as 2 < 5
        
        alerts = []
        scheduler.on_pre_alert = lambda t: alerts.append("pre")
        scheduler.on_due_alert = lambda t: alerts.append("due")

        scheduler.check_tasks()
        
        self.assertIn("pre", alerts)
        self.assertTrue(task.has_alerted_pre)
        self.assertNotIn("due", alerts)

        # Fast forward time to due
        task.due_time = now - timedelta(seconds=1) # Overdue
        task.has_alerted_due = False # Reset for test
        
        scheduler.check_tasks()
        self.assertIn("due", alerts)

if __name__ == '__main__':
    unittest.main()
