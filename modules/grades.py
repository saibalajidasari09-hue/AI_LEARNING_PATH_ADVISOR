import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_grades_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            subject TEXT,
            grade REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_grade(user, subject, grade):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO grades (user, subject, grade, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user, subject, grade, timestamp))
    conn.commit()
    conn.close()

def get_grades(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, grade, timestamp
        FROM grades
        WHERE user = ?
        ORDER BY timestamp DESC
    """, (user,))
    results = cursor.fetchall()
    conn.close()
    return results

def calculate_gpa(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(grade)
        FROM grades
        WHERE user = ?
    """, (user,))
    result = cursor.fetchone()
    conn.close()
    return round(result[0], 2) if result and result[0] is not None else None

def show_grade_tracker(user):
    st.subheader("📊 Grade Tracker")
    init_grades_table()

    with st.form("grade_form"):
        subject = st.text_input("Subject")
        grade = st.number_input("Grade (0.0 - 10.0)", min_value=0.0, max_value=10.0, step=0.1)
        submitted = st.form_submit_button("Log Grade")

        if submitted and subject:
            log_grade(user, subject, grade)
            st.success(f"✅ Logged grade for **{subject}**: {grade}")

    st.markdown("---")
    st.subheader("📈 Performance Summary")

    gpa = calculate_gpa(user)
    if gpa is not None:
        st.markdown(f"**Current GPA**: 🎓 {gpa}")
        if gpa >= 8.0:
            st.success("Excellent performance! Keep it up.")
        elif gpa >= 6.0:
            st.info("Good progress. Aim for consistency.")
        else:
            st.warning("Consider reviewing weak areas and adjusting your study strategy.")
    else:
        st.info("No grades logged yet.")

    st.markdown("---")
    st.subheader("📜 Grade History")

    grades = get_grades(user)
    if grades:
        st.subheader("📊 Your Grades")
        for grade in grades:
            st.write(f"✅ {grade[1]}: {grade[2]}")
    else:
        st.info("No grades recorded yet.")