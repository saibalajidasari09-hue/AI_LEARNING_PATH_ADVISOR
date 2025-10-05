import streamlit as st
import sqlite3
from modules.db import get_connection
from datetime import datetime, timedelta

def show_planner_table(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            subject TEXT,
            priority INTEGER,
            last_reviewed TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_subject(user, subject, priority):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO planner (user, subject, priority, last_reviewed)
        VALUES (?, ?, ?, ?)
    """, (user, subject, priority, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_subjects(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, priority, last_reviewed
        FROM planner
        WHERE user = ?
    """, (user,))
    subjects = cursor.fetchall()
    conn.close()
    return subjects

def generate_study_sequence(user):
    subjects = get_subjects(user)
    today = datetime.now().date()
    sequence = []

    for subject, priority, last_reviewed in subjects:
        last_date = datetime.strptime(last_reviewed, "%Y-%m-%d").date()
        days_since = (today - last_date).days
        urgency_score = priority * (1 + days_since / 3)
        sequence.append((subject, urgency_score))

    sequence.sort(key=lambda x: x[1], reverse=True)
    return sequence

def show_multi_subject_planner(user):
    st.subheader("🧠 Multi-Subject Planner with AI Ordering")
    show_planner_table(user)  # ✅ Now defined

    with st.form("planner_form"):
        subject = st.text_input("Subject Name")
        priority = st.slider("Priority (1 = low, 5 = high)", 1, 5, 3)
        submitted = st.form_submit_button("Add Subject", key="add_subject_btn")

        if submitted and subject:
            add_subject(user, subject, priority)
            st.success(f"✅ Added **{subject}** with priority {priority}")

    st.markdown("---")
    st.subheader("📋 Current Subjects")

    subjects = get_subjects(user)
    if subjects:
        for subject, priority, last_reviewed in subjects:
            st.markdown(f"- **{subject}** | Priority: {priority} | Last Reviewed: {last_reviewed}")
    else:
        st.info("No subjects added yet.")

    st.markdown("---")
    st.subheader("🧠 AI-Ordered Study Sequence")

    sequence = generate_study_sequence(user)
    if sequence:
        for i, (subject, score) in enumerate(sequence, 1):
            st.markdown(f"{i}. **{subject}** — Urgency Score: {round(score, 2)}")
    else:
        st.info("No sequence generated yet.")