import streamlit as st
import sqlite3
from datetime import datetime
from modules.db import get_connection

def init_resources_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            title TEXT,
            link TEXT,
            category TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_resource(user, title, link, category):
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO resources (user, title, link, category, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user, title, link, category, timestamp))
    conn.commit()
    conn.close()

def get_resources(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, link, category, timestamp
        FROM resources
        WHERE user = ?
        ORDER BY timestamp DESC
    """, (user,))
    results = cursor.fetchall()
    conn.close()
    return results

def show_resource_hub(user):
    st.subheader("📚 Resource Hub")
    init_resources_table()

    with st.form("resource_form"):
        title = st.text_input("Resource Title")
        link = st.text_input("Link (URL)")
        category = st.selectbox("Category", ["Study", "Career", "Tools", "Reference", "Coding", "Other"])
        submitted = st.form_submit_button("Add Resource")

        if submitted and title and link:
            add_resource(user, title, link, category)
            st.success(f"✅ Added resource: **{title}**")

    st.markdown("---")
    st.subheader("📜 Your Saved Resources")

    resources = get_resources(user)
    if resources:
        for title, link, category, timestamp in resources:
            st.markdown(f"""
            ### 🔗 {title}
            - **Category**: {category}
            - **Added**: {timestamp}
            - **Link**: [{link}]({link})
            """)
            st.markdown("---")
    else:
        st.info("No resources saved yet.")