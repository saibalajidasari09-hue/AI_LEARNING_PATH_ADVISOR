import sqlite3
from db import get_connection

def force_reset_exams(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exams WHERE user = ?", (user,))
    conn.commit()
    conn.close()
    return f"✅ All exam entries for user '{user}' have been deleted."