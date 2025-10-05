import streamlit as st
import sqlite3
from modules.db import get_connection

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

def get_projects(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, description, status, deadline, tech_stack, timestamp
        FROM projects
        WHERE user = ?
        ORDER BY timestamp DESC
    """, (user,))
    results = cursor.fetchall()
    conn.close()
    return results

def show_showcase_dashboard(user):
    st.subheader("🌟 Showcase Dashboard")
    st.markdown("Your curated portfolio of achievements, projects, and milestones.")

    view = st.radio("Choose what to showcase", ["Portfolio", "Projects", "All"])

    if view in ["Portfolio", "All"]:
        st.markdown("### 🧩 Portfolio Highlights")
        items = get_portfolio_items(user)
        if items:
            category_filter = st.selectbox("Filter by Category", ["All"] + sorted(set(i[2] for i in items)))
            for title, desc, cat, link, ts in items:
                if category_filter == "All" or category_filter == cat:
                    st.markdown(f"""
                    #### 🔗 {title}
                    - **Category**: {cat}
                    - **Date**: {ts}
                    - **Description**: {desc}
                    - **Link**: {link if link else "—"}
                    """)
                    st.markdown("---")
        else:
            st.info("No portfolio items found.")

    if view in ["Projects", "All"]:
        st.markdown("### 🛠️ Project Highlights")
        projects = get_projects(user)
        if projects:
            status_filter = st.selectbox("Filter by Status", ["All"] + sorted(set(p[2] for p in projects)))
            for title, desc, status, deadline, tech, ts in projects:
                if status_filter == "All" or status_filter == status:
                    st.markdown(f"""
                    #### 🚧 {title}
                    - **Status**: {status}
                    - **Deadline**: {deadline}
                    - **Tech Stack**: {tech}
                    - **Date**: {ts}
                    - **Description**: {desc}
                    """)
                    st.markdown("---")
        else:
            st.info("No projects found.")