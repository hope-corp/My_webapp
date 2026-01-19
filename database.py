import sqlite3
from datetime import date

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create users table with tier and usage tracking
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, 
                  tier TEXT, daily_usage INTEGER, last_use_date TEXT)''')
    conn.commit()
    conn.close()

def get_user_usage(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT tier, daily_usage, last_use_date FROM users WHERE username=?", (username,))
    row = c.fetchone()
    
    if row:
        tier, usage, last_date = row
        # Reset counter if it's a new day
        if last_date != str(date.today()):
            c.execute("UPDATE users SET daily_usage=0, last_use_date=? WHERE username=?", 
                      (str(date.today()), username))
            conn.commit()
            return tier, 0
        return tier, usage
    return None, None

def increment_usage(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET daily_usage = daily_usage + 1 WHERE username=?", (username,))
    conn.commit()
    conn.close()
