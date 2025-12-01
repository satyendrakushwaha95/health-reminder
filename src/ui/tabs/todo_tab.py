from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLineEdit, QTimeEdit, QPushButton, QScrollArea, QLabel)
from PySide6.QtCore import QTime, Qt
from datetime import datetime, timedelta
from src.models.task_model import Task
from src.ui.components.task_widget import TaskWidget

class ToDoTab(QWidget):
    def __init__(self, scheduler, repo):
        super().__init__()
        self.scheduler = scheduler
        self.repo = repo
        self.init_ui()
        self.refresh_tasks()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Add Task Area
        add_layout = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Task Title...")
        
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime.currentTime().addSecs(300))
        
        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_task)

        add_layout.addWidget(self.title_input, 2)
        add_layout.addWidget(self.time_input, 1)
        add_layout.addWidget(self.add_btn)
        layout.addLayout(add_layout)

        # Task List
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.task_container)
        layout.addWidget(self.scroll_area)

    def add_task(self):
        title = self.title_input.text().strip()
        if not title:
            return

        qtime = self.time_input.time()
        now = datetime.now()
        due_time = now.replace(hour=qtime.hour(), minute=qtime.minute(), second=0, microsecond=0)
        
        if due_time < now:
             due_time += timedelta(days=1)

        task = Task(title=title, due_time=due_time)
        self.repo.add_task(task)
        self.title_input.clear()
        self.refresh_tasks()

    def refresh_tasks(self):
        for i in reversed(range(self.task_layout.count())):
            widget = self.task_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        tasks = self.repo.get_all_tasks()
        tasks.sort(key=lambda t: t.due_time)

        for task in tasks:
            w = TaskWidget(task)
            w.status_changed.connect(self.on_task_changed)
            w.delete_requested.connect(self.on_task_delete)
            self.task_layout.addWidget(w)

    def on_task_changed(self, task):
        self.repo.update_task(task)

    def on_task_delete(self, task):
        self.repo.delete_task(task.id)
        self.refresh_tasks()
