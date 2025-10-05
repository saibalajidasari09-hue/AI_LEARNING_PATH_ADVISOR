import streamlit as st
import sqlite3
from modules.study_sessions import show_study_plan
from modules.schedule import export_exam_calendar
from modules.db import get_connection 

def show_exam_manager():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            subject TEXT,
            date TEXT,
            time TEXT,
            location TEXT
        )
    """)
    conn.commit()
    conn.close()

def manage_exams(user):
    st.subheader("📘 Manage Exams")
    show_exam_manager()  # ✅ Ensures table is created

    with st.form("exam_form"):
        subject = st.text_input("Subject")
        date = st.date_input("Exam Date")
        time = st.time_input("Exam Time")
        location = st.text_input("Location")
        submitted = st.form_submit_button("➕ Add Exam", key="add_exam_btn")

        if submitted and subject:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO exams (user, subject, date, time, location)
                VALUES (?, ?, ?, ?, ?)
            """, (user, subject, date.strftime("%Y-%m-%d"), time.strftime("%H:%M"), location))
            conn.commit()
            conn.close()
            st.success(f"✅ Added exam for **{subject}** on {date} at {time} in *{location}*")

    st.markdown("---")
    st.subheader("📅 Upcoming Exams")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, date, time, location
        FROM exams
        WHERE user = ?
        ORDER BY date
    """, (user,))
    exams = cursor.fetchall()
    conn.close()

    if exams:
        for subject, date, time, location in exams:
            st.markdown(f"✅ **{subject}** — {date} at {time} in *{location}*")
    else:
        st.info("No exams scheduled yet.")

    st.markdown("---")
    st.subheader("📤 Export Exam Calendar")

    if st.button("Generate .ics Calendar File", key="generate_ics_btn"):
        file_path = export_exam_calendar(user)
        with open(file_path, "rb") as f:
            st.download_button(
                label="📥 Download exams.ics",
                data=f,
                file_name="exams.ics",
                mime="text/calendar"
            )

    st.markdown("---")
    # Optional: show_study_plan(user)