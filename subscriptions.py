import sqlite3
from datetime import datetime, timedelta

DB_FILE = "subscriptions.db"

def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions
        (chat_id INTEGER PRIMARY KEY, expiry_date TEXT)
    ''')
    conn.commit()
    conn.close()

def add_subscription(chat_id: int, days: int = 30):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    expiry_date = datetime.now() + timedelta(days=days)
    c.execute("INSERT OR REPLACE INTO subscriptions (chat_id, expiry_date) VALUES (?, ?)",
              (chat_id, expiry_date.isoformat()))
    conn.commit()
    conn.close()

def is_subscription_active(chat_id: int) -> bool:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT expiry_date FROM subscriptions WHERE chat_id = ?", (chat_id,))
    result = c.fetchone()
    conn.close()

    if result is None:
        return False

    expiry_date = datetime.fromisoformat(result[0])
    return expiry_date > datetime.now()

def get_all_active_subscribers() -> list[int]:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT chat_id, expiry_date FROM subscriptions")
    results = c.fetchall()
    conn.close()

    active_subscribers = []
    for chat_id, expiry_date_str in results:
        expiry_date = datetime.fromisoformat(expiry_date_str)
        if expiry_date > datetime.now():
            active_subscribers.append(chat_id)

    return active_subscribers
