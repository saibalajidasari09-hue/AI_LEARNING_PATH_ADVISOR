import streamlit as st
import time
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_pomodoro_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pomodoro_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            session_type TEXT,
            duration INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_session(user, session_type, duration):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO pomodoro_sessions (user, session_type, duration, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user, session_type, duration, timestamp))
    conn.commit()
    conn.close()

def get_today_sessions(user):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT session_type, duration, timestamp
        FROM pomodoro_sessions
        WHERE user = ? AND DATE(timestamp) = ?
    """, (user, today))
    sessions = cursor.fetchall()
    conn.close()
    return sessions

def show_pomodoro_timer(user):
    st.subheader("⏱️ Pomodoro Timer")
    init_pomodoro_table()

    st.markdown("Classic 25-minute focus + 5-minute break cycle. Stay sharp, stay consistent!")

    session_type = st.radio("Choose session type", ["Focus (25 min)", "Break (5 min)"])
    duration = 25 if "Focus" in session_type else 5

    if st.button("Start Timer"):
        st.success(f"🔒 {session_type} started! Stay focused.")
        with st.empty():
            for i in range(duration * 60, 0, -1):
                mins, secs = divmod(i, 60)
                st.metric(label="Time Remaining", value=f"{mins:02d}:{secs:02d}")
                time.sleep(1)
        st.balloons()
        log_session(user, session_type, duration)
        st.success(f"✅ {session_type} completed!")

    st.markdown("---")
    st.subheader("📊 Today's Sessions")

    sessions = get_today_sessions(user)
    if sessions:
        focus_count = sum(1 for s in sessions if "Focus" in s[0])
        break_count = sum(1 for s in sessions if "Break" in s[0])
        st.markdown(f"- **Focus Sessions**: {focus_count} 🔥")
        st.markdown(f"- **Breaks Taken**: {break_count} 🧘")
        for s_type, dur, ts in sessions:
            st.markdown(f"{ts} — {s_type} ({dur} min)")
    else:
        st.info("No sessions logged today.")