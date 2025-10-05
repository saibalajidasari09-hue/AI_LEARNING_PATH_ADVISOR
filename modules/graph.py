import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from modules.db import get_connection

# 🔧 Fetch grade data for plotting
def get_grade_data(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, grade, timestamp
        FROM grades
        WHERE user = ?
        ORDER BY timestamp ASC
    """, (user,))
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=["Subject", "Grade", "Timestamp"])

# 🔧 Fetch quiz score data for plotting
def get_quiz_data(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, average_quiz_score
        FROM learning_evolution
        WHERE user = ?
        ORDER BY timestamp ASC
    """, (user,))
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=["Timestamp", "Score"])

# 📊 Main graph display function
def show_graphs(user):
    st.subheader("📊 Learning Graphs")
    st.markdown("---")

    graph_type = st.selectbox("Choose a graph to view", [
        "Grade Progression", "Quiz Score Evolution"
    ])

    if graph_type == "Grade Progression":
        df = get_grade_data(user)
        if not df.empty:
            fig, ax = plt.subplots()
            for subject in df["Subject"].unique():
                subject_df = df[df["Subject"] == subject]
                ax.plot(pd.to_datetime(subject_df["Timestamp"]), subject_df["Grade"], label=subject)
            ax.set_title("Grade Progression Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Grade")
            ax.legend()
            st.pyplot(fig)
        else:
            st.info("No grade data available.")

    elif graph_type == "Quiz Score Evolution":
        df = get_quiz_data(user)
        if not df.empty:
            fig, ax = plt.subplots()
            ax.bar(pd.to_datetime(df["Timestamp"]), df["Score"], color="orange")
            ax.set_title("Quiz Score Evolution")
            ax.set_xlabel("Date")
            ax.set_ylabel("Score")
            st.pyplot(fig)
        else:
            st.info("No quiz score data available.")

# 🧱 Table initializer for quiz score tracking
def init_learning_evolution_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_evolution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            timestamp TEXT,
            average_quiz_score REAL
        )
    """)
    conn.commit()
    conn.close()