import os
import streamlit as st
import sqlite3
from ics import Calendar, Event
from datetime import datetime
from modules.db import get_connection

def show_schedule_table(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            subject TEXT,
            date TEXT,
            time_slot TEXT,
            session_type TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def export_exam_calendar(user):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject, date, time, location
        FROM exams
        WHERE user = ?
        ORDER BY date
    """, (user,))

    calendar = Calendar()
    exams = cursor.fetchall()
    for exam in exams:
        subject, date_str, time_str, location = exam
        dt_str = f"{date_str} {time_str}"
        try:
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            continue

        event = Event()
        event.name = f"Exam: {subject}"
        event.begin = dt
        event.location = location
        calendar.events.add(event)

    output_path = os.path.join("data", "exams_calendar.ics")
    with open(output_path, "w") as f:
        f.writelines(calendar)

    return output_path

def add_schedule_entry(user, subject, date, time_slot, session_type):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO schedule (user, subject, date, time_slot, session_type, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user, subject, date.strftime("%Y-%m-%d"), time_slot, session_type, timestamp))
    conn.commit()
    conn.close()

def get_upcoming_schedule(user):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT subject, date, time_slot, session_type
        FROM schedule
        WHERE user = ? AND date >= ?
        ORDER BY date ASC, time_slot ASC
    """, (user, today))
    results = cursor.fetchall()
    conn.close()
    return results

def show_schedule_planner(user):
    st.subheader("📅 Smart Scheduler")
    show_schedule_table(user)  # ✅ Fixed: replaced undefined init_schedule_table()

    with st.form("schedule_form"):
        subject = st.text_input("Subject")
        date = st.date_input("Session Date")
        time_slot = st.selectbox("Time Slot", ["Morning", "Afternoon", "Evening", "Night"])
        session_type = st.selectbox("Session Type", ["Study", "Revision", "Exam", "Break"])
        submitted = st.form_submit_button("Add to Schedule")

        if submitted and subject:
            add_schedule_entry(user, subject, date, time_slot, session_type)
            st.success(f"✅ Scheduled **{session_type}** for *{subject}* on {date} during {time_slot}")

    st.markdown("---")
    st.subheader("📜 Upcoming Schedule")

    schedule = get_upcoming_schedule(user)
    if schedule:
        for subject, date, time_slot, session_type in schedule:
            st.markdown(f"- **{date}** | {time_slot} → *{subject}* ({session_type})")
    else:
        st.info("No upcoming sessions scheduled.")