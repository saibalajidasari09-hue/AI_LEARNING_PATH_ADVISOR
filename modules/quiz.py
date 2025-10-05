import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_quiz_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            score INTEGER,
            total INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_quiz_result(user, score, total):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO quiz_results (user, score, total, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user, score, total, timestamp))
    conn.commit()
    conn.close()

def get_quiz_history(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT score, total, timestamp
        FROM quiz_results
        WHERE user = ?
        ORDER BY timestamp DESC
    """, (user,))
    results = cursor.fetchall()
    conn.close()
    return results

def show_quiz_engine(user):
    st.subheader("🧪 Learning Style Quiz")
    init_quiz_table()

    st.markdown("Answer the following questions to help us understand your dominant learning style:")

    questions = [
        ("I prefer diagrams and visual aids when learning.", "Visual"),
        ("I learn best by doing hands-on activities.", "Kinesthetic"),
        ("I remember information better when I hear it.", "Auditory"),
        ("I enjoy reading and writing to understand concepts.", "Verbal"),
        ("I like solving puzzles and logical problems.", "Logical")
    ]

    responses = {}
    for i, (q, style) in enumerate(questions):
        responses[style] = st.slider(q, 1, 5, 3, key=f"q{i}")

    if st.button("Submit Quiz"):
        dominant_style = max(responses, key=responses.get)
        score = sum(responses.values())
        total = len(questions) * 5
        log_quiz_result(user, score, total)

        st.success(f"✅ Your dominant learning style is **{dominant_style}**")
        st.markdown(f"**Score**: {score}/{total}")

        if score / total < 0.6:
            st.warning("Your responses suggest mixed preferences. Consider blending styles for better results.")
        else:
            st.info(f"Try using more {dominant_style}-based resources in your study plan.")

    st.markdown("---")
    st.subheader("📜 Quiz History")

    history = get_quiz_history(user)
    if history:
        for score, total, timestamp in history:
            st.markdown(f"- {timestamp}: Score {score}/{total}")
    else:
        st.info("No quiz attempts logged yet.")