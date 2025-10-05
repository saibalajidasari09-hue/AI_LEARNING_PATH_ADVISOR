import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_hackathon_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hackathon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            feature TEXT,
            status TEXT,
            notes TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_feature_status(user, feature, status, notes):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO hackathon (user, feature, status, notes, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user, feature, status, notes, timestamp))
    conn.commit()
    conn.close()

def get_hackathon_progress(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT feature, status, notes, timestamp
        FROM hackathon
        WHERE user = ?
        ORDER BY timestamp DESC
    """, (user,))
    results = cursor.fetchall()
    conn.close()
    return results

def show_hackathon_suite(user):
    st.subheader("🚀 Hackathon Readiness Suite")
    init_hackathon_table()

    with st.form("hackathon_form"):
        feature = st.selectbox("Feature", [
            "Dashboard", "Exams", "Study Plan", "Calendar Export", "Learning DNA", "Experiment Tracker",
            "Feedback Engine", "Gamification", "Grade Tracker", "Graph Explorer", "Career Navigator",
            "Notifications", "Multi-Subject Planner", "Showcase Mode"
        ])
        status = st.selectbox("Status", ["✅ Complete", "🔧 In Progress", "❌ Not Started"])
        notes = st.text_area("Notes or blockers")
        submitted = st.form_submit_button("Log Progress")

        if submitted:
            log_feature_status(user, feature, status, notes)
            st.success(f"Logged status for **{feature}**")

    st.markdown("---")
    st.subheader("📋 Feature Progress")

    progress = get_hackathon_progress(user)
    if progress:
        for feature, status, notes, timestamp in progress:
            st.markdown(f"""
            ### 🧩 {feature}
            - **Status**: {status}
            - **Logged**: {timestamp}
            - **Notes**: {notes if notes else "—"}
            """)
            st.markdown("---")
    else:
        st.info("No progress logged yet.")

    st.subheader("🎤 Final Pitch Prep")
    st.markdown("""
    - ✅ Highlight modularity and scalability  
    - ✅ Emphasize AI-powered personalization  
    - ✅ Showcase calendar export, gamification, and career tools  
    - ✅ Mention SQLite + Streamlit stack  
    - ✅ End with: *“Built to evolve with every learner — powered by GenAI.”*
    """)