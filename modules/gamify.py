import streamlit as st
import sqlite3
from datetime import datetime, timedelta
from modules.db import get_connection

def show_gamify_table(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gamify (
            user TEXT PRIMARY KEY,
            last_active TEXT,
            streak INTEGER,
            xp INTEGER,
            level INTEGER,
            badges TEXT
        )
    """)
    conn.commit()
    conn.close()

def update_gamify(user):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().date()

    cursor.execute("SELECT last_active, streak, xp, level, badges FROM gamify WHERE user = ?", (user,))
    result = cursor.fetchone()

    if result:
        last_active_str, streak, xp, level, badges = result
        last_active = datetime.strptime(last_active_str, "%Y-%m-%d").date()
        delta = (now - last_active).days

        if delta == 1:
            streak += 1
        elif delta > 1:
            streak = 1  # reset streak

        xp += 10  # daily login XP
        level = xp // 100

        cursor.execute("""
            UPDATE gamify
            SET last_active = ?, streak = ?, xp = ?, level = ?
            WHERE user = ?
        """, (now.strftime("%Y-%m-%d"), streak, xp, level, user))
    else:
        cursor.execute("""
            INSERT INTO gamify (user, last_active, streak, xp, level, badges)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user, now.strftime("%Y-%m-%d"), 1, 10, 0, ""))

    conn.commit()
    conn.close()

def get_gamify_stats(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO streaks (user, date, streak_count)
    VALUES (?, ?, ?)
""", (user, date, streak_count))