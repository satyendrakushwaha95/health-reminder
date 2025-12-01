from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QPushButton
from PySide6.QtCore import Signal, Qt
from src.models.task_model import Task

class TaskWidget(QWidget):
    status_changed = Signal(Task)
    delete_requested = Signal(Task)

    def __init__(self, task: Task):
        super().__init__()
        self.task = task
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        # Checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.task.is_completed)
        self.checkbox.stateChanged.connect(self.on_check_changed)
        layout.addWidget(self.checkbox)

        # Title and Time
        info_layout = QHBoxLayout()
        self.title_label = QLabel(self.task.title)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        time_str = self.task.due_time.strftime("%H:%M")
        self.time_label = QLabel(f"Due: {time_str}")
        self.time_label.setStyleSheet("color: gray;")

        layout.addWidget(self.title_label, 1) # Stretch
        layout.addWidget(self.time_label)

        # Delete Button
        self.delete_btn = QPushButton("X")
        self.delete_btn.setFixedWidth(30)
        self.delete_btn.clicked.connect(self.on_delete)
        layout.addWidget(self.delete_btn)

        self.update_style()

    def on_check_changed(self, state):
        self.task.is_completed = (state == Qt.Checked)
        self.update_style()
        self.status_changed.emit(self.task)

    def on_delete(self):
        self.delete_requested.emit(self.task)

    def update_style(self):
        if self.task.is_completed:
            self.title_label.setStyleSheet("font-weight: normal; color: gray; text-decoration: line-through;")
        else:
            self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
