import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_feedback_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            module TEXT,
            rating INTEGER,
            comments TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def submit_feedback(user, module, rating, comments):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO feedback (user, module, rating, comments, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user, module, rating, comments, timestamp))
    conn.commit()
    conn.close()

def get_feedback_history(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT module, rating, comments, timestamp
        FROM feedback
        WHERE user = ?
        ORDER BY timestamp DESC
    """, (user,))
    results = cursor.fetchall()
    conn.close()
    return results

def show_feedback_engine(user):
    st.subheader("🗣️ Feedback Engine")
    init_feedback_table()

    with st.form("feedback_form"):
        module = st.selectbox("Which module are you reviewing?", [
            "Dashboard", "Exams", "Study Plan", "Experiment Tracker", "Learning DNA", "Career Navigator", "Resources", "Notifications"
        ])
        rating = st.slider("Rate your experience (1 = poor, 5 = excellent)", 1, 5, 3)
        comments = st.text_area("Any suggestions or feedback?")
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            submit_feedback(user, module, rating, comments)
            st.success("✅ Feedback submitted successfully!")

    st.markdown("---")
    st.subheader("📜 Your Feedback History")

    history = get_feedback_history(user)
    if history:
        for module, rating, comments, timestamp in history:
            st.markdown(f"""
            ### 🧩 {module}
            - **Rating**: ⭐ {rating}/5
            - **Submitted**: {timestamp}
            - **Comments**: {comments}
            """)
            st.markdown("---")
    else:
        st.info("No feedback submitted yet.")