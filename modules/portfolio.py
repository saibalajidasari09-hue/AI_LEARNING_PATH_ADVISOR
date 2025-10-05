import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_portfolio_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            title TEXT,
            description TEXT,
            category TEXT,
            link TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_portfolio_item(user, title, description, category, link):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO portfolio (user, title, description, category, link, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user, title, description, category, link, timestamp))
    conn.commit()
    conn.close()

def get_portfolio_items(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, description, category, link, timestamp
        FROM portfolio
        WHERE user = ?
        ORDER BY timestamp DESC
    """, (user,))
    items = cursor.fetchall()
    conn.close()
    return items

def show_portfolio(user):
    st.subheader("🌟 Showcase Mode: Your Learning Portfolio")
    init_portfolio_table()

    with st.form("portfolio_form"):
        title = st.text_input("Project / Achievement Title")
        description = st.text_area("Brief Description")
        category = st.selectbox("Category", ["Project", "Hackathon", "Experiment", "Course", "Internship", "Award", "Other"])
        link = st.text_input("External Link (optional)")
        submitted = st.form_submit_button("Add to Portfolio")

        if submitted and title:
            add_portfolio_item(user, title, description, category, link)
            st.success(f"✅ Added **{title}** to your portfolio!")

    st.markdown("---")
    st.subheader("📜 Your Portfolio Timeline")

    items = get_portfolio_items(user)
    if items:
        for title, description, category, link, timestamp in items:
            st.markdown(f"""
            ### 🧩 {title}
            - **Category**: {category}
            - **Logged**: {timestamp}
            - **Description**: {description}
            - **Link**: {link if link else "—"}
            """)
            st.markdown("---")
    else:
        st.info("No portfolio items added yet.")