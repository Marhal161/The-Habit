import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('habits.db')
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    date TEXT,
                    completed INTEGER
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tracked_habits (
                    id INTEGER PRIMARY KEY,
                    habit_id INTEGER,
                    tracked_date TEXT,
                    FOREIGN KEY (habit_id) REFERENCES habits (id)
                )
            """)

    def create_task(self, name, date):
        with self.conn:
            cursor = self.conn.execute("INSERT INTO habits (name, date, completed) VALUES (?, ?, ?)", (name, date, 0))
            return cursor.lastrowid, name, date

    def get_tasks(self):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM habits")
            tasks = cursor.fetchall()
            completed_tasks = [task for task in tasks if task[3] == 1]
            uncomplete_tasks = [task for task in tasks if task[3] == 0]
            return completed_tasks, uncomplete_tasks

    def mark_task_as_complete(self, task_id):
        with self.conn:
            self.conn.execute("UPDATE habits SET completed = 1 WHERE id = ?", (task_id,))

    def mark_task_as_incomplete(self, task_id):
        with self.conn:
            self.conn.execute("UPDATE habits SET completed = 0 WHERE id = ?", (task_id,))

    def delete_task(self, task_id):
        with self.conn:
            self.conn.execute("DELETE FROM habits WHERE id = ?", (task_id,))

    def track_task(self, task_id):
        with self.conn:
            self.conn.execute("INSERT INTO tracked_habits (habit_id, tracked_date) VALUES (?, ?)", (task_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def get_tracked_count(self, task_id):
        with self.conn:
            cursor = self.conn.execute("SELECT COUNT(*) FROM tracked_habits WHERE habit_id = ?", (task_id,))
            return cursor.fetchone()[0]

    def reset_task(self, task_id):
        with self.conn:
            self.conn.execute("DELETE FROM tracked_habits WHERE habit_id = ?", (task_id,))