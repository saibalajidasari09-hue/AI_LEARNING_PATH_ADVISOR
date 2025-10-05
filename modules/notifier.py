import streamlit as st
from datetime import datetime
from modules.db import get_connection
from modules.notify import get_preferences

# 🧱 Table initializer (already correct)
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

# 🔔 Notification simulation logic (reusable)
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
        st.markdown("- 📚 You have a study session today.")
    if goals:
        st.markdown("- 🎯 Check your goal progress.")
    if streak:
        st.markdown("- 🔥 Keep your streak alive!")

# 🚨 Dispatch notifications (called from app.py)
def dispatch_notifications(user):
    st.subheader("🚨 Alert Center")
    simulate_notifications(user)