import streamlit as st
import sqlite3
from modules.db import DB_NAME

def manage_assignments(user):
    st.subheader("Manage Assignments")

    title = st.text_input("Title", key="assignment_title_input")
    subject = st.text_input("Subject", key="assignment_subject_input")
    deadline = st.date_input("Deadline", key="assignment_deadline_input")
    status = st.selectbox("Status", ["Pending", "Completed"], key="assignment_status_input")

    if st.button("Save Assignment", key="save_assignment_button"):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO assignments VALUES (?, ?, ?, ?, ?)", (user, title, subject, deadline.strftime("%Y-%m-%d"), status))
        conn.commit()
        conn.close()
        st.success("Assignment saved!")

    st.markdown("### Your Assignments")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT title, subject, deadline, status FROM assignments WHERE user = ?", (user,))
    rows = cursor.fetchall()
    conn.close()

    for title, subject, deadline, status in rows:
        st.write(f"📘 {title} | {subject} | Due: {deadline} | Status: {status}")