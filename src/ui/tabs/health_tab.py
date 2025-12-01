from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QComboBox, QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt
from src.services.scheduler_service import SchedulerService

class HealthTab(QWidget):
    def __init__(self, scheduler: SchedulerService, repo):
        super().__init__()
        self.scheduler = scheduler
        self.repo = repo
        self.init_ui()
        self.refresh_history()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Status Label
        self.status_label = QLabel("Next Break: Stopped")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; background-color: #2c3e50; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.status_label)

        # Controls
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Interval:"))
        self.interval_combo = QComboBox()
        self.interval_combo.addItems(["15 Minutes", "30 Minutes", "60 Minutes", "1 Minute (Test)"])
        hbox.addWidget(self.interval_combo)
        layout.addLayout(hbox)

        self.toggle_btn = QPushButton("Start Monitoring")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setStyleSheet("background-color: #2980b9; color: white; font-size: 16px; padding: 10px;")
        self.toggle_btn.toggled.connect(self.on_toggle)
        layout.addWidget(self.toggle_btn)

        # History
        layout.addWidget(QLabel("Today's Breaks:"))
        self.history_list = QListWidget()
        layout.addWidget(self.history_list)

    def on_toggle(self, checked):
        if checked:
            text = self.interval_combo.currentText()
            if "15" in text: minutes = 15
            elif "30" in text: minutes = 30
            elif "60" in text: minutes = 60
            else: minutes = 1
            
            self.scheduler.start_session(minutes)
            self.toggle_btn.setText("Stop Monitoring")
            self.toggle_btn.setStyleSheet("background-color: #c0392b; color: white; font-size: 16px; padding: 10px;")
            self.interval_combo.setEnabled(False)
        else:
            self.scheduler.stop_session()
            self.toggle_btn.setText("Start Monitoring")
            self.toggle_btn.setStyleSheet("background-color: #2980b9; color: white; font-size: 16px; padding: 10px;")
            self.interval_combo.setEnabled(True)
            self.status_label.setText("Next Break: Stopped")

    def update_status(self):
        if self.scheduler.is_running:
            remaining = self.scheduler.get_time_remaining()
            self.status_label.setText(f"Next Break: {remaining}")

    def refresh_history(self):
        self.history_list.clear()
        history = self.repo.get_history()
        for event in reversed(history):
            time_str = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            item = QListWidgetItem(f"{time_str} - {event.type}")
            self.history_list.addItem(item)
