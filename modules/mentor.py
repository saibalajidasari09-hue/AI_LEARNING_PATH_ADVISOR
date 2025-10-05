import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_mentor_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mentorship (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            mentor_name TEXT,
            topic TEXT,
            advice TEXT,
            action_items TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_mentorship(user, mentor_name, topic, advice, action_items):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO mentorship (user, mentor_name, topic, advice, action_items, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user, mentor_name, topic, advice, action_items, timestamp))
    conn.commit()
    conn.close()

def get_mentorship_history(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mentor_name, topic, advice, action_items, timestamp
        FROM mentorship
        WHERE user = ?
        ORDER BY timestamp DESC
    """, (user,))
    results = cursor.fetchall()
    conn.close()
    return results

def show_mentorship_engine(user):
    st.subheader("🤝 Mentorship Tracker")
    init_mentor_table()

    with st.form("mentor_form"):
        mentor_name = st.text_input("Mentor Name")
        topic = st.text_input("Topic of Discussion")
        advice = st.text_area("Advice Received")
        action_items = st.text_area("Action Items or Follow-ups")
        submitted = st.form_submit_button("Log Mentorship")

        if submitted and mentor_name and topic:
            log_mentorship(user, mentor_name, topic, advice, action_items)
            st.success(f"Logged mentorship session with **{mentor_name}**")

    st.markdown("---")
    st.subheader("📜 Mentorship History")

    history = get_mentorship_history(user)
    if history:
        for mentor_name, topic, advice, action_items, timestamp in history:
            st.markdown(f"""
            ### 🧑‍🏫 {mentor_name}
            - **Topic**: {topic}
            - **Timestamp**: {timestamp}
            - **Advice**: {advice}
            - **Action Items**: {action_items if action_items else "—"}
            """)
            st.markdown("---")
    else:
        st.info("No mentorship sessions logged yet.")