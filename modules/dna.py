import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_learning_style_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_style (
            user TEXT PRIMARY KEY,
            dominant_style TEXT,
            average_quiz_score REAL,
            last_updated TEXT
        )
    """)
    conn.commit()
    conn.close()

def update_learning_style(user, style, score):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT user FROM learning_style WHERE user = ?", (user,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute("""
            UPDATE learning_style
            SET dominant_style = ?, average_quiz_score = ?, last_updated = ?
            WHERE user = ?
        """, (style, score, now, user))
    else:
        cursor.execute("""
            INSERT INTO learning_style (user, dominant_style, average_quiz_score, last_updated)
            VALUES (?, ?, ?, ?)
        """, (user, style, score, now))

    conn.commit()
    conn.close()

def get_learning_style(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dominant_style, average_quiz_score, last_updated
        FROM learning_style
        WHERE user = ?
    """, (user,))
    result = cursor.fetchone()
    conn.close()
    return result

def show_learning_dna(user):
    st.subheader("🧬 AI Learning DNA")

    result = get_learning_style(user)
    if result:
        style, score, updated = result
        st.markdown(f"""
        - **Dominant Style**: 🎨 {style}  
        - **Average Quiz Score**: 📊 {score}  
        - **Last Updated**: 🕒 {updated}
        """)

        if score < 3.0:
            st.warning("Your scores suggest a plateau. Consider blending your dominant style with another — e.g., Visual + Kinesthetic.")
        else:
            st.success("Your learning style is performing well! Keep reinforcing it with targeted resources.")
    else:
        st.info("No learning style data found. Complete a quiz or update your profile to begin tracking.")