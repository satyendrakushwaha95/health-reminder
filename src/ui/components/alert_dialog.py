from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class AlertDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Health Reminder")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.resize(300, 150)

        layout = QVBoxLayout()
        
        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(self.label)

        self.ok_btn = QPushButton("I'm Back / I Acknowledge")
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; font-weight: bold;")
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)
