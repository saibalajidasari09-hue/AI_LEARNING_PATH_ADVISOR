import streamlit as st
from datetime import datetime
from modules.db import get_connection

# 🧱 Create notifications table if not exists
def show_notification_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            user TEXT PRIMARY KEY,
            exams_enabled INTEGER,
            study_enabled INTEGER,
            goals_enabled INTEGER,
            streak_enabled INTEGER,
            last_checked TEXT
        )
    """)
    conn.commit()
    conn.close()

# 🔧 Update preferences for a user
def update_preferences(user, exams, study, goals, streak):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT user FROM notifications WHERE user = ?", (user,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute("""
            UPDATE notifications
            SET exams_enabled = ?, study_enabled = ?, goals_enabled = ?, streak_enabled = ?, last_checked = ?
            WHERE user = ?
        """, (exams, study, goals, streak, now, user))
    else:
        cursor.execute("""
            INSERT INTO notifications (user, exams_enabled, study_enabled, goals_enabled, streak_enabled, last_checked)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user, exams, study, goals, streak, now))

    conn.commit()
    conn.close()

# 📥 Fetch preferences for a user
def get_preferences(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT exams_enabled, study_enabled, goals_enabled, streak_enabled
        FROM notifications
        WHERE user = ?
    """, (user,))
    result = cursor.fetchone()
    conn.close()
    return result

# 🔔 Simulate smart nudges based on preferences
def simulate_notifications(user):
    prefs = get_preferences(user)
    if not prefs:
        st.info("No notification preferences set.")
        return

    exams, study, goals, streak = prefs
    st.subheader("🔔 Today's Smart Notifications")

    if exams:
        st.markdown("- 📘 You have upcoming exams. Review your study plan.")
    if study:
        st.markdown("- 📚 Time to log a study session.")
    if goals:
        st.markdown("- 🎯 Check your goal progress.")
    if streak:
        st.markdown("- 🔥 Keep your streak alive!")

# 🎛️ Interactive preference manager
import time

def show_notification_center(user):
    st.subheader("🔧 Notification Preferences")
    prefs = get_preferences(user)
    unique_suffix = str(time.time())  # ensures uniqueness per render

    exams = st.checkbox("Exam Reminders", value=bool(prefs[0]) if prefs else True, key=f"{user}_exams_{unique_suffix}")
    study = st.checkbox("Study Nudges", value=bool(prefs[1]) if prefs else True, key=f"{user}_study_{unique_suffix}")
    goals = st.checkbox("Goal Tracking Alerts", value=bool(prefs[2]) if prefs else True, key=f"{user}_goals_{unique_suffix}")
    streak = st.checkbox("Streak Motivation", value=bool(prefs[3]) if prefs else True, key=f"{user}_streak_{unique_suffix}")

    if st.button("Update Preferences", key=f"{user}_update_{unique_suffix}"):
        update_preferences(user, int(exams), int(study), int(goals), int(streak))
        st.success("Preferences updated!")

    st.markdown("---")
    simulate_notifications(user)