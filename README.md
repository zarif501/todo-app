# 📝 Todo List App

A simple command-line Todo List application built with **Python** and **SQLite** — no external dependencies required.

## Features

- ✅ Add tasks with priority levels (low / medium / high)
- 📋 View all tasks or only pending ones
- ✔️ Mark tasks as done
- 🗑️ Delete individual tasks
- 🧹 Clear all completed tasks at once
- 💾 Persistent storage via SQLite database

## Requirements

- Python 3.6+
- No third-party packages needed (uses built-in `sqlite3`)

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/todo-app.git
cd todo-app

# 2. Run the app
python3 todo_app.py
```

## Usage

```
╔══════════════════════════════╗
║      📝  TODO LIST APP       ║
╠══════════════════════════════╣
║  1  Add a task               ║
║  2  View all tasks           ║
║  3  View pending tasks only  ║
║  4  Mark task as done        ║
║  5  Delete a task            ║
║  6  Clear completed tasks    ║
║  0  Exit                     ║
╚══════════════════════════════╝
```

## Database

The app automatically creates a `todos.db` SQLite file in the same directory on first run.

| Column   | Type    | Description                        |
|----------|---------|------------------------------------|
| id       | INTEGER | Auto-increment primary key         |
| title    | TEXT    | Task description                   |
| done     | INTEGER | 0 = pending, 1 = completed         |
| priority | TEXT    | `low`, `medium`, or `high`         |
| created  | TEXT    | Timestamp when the task was added  |

## Project Structure

```
todo-app/
├── todo_app.py   # Main application
├── .gitignore    # Ignores todos.db and __pycache__
└── README.md     # This file
```

## License

OTU_ME Zarif
