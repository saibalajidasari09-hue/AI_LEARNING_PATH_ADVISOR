import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def show_study_table(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            slot TEXT NOT NULL,
            notes TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_study_session(user, subject, date, slot, notes):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO study_sessions (user, subject, date, slot, notes, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user, subject, date.strftime("%Y-%m-%d"), slot, notes, timestamp))
    conn.commit()
    conn.close()

def get_today_sessions(user):
    conn = get_connection()
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT subject, slot, notes, timestamp
        FROM study_sessions
        WHERE user = ? AND date = ?
        ORDER BY slot ASC
    """, (user, today))
    sessions = cursor.fetchall()
    conn.close()
    return sessions

def show_study_session_tracker(user):
    st.subheader("📚 Daily Study Session Tracker")
    show_study_table(user)

    st.markdown("---")
    st.subheader("📅 Today's Study Sessions")

    sessions = get_today_sessions(user)
    if sessions:
        for subject, slot, notes, timestamp in sessions:
            st.markdown(f"- **{slot}** → *{subject}* | Notes: {notes if notes else '—'} | Logged: {timestamp}")
    else:
        st.info("No sessions logged for today.")

def show_study_plan(user):
    st.header("📚 Your Study Plan")
    show_study_table(user)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, subject, date, slot, notes
        FROM study_sessions
        WHERE user = ?
        ORDER BY date, slot
    """, (user,))
    sessions = cursor.fetchall()

    if not sessions:
        st.info("No study sessions scheduled yet.")
        conn.close()
        return

    for session in sessions:
        with st.expander(f"{session[1]} on {session[2]} during {session[3]}"):
            st.write(f"📝 Notes: {session[4]}")
            if st.button(f"❌ Delete Session {session[0]}", key=f"delete_{session[0]}"):
                cursor.execute("DELETE FROM study_sessions WHERE id = ?", (session[0],))
                conn.commit()
                st.success("Session deleted. Please refresh.")

    conn.close()

    st.markdown("---")
    st.subheader("📝 Log a New Study Session")

    with st.form("study_form"):
        subject = st.text_input("Subject")
        date = st.date_input("Study Date", value=datetime.now())
        slot = st.selectbox("Time Slot", ["Morning", "Afternoon", "Evening", "Night"])
        notes = st.text_area("Notes or Focus Area")
        submitted = st.form_submit_button("Log Session", key="log_session_btn")

        if submitted and subject:
            log_study_session(user, subject, date, slot, notes)
            st.success(f"✅ Logged study session for **{subject}** on {date} during {slot}")

    st.markdown("---")
    st.subheader("📅 Today's Study Sessions")

    sessions = get_today_sessions(user)
    if sessions:
        for subject, slot, notes, timestamp in sessions:
            st.markdown(f"- **{slot}** → *{subject}* | Notes: {notes if notes else '—'} | Logged: {timestamp}")
    else:
        st.info("No sessions logged for today.")