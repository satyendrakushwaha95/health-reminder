import unittest
import os
import sys
sys.path.append(os.getcwd())
from datetime import datetime, timedelta
from src.models.task_model import BreakEvent
from src.data.repository import TaskRepository
from src.services.scheduler_service import SchedulerService

class TestHealthApp(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_history.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.repo = TaskRepository(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_break_event_persistence(self):
        event = BreakEvent(timestamp=datetime.now(), type="Stand Up")
        self.repo.add_event(event)
        
        new_repo = TaskRepository(self.test_file)
        history = new_repo.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].type, "Stand Up")

    def test_scheduler_interval(self):
        scheduler = SchedulerService(self.repo)
        scheduler.start_session(interval_minutes=30)
        
        # Mock time
        scheduler.last_break_time = datetime.now() - timedelta(minutes=31)
        scheduler.next_break_time = scheduler.last_break_time + timedelta(minutes=30)
        
        alerts = []
        scheduler.on_break_due = lambda msg: alerts.append(msg)
        
        scheduler.check_interval()
        self.assertEqual(len(alerts), 1)
        self.assertIn("Stand Up", alerts[0])

if __name__ == '__main__':
    unittest.main()
