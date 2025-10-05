import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_projects_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            title TEXT,
            description TEXT,
            status TEXT,
            deadline TEXT,
            tech_stack TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_project(user, title, description, status, deadline, tech_stack):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO projects (user, title, description, status, deadline, tech_stack, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user, title, description, status, deadline, tech_stack, timestamp))
    conn.commit()
    conn.close()

def get_projects(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, description, status, deadline, tech_stack, timestamp
        FROM projects
        WHERE user = ?
        ORDER BY timestamp DESC
    """, (user,))
    results = cursor.fetchall()
    conn.close()
    return results

def show_project_tracker(user):
    st.subheader("🛠️ Project Tracker")
    init_projects_table()

    with st.form("project_form"):
        title = st.text_input("Project Title")
        description = st.text_area("Brief Description")
        status = st.selectbox("Status", ["Planning", "In Progress", "Completed", "Paused"])
        deadline = st.date_input("Deadline")
        tech_stack = st.text_input("Tech Stack (e.g., Python, Streamlit, SQLite)")
        submitted = st.form_submit_button("Log Project")

        if submitted and title:
            log_project(user, title, description, status, deadline.strftime("%Y-%m-%d"), tech_stack)
            st.success(f"✅ Logged project: **{title}**")

    st.markdown("---")
    st.subheader("📜 Project Timeline")

    projects = get_projects(user)
    if projects:
        for title, description, status, deadline, tech_stack, timestamp in projects:
            st.markdown(f"""
            ### 🚧 {title}
            - **Status**: {status}
            - **Deadline**: {deadline}
            - **Tech Stack**: {tech_stack}
            - **Logged**: {timestamp}
            - **Description**: {description}
            """)
            st.markdown("---")
    else:
        st.info("No projects logged yet.")