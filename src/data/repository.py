import json
import os
from typing import List
from src.models.task_model import Task, BreakEvent

class TaskRepository:
    def __init__(self, task_file="tasks.json", history_file="history.json"):
        self.task_file = task_file
        self.history_file = history_file
        self.tasks: List[Task] = []
        self.history: List[BreakEvent] = []
        self.load_tasks()
        self.load_history()

    def load_tasks(self):
        if not os.path.exists(self.task_file):
            self.tasks = []
            return
        try:
            with open(self.task_file, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, IOError):
            self.tasks = []

    def save_tasks(self):
        data = [task.to_dict() for task in self.tasks]
        with open(self.task_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_history(self):
        if not os.path.exists(self.history_file):
            self.history = []
            return
        try:
            with open(self.history_file, "r") as f:
                data = json.load(f)
                self.history = [BreakEvent.from_dict(item) for item in data]
        except (json.JSONDecodeError, IOError):
            self.history = []

    def save_history(self):
        data = [event.to_dict() for event in self.history]
        with open(self.history_file, "w") as f:
            json.dump(data, f, indent=4)

    # --- Task Methods ---
    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def update_task(self, updated_task: Task):
        for i, task in enumerate(self.tasks):
            if task.id == updated_task.id:
                self.tasks[i] = updated_task
                self.save_tasks()
                return
    
    def delete_task(self, task_id: str):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save_tasks()

    def get_all_tasks(self) -> List[Task]:
        return self.tasks

    # --- History Methods ---
    def add_event(self, event: BreakEvent):
        self.history.append(event)
        self.save_history()

    def get_history(self) -> List[BreakEvent]:
        return self.history
