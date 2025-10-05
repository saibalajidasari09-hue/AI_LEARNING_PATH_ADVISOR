import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_experiment_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            title TEXT,
            description TEXT,
            status TEXT,
            reflection TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_experiment(user, title, description, status, reflection):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO experiments (user, title, description, status, reflection, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user, title, description, status, reflection, timestamp))
    conn.commit()
    conn.close()

def get_experiments(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, description, status, reflection, timestamp
        FROM experiments
        WHERE user = ?
        ORDER BY timestamp DESC
    """, (user,))
    results = cursor.fetchall()
    conn.close()
    return results

def show_experiment_tracker(user):
    st.subheader("🧪 Experiment Tracker")
    init_experiment_table()

    with st.form("experiment_form"):
        title = st.text_input("Experiment Title")
        description = st.text_area("What did you try?")
        status = st.selectbox("Status", ["Ongoing", "Successful", "Failed", "Paused"])
        reflection = st.text_area("What did you learn?")
        submitted = st.form_submit_button("Log Experiment")

        if submitted and title:
            log_experiment(user, title, description, status, reflection)
            st.success(f"Logged experiment: **{title}**")

    st.markdown("---")
    st.subheader("📜 Past Experiments")

    experiments = get_experiments(user)
    if experiments:
        for title, description, status, reflection, timestamp in experiments:
            st.markdown(f"""
            ### 🔬 {title}
            - **Status**: {status}
            - **Logged**: {timestamp}
            - **Description**: {description}
            - **Reflection**: {reflection}
            """)
            st.markdown("---")
    else:
        st.info("No experiments logged yet.")