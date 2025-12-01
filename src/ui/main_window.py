from PySide6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer
import winsound

from src.data.repository import TaskRepository
from src.services.scheduler_service import SchedulerService
from src.services.alarm_service import AlarmService
from src.ui.tabs.health_tab import HealthTab
from src.ui.tabs.todo_tab import ToDoTab
from src.ui.components.alert_dialog import AlertDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Health & To-Do Manager")
        self.resize(500, 600)

        # Services
        self.repo = TaskRepository()
        self.scheduler = SchedulerService(self.repo)
        self.alarm_service = AlarmService()

        # Connect Scheduler Signals
        self.scheduler.on_break_due = self.on_break_due
        self.scheduler.on_pre_alert = self.on_pre_alert
        self.scheduler.on_due_alert = self.on_due_alert

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_tick)
        self.timer.start(1000) # 1 second tick

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        self.health_tab = HealthTab(self.scheduler, self.repo)
        self.todo_tab = ToDoTab(self.scheduler, self.repo)

        self.tabs.addTab(self.health_tab, "Health Monitor")
        self.tabs.addTab(self.todo_tab, "To-Do Alarms")

        main_layout.addWidget(self.tabs)

    def on_timer_tick(self):
        self.scheduler.check_all()
        self.health_tab.update_status()

    # --- Signal Handlers ---
    def on_break_due(self, message):
        self.alarm_service.play_alarm()
        dlg = AlertDialog(message, self)
        dlg.exec()
        self.alarm_service.stop_alarm()
        
        # Log event (handled by caller usually, but let's do it here for simplicity or in tab)
        # Actually, Scheduler doesn't log. We should log here.
        from datetime import datetime
        from src.models.task_model import BreakEvent
        event = BreakEvent(timestamp=datetime.now(), is_acknowledged=True)
        self.repo.add_event(event)
        self.health_tab.refresh_history()

    def on_pre_alert(self, task):
        winsound.Beep(1000, 200)

    def on_due_alert(self, task):
        self.alarm_service.play_alarm()
        dlg = AlertDialog(f"Task Due: {task.title}", self)
        dlg.exec()
        self.alarm_service.stop_alarm()

    def closeEvent(self, event):
        self.alarm_service.stop_alarm()
        event.accept()
