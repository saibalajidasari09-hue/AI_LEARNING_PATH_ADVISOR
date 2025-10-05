import sqlite3
from db import get_connection

def reset_exams_table():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS exams")
    
    cursor.execute("""
        CREATE TABLE exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            subject TEXT,
            date TEXT,
            time TEXT,
            location TEXT,
            notes TEXT,
            timestamp TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    return "✅ Exams table has been reset successfully."