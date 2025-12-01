from datetime import datetime, timedelta
from typing import Callable, Optional
from src.data.repository import TaskRepository
from src.models.task_model import Task

class SchedulerService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository
        
        # Health Signals
        self.on_break_due: Callable[[str], None] = lambda t: None
        
        # To-Do Signals
        self.on_pre_alert: Callable[[Task], None] = lambda t: None
        self.on_due_alert: Callable[[Task], None] = lambda t: None
        self.pre_alert_minutes = 5

        # Health State
        self.is_running = False
        self.interval_minutes = 30
        self.last_break_time: Optional[datetime] = None
        self.next_break_time: Optional[datetime] = None

    # --- Health Logic ---
    def start_session(self, interval_minutes: int):
        self.interval_minutes = interval_minutes
        self.is_running = True
        self.last_break_time = datetime.now()
        self.next_break_time = self.last_break_time + timedelta(minutes=self.interval_minutes)

    def stop_session(self):
        self.is_running = False
        self.next_break_time = None

    def get_time_remaining(self) -> str:
        if not self.is_running or not self.next_break_time:
            return "Stopped"
        now = datetime.now()
        remaining = self.next_break_time - now
        if remaining.total_seconds() < 0:
            return "Due!"
        minutes, seconds = divmod(int(remaining.total_seconds()), 60)
        return f"{minutes:02d}:{seconds:02d}"

    # --- Combined Check ---
    def check_all(self):
        now = datetime.now()
        
        # 1. Check Health Interval
        if self.is_running and self.next_break_time:
            if now >= self.next_break_time:
                self.on_break_due("Time to Stand Up & Walk!\nTake a break from the screen.")
                self.last_break_time = now
                self.next_break_time = now + timedelta(minutes=self.interval_minutes)

        # 2. Check To-Do Tasks
        tasks = self.repository.get_all_tasks()
        dirty = False
        for task in tasks:
            if task.is_completed:
                continue

            # Pre-Alert
            pre_time = task.due_time - timedelta(minutes=self.pre_alert_minutes)
            if not task.has_alerted_pre and now >= pre_time and now < task.due_time:
                task.has_alerted_pre = True
                self.on_pre_alert(task)
                dirty = True

            # Due-Alert
            if not task.has_alerted_due and now >= task.due_time:
                task.has_alerted_due = True
                self.on_due_alert(task)
                dirty = True
        
        if dirty:
            self.repository.save_tasks()
