import streamlit as st
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
from modules.db import get_connection

def init_graph_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS concept_graph (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            source TEXT,
            target TEXT,
            relationship TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_concept_link(user, source, target, relationship):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO concept_graph (user, source, target, relationship)
        VALUES (?, ?, ?, ?)
    """, (user, source, target, relationship))
    conn.commit()
    conn.close()

def get_concept_links(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT source, target, relationship
        FROM concept_graph
        WHERE user = ?
    """, (user,))
    links = cursor.fetchall()
    conn.close()
    return links

def show_graph_explorer(user):
    st.subheader("🧠 Knowledge Graph Explorer")
    init_graph_table()

    with st.form("graph_form"):
        source = st.text_input("Concept A (Source)")
        target = st.text_input("Concept B (Target)")
        relationship = st.text_input("Relationship (e.g., 'leads to', 'depends on')")
        submitted = st.form_submit_button("Add Link")

        if submitted and source and target:
            add_concept_link(user, source, target, relationship)
            st.success(f"Linked **{source}** → **{target}** as *{relationship}*")

    st.markdown("---")
    st.subheader("📊 Visual Graph")

    links = get_concept_links(user)
    if links:
        G = nx.DiGraph()
        for source, target, rel in links:
            G.add_edge(source, target, label=rel)

        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2000, font_size=10, arrows=True)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        st.pyplot(plt)
    else:
        st.info("No concept links found. Start building your graph above.")