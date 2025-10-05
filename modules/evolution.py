import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_evolution_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_evolution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            dominant_style TEXT,
            average_quiz_score REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_learning_evolution(user, style, score):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO learning_evolution (user, dominant_style, average_quiz_score, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user, style, score, timestamp))
    conn.commit()
    conn.close()

def get_latest_evolution(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dominant_style, average_quiz_score, timestamp
        FROM learning_evolution
        WHERE user = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (user,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_evolution_history(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, dominant_style, average_quiz_score
        FROM learning_evolution
        WHERE user = ?
        ORDER BY timestamp ASC
    """, (user,))
    history = cursor.fetchall()
    conn.close()
    return history

def show_learning_evolution(user):
    st.subheader("📈 Learning Style Evolution")

    latest = get_latest_evolution(user)
    if latest:
        style, score, timestamp = latest
        st.markdown(f"""
        - **Dominant Style**: 🎨 {style}  
        - **Average Quiz Score**: 📊 {score}  
        - **Last Updated**: 🕒 {timestamp}
        """)

        if score < 3.0:
            st.warning("Your scores suggest a plateau. Consider blending your dominant style with another — e.g., Visual + Kinesthetic.")
        else:
            st.success("Your learning style is performing well! Keep reinforcing it with targeted resources.")
    else:
        st.info("No evolution data found. Start by completing a learning style quiz or logging your current style.")

    st.markdown("---")
    st.subheader("📊 Historical Evolution")

    history = get_evolution_history(user)
    if history:
        for timestamp, style, score in history:
            st.markdown(f"🕒 {timestamp} — **{style}** | Score: {score}")
    else:
        st.info("No historical records yet.")