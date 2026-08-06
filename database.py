# ==========================================
# database.py
# Bureaucracy AI Database Layer
# ==========================================

import sqlite3
from datetime import datetime
import os


# ==========================================
# DATABASE PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "bureaucracy_ai.db"
)


# ==========================================
# CONNECTION
# ==========================================

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

cursor = conn.cursor()



# ==========================================
# INITIALIZE DATABASE
# ==========================================

def init_database():


    # USERS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        language TEXT,

        country TEXT,

        created_at TEXT

    )
    """)



    # EMAILS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        sender TEXT,

        subject TEXT,

        body TEXT,

        language TEXT,

        created_at TEXT

    )
    """)



    # TASKS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks_v03(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email_id INTEGER,

        category TEXT,

        task TEXT,

        deadline TEXT,

        priority TEXT,

        risk TEXT,

        explanation TEXT,

        status TEXT,

        created_at TEXT

    )
    """)



    # MEMORY

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memories(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        memory_type TEXT,

        entity TEXT,

        content TEXT,

        importance REAL,

        source_id INTEGER,

        created_at TEXT

    )
    """)



    # KNOWLEDGE BASE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_base(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        source TEXT,

        topic TEXT,

        content TEXT

    )
    """)



    # REMINDERS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        task_id INTEGER,

        reminder_date TEXT,

        reminder_type TEXT,

        status TEXT

    )
    """)



    # ACTIONS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS actions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        task_id INTEGER,

        action_type TEXT,

        result TEXT,

        requires_confirmation INTEGER,

        created_at TEXT

    )
    """)



    # ACTIVITIES

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        task_id INTEGER,

        event_type TEXT,

        description TEXT,

        created_at TEXT

    )
    """)



    # BILLS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        task_id INTEGER,

        bill_type TEXT,

        provider TEXT,

        amount TEXT,

        customer_number TEXT,

        deadline TEXT,

        status TEXT,

        created_at TEXT

    )
    """)



    conn.commit()



# ==========================================
# TIME
# ==========================================

def now():

    return datetime.now().isoformat()



if __name__ == "__main__":

    init_database()

    print(
        "Database initialized successfully"
    )