import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'expense_tracker.db')


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ('Demo User', 'demo@spendly.com', generate_password_hash('demo123')),
    )
    user_id = cursor.lastrowid

    sample_expenses = [
        (user_id, 'Grocery shopping',   850.00,  'Food',          '2026-06-01'),
        (user_id, 'Electricity bill',  1200.00,  'Bills',         '2026-06-03'),
        (user_id, 'Movie tickets',      450.00,  'Entertainment', '2026-06-05'),
        (user_id, 'Uber ride',          320.00,  'Transport',     '2026-06-07'),
        (user_id, 'Medicine',           680.00,  'Health',        '2026-06-10'),
        (user_id, 'Clothes shopping',  1500.00,  'Shopping',      '2026-06-12'),
        (user_id, 'Miscellaneous',      200.00,  'Other',         '2026-06-15'),
        (user_id, 'Coffee and snacks',  180.00,  'Food',          '2026-06-18'),
    ]
    cursor.executemany(
        "INSERT INTO expenses (user_id, description, amount, category, date) VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )

    conn.commit()
    conn.close()
