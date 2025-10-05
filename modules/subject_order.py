import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_subject_order_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subject_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            subject TEXT,
            urgency INTEGER,
            last_revised TEXT,
            exam_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_subject_order(user, subject, urgency, last_revised, exam_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO subject_order (user, subject, urgency, last_revised, exam_date)
        VALUES (?, ?, ?, ?, ?)
    """, (user, subject, urgency, last_revised.strftime("%Y-%m-%d"), exam_date.strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_subject_order_data(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, urgency, last_revised, exam_date
        FROM subject_order
        WHERE user = ?
    """, (user,))
    results = cursor.fetchall()
    conn.close()
    return results

def generate_subject_sequence(user):
    data = get_subject_order_data(user)
    today = datetime.now().date()
    sequence = []

    for subject, urgency, last_revised, exam_date in data:
        last_gap = (today - datetime.strptime(last_revised, "%Y-%m-%d").date()).days
        days_to_exam = max((datetime.strptime(exam_date, "%Y-%m-%d").date() - today).days, 1)
        score = urgency * (1 + last_gap / 2) / days_to_exam
        sequence.append((subject, round(score, 2)))

    sequence.sort(key=lambda x: x[1], reverse=True)
    return sequence

def show_subject_order(user):
    st.subheader("🧠 AI-Powered Subject Sequencer")
    init_subject_order_table()

    with st.form("subject_order_form"):
        subject = st.text_input("Subject Name")
        urgency = st.slider("Urgency (1 = low, 5 = high)", 1, 5, 3)
        last_revised = st.date_input("Last Revised Date")
        exam_date = st.date_input("Upcoming Exam Date")
        submitted = st.form_submit_button("Add Subject")

        if submitted and subject:
            add_subject_order(user, subject, urgency, last_revised, exam_date)
            st.success(f"✅ Added **{subject}** to sequencing engine")

    st.markdown("---")
    st.subheader("📋 AI-Ordered Subject Sequence")

    sequence = generate_subject_sequence(user)
    if sequence:
        for i, (subject, score) in enumerate(sequence, 1):
            st.markdown(f"{i}. **{subject}** — Score: {score}")
    else:
        st.info("No subjects added yet.")