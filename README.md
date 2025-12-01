# Health & To-Do Manager

A Windows desktop application that combines health monitoring with task management. Get reminded to take breaks and manage your daily tasks with time-based alarms.

## Features

### 🏃 Health Monitor
- **Interval-based reminders** to stand up, walk, and take screen breaks
- Customizable intervals: 15, 30, or 60 minutes
- Visual and audio alerts
- Break history tracking

### ✅ To-Do Alarms
- Create tasks with specific due times
- Pre-alerts 5 minutes before task time
- Due-time alarms with popup notifications
- Task completion tracking
- Persistent storage across app restarts

## Screenshots

The application features a clean tabbed interface:
- **Health Monitor Tab**: Start/stop monitoring with countdown timer
- **To-Do Alarms Tab**: Add and manage time-based tasks

## Installation

### Prerequisites
- Python 3.9 or higher
- Windows OS

### Setup

1. Clone the repository:
```bash
git clone https://github.com/satyendrakushwaha95/health-reminder.git
cd health-reminder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### Health Monitor
1. Switch to the "Health Monitor" tab
2. Select your preferred interval (15/30/60 minutes)
3. Click "Start Monitoring"
4. When the alarm sounds, acknowledge the break
5. View your break history in the list below

### To-Do Alarms
1. Switch to the "To-Do Alarms" tab
2. Enter a task title
3. Set the due time
4. Click "Add"
5. Receive alerts at the scheduled time
6. Mark tasks as complete or delete them

## Technical Details

### Architecture
- **Frontend**: PySide6 (Qt for Python)
- **Backend**: Python with threaded scheduler
- **Storage**: JSON files for persistence
- **Audio**: Windows native `winsound` module

### Project Structure
```
ToDoApp/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── models/
│   │   └── task_model.py   # Task and BreakEvent models
│   ├── data/
│   │   └── repository.py   # Data persistence layer
│   ├── services/
│   │   ├── scheduler_service.py  # Interval and task scheduling
│   │   └── alarm_service.py      # Audio alarm handling
│   └── ui/
│       ├── main_window.py        # Main application window
│       ├── tabs/
│       │   ├── health_tab.py     # Health monitor UI
│       │   └── todo_tab.py       # To-Do list UI
│       └── components/
│           ├── alert_dialog.py   # Alert popup
│           └── task_widget.py    # Task list item
└── tests/
    ├── test_core.py        # Core functionality tests
    └── test_health.py      # Health monitor tests
```

## Data Storage

- **tasks.json**: Stores to-do tasks
- **history.json**: Stores break event history

Both files are created automatically in the application directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Satyendra Kushwaha

## Acknowledgments

Built with Python and PySide6 for a healthier, more productive work routine.
