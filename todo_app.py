import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todos.db")

# ── Database Setup ──────────────────────────────────────────────────────────

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                title     TEXT    NOT NULL,
                done      INTEGER NOT NULL DEFAULT 0,
                priority  TEXT    NOT NULL DEFAULT 'medium',
                created   TEXT    NOT NULL
            )
        """)
        conn.commit()

# ── CRUD Operations ─────────────────────────────────────────────────────────

def add_todo(title: str, priority: str = "medium") -> int:
    priority = priority.lower()
    if priority not in ("low", "medium", "high"):
        priority = "medium"
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO todos (title, priority, created) VALUES (?, ?, ?)",
            (title.strip(), priority, datetime.now().strftime("%Y-%m-%d %H:%M")),
        )
        conn.commit()
        return cur.lastrowid

def list_todos(show_done: bool = True):
    with get_connection() as conn:
        if show_done:
            rows = conn.execute(
                "SELECT * FROM todos ORDER BY done, priority DESC, id"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM todos WHERE done=0 ORDER BY priority DESC, id"
            ).fetchall()
    return [dict(r) for r in rows]

def complete_todo(todo_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute("UPDATE todos SET done=1 WHERE id=?", (todo_id,))
        conn.commit()
        return cur.rowcount > 0

def delete_todo(todo_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM todos WHERE id=?", (todo_id,))
        conn.commit()
        return cur.rowcount > 0

def clear_done():
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM todos WHERE done=1")
        conn.commit()
        return cur.rowcount

# ── Display Helpers ─────────────────────────────────────────────────────────

PRIORITY_ICONS = {"high": "🔴", "medium": "🟡", "low": "🟢"}
PRIORITY_ORDER = {"high": 3, "medium": 2, "low": 1}

def print_todos(todos):
    if not todos:
        print("\n  📭  No tasks found.\n")
        return
    width = 60
    print("\n" + "─" * width)
    print(f"  {'ID':<4} {'✓':<3} {'P':<4}  {'Task':<30}  {'Created'}")
    print("─" * width)
    for t in todos:
        icon = PRIORITY_ICONS.get(t["priority"], "⚪")
        check = "✅" if t["done"] else "  "
        title = t["title"][:32] + "…" if len(t["title"]) > 32 else t["title"]
        print(f"  {t['id']:<4} {check}  {icon}  {title:<34} {t['created']}")
    print("─" * width + "\n")

# ── CLI Menu ────────────────────────────────────────────────────────────────

MENU = """
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
"""

def run():
    init_db()
    print(MENU)
    while True:
        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("  Task title: ").strip()
            if not title:
                print("  ⚠  Title cannot be empty.")
                continue
            priority = input("  Priority [low / medium / high] (default: medium): ").strip() or "medium"
            tid = add_todo(title, priority)
            print(f"  ✅  Task #{tid} added.")

        elif choice == "2":
            print_todos(list_todos(show_done=True))

        elif choice == "3":
            print_todos(list_todos(show_done=False))

        elif choice == "4":
            try:
                tid = int(input("  Task ID to mark done: "))
            except ValueError:
                print("  ⚠  Invalid ID.")
                continue
            if complete_todo(tid):
                print(f"  ✅  Task #{tid} marked as done.")
            else:
                print(f"  ⚠  Task #{tid} not found.")

        elif choice == "5":
            try:
                tid = int(input("  Task ID to delete: "))
            except ValueError:
                print("  ⚠  Invalid ID.")
                continue
            if delete_todo(tid):
                print(f"  🗑  Task #{tid} deleted.")
            else:
                print(f"  ⚠  Task #{tid} not found.")

        elif choice == "6":
            n = clear_done()
            print(f"  🧹  {n} completed task(s) removed.")

        elif choice == "0":
            print("\n  Bye! 👋\n")
            break

        else:
            print("  ⚠  Unknown option, try again.")

        print(MENU)

if __name__ == "__main__":
    run()