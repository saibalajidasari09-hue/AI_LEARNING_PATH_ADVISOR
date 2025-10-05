import sqlite3
import os
from datetime import datetime

# Constants
DB_FOLDER = "data"
DB_NAME = "data.db"
DB_PATH = os.path.join(DB_FOLDER, DB_NAME)

def ensure_data_folder():
    """Ensure the data folder exists."""
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)

def get_connection():
    """Return a thread-safe SQLite connection."""
    ensure_data_folder()
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def ensure_study_sessions_table():
    """Create the study_sessions table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            slot TEXT,
            notes TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def list_tables():
    """Return a list of all tables in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def run_query(query, params=None):
    """Run a raw SQL query (use with caution)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        result = cursor.fetchall()
        return result
    except Exception as e:
        return f"❌ Query failed: {e}"
    finally:
        conn.close()

def reset_table(table_name, schema):
    """Drop and recreate a table with the given schema."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(schema)
        conn.commit()
        return f"✅ Table '{table_name}' has been reset."
    except Exception as e:
        return f"❌ Failed to reset table '{table_name}': {e}"
    finally:
        conn.close()

def backup_database():
    """Create a timestamped backup of the database file."""
    ensure_data_folder()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(DB_FOLDER, f"backup_{timestamp}.db")
    try:
        with open(DB_PATH, "rb") as src, open(backup_path, "wb") as dst:
            dst.write(src.read())
        return f"✅ Backup created at {backup_path}"
    except Exception as e:
        return f"❌ Backup failed: {e}"

# Optional: Run diagnostics if executed directly
if __name__ == "__main__":
    print("🔍 DB Diagnostics")
    print(f"📁 Path: {DB_PATH}")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()[0]
        print(f"✅ Connected to SQLite {version}")
        print("📦 Tables:", list_tables())
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")