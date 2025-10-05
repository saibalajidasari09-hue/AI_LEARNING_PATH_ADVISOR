import streamlit as st
import sqlite3
from datetime import datetime, timedelta
from modules.db import get_connection

def init_revision_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS revision (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            subject TEXT,
            topic TEXT,
            revision_date TEXT,
            urgency INTEGER,
            last_revised TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_revision(user, subject, topic, revision_date, urgency):
    conn = get_connection()
    cursor = conn.cursor()
    last_revised = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO revision (user, subject, topic, revision_date, urgency, last_revised)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user, subject, topic, revision_date.strftime("%Y-%m-%d"), urgency, last_revised))
    conn.commit()
    conn.close()

def get_upcoming_revisions(user):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().date()
    cursor.execute("""
        SELECT subject, topic, revision_date, urgency, last_revised
        FROM revision
        WHERE user = ? AND DATE(revision_date) >= ?
        ORDER BY revision_date ASC
    """, (user, today.strftime("%Y-%m-%d")))
    revisions = cursor.fetchall()
    conn.close()
    return revisions

def generate_revision_sequence(user):
    revisions = get_upcoming_revisions(user)
    today = datetime.now().date()
    sequence = []

    for subject, topic, revision_date, urgency, last_revised in revisions:
        days_until = (datetime.strptime(revision_date, "%Y-%m-%d").date() - today).days
        days_since = (today - datetime.strptime(last_revised, "%Y-%m-%d").date()).days
        score = urgency * (1 + days_since / 2) / (1 + days_until)
        sequence.append((subject, topic, revision_date, round(score, 2)))

    sequence.sort(key=lambda x: x[3], reverse=True)
    return sequence

def show_revision_planner(user):
    st.subheader("🔁 Revision Planner")
    init_revision_table()

    with st.form("revision_form"):
        subject = st.text_input("Subject")
        topic = st.text_input("Topic")
        revision_date = st.date_input("Planned Revision Date")
        urgency = st.slider("Urgency (1 = low, 5 = high)", 1, 5, 3)
        submitted = st.form_submit_button("Log Revision")

        if submitted and subject and topic:
            log_revision(user, subject, topic, revision_date, urgency)
            st.success(f"✅ Logged revision for **{topic}** in *{subject}*")

    st.markdown("---")
    st.subheader("📅 Upcoming Revisions")

    revisions = get_upcoming_revisions(user)
    if revisions:
        for subject, topic, date, urgency, last in revisions:
            st.markdown(f"- **{subject}** → *{topic}* on {date} | Urgency: {urgency} | Last Revised: {last}")
    else:
        st.info("No upcoming revisions logged.")

    st.markdown("---")
    st.subheader("🧠 AI-Ordered Revision Sequence")

    sequence = generate_revision_sequence(user)
    if sequence:
        for i, (subject, topic, date, score) in enumerate(sequence, 1):
            st.markdown(f"{i}. **{subject}** → *{topic}* on {date} | Score: {score}")
    else:
        st.info("No sequence generated yet.")