import streamlit as st
from modules.db import get_connection
from datetime import datetime
st.set_page_config(
    page_title="GenAI Productivity OS",
    page_icon="🚀 ",
    layout="wide",
)
# Import all modules
from modules.dashboard import show_dashboard
from modules.planner import show_multi_subject_planner
from modules.subject_order import show_subject_order
from modules.schedule import show_schedule_planner
from modules.study_sessions import show_study_session_tracker
from modules.revision import show_revision_planner
from modules.exams import manage_exams
from modules.grades import show_grade_tracker
from modules.graph import init_learning_evolution_table
from modules.graph import show_graphs
from modules.graph_explorer import show_graph_explorer
from modules.gamify import show_gamify_table
from modules.pomodoro import show_pomodoro_timer
from modules.quiz import show_quiz_engine
from modules.resources import show_resource_hub
from modules.projects import show_project_tracker
from modules.portfolio import show_portfolio
from modules.showcase import show_showcase_dashboard
from modules.mentor import show_mentorship_engine
from modules.career import show_career_path
from modules.hackathon import show_hackathon_suite
from modules.notify import show_notification_table
from modules.notify import show_notification_center
from modules.notifier import dispatch_notifications

def init_user_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def login():
    st.title("🚀 GenAI Productivity OS")
    st.markdown("Built for learners, founders, and dreamers. Powered by AI.")

    username = st.text_input("Enter your username")
    if st.button("Login") and username:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute("INSERT INTO users (username, created_at) VALUES (?, ?)", (username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
        conn.close()
        st.session_state["user"] = username
        st.success(f"Welcome, {username}!")

def main():
    init_user_table()
    init_learning_evolution_table()
    show_notification_table()
    if "user" not in st.session_state:
        login()
        return

    user = st.session_state["user"]
    show_notification_center(user)

    user = st.session_state["user"]
    show_gamify_table(user)

    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox("Choose a module", [
        "Dashboard", "Planner", "Subject Order", "Schedule", "Study Sessions", "Revision",
        "Exams", "Grades", "Graphs", "Graph Explorer", "Gamification", "Pomodoro",
        "Quiz", "Resources", "Projects", "Portfolio", "Showcase", "Mentor",
        "Career", "Hackathon", "Notifications", "Alerts"
    ])

    if page == "Dashboard":
        show_dashboard(user)
    elif page == "Planner":
        show_multi_subject_planner(user)
    elif page == "Subject Order":
        show_subject_order(user)
    elif page == "Schedule":
        show_schedule_planner(user)
    elif page == "Study Sessions":
        show_study_session_tracker(user)
    elif page == "Revision":
        show_revision_planner(user)
    elif page == "Exams":
        manage_exams(user)
    elif page == "Grades":
        show_grade_tracker(user)
    elif page == "Graphs":
        show_graphs(user)
    elif page == "Graph Explorer":
        show_graph_explorer(user)
    elif page == "Gamification":
        show_gamify_table(user)
    elif page == "Pomodoro":
        show_pomodoro_timer(user)
    elif page == "Quiz":
        show_quiz_engine(user)
    elif page == "Resources":
        show_resource_hub(user)
    elif page == "Projects":
        show_project_tracker(user)
    elif page == "Portfolio":
        show_portfolio(user)
    elif page == "Showcase":
        show_showcase_dashboard(user)
    elif page == "Mentor":
        show_mentorship_engine(user)
    elif page == "Career":
        show_career_path(user)
    elif page == "Hackathon":
        show_hackathon_suite(user)
    elif page == "Notifications":
        show_notification_center(user)
    elif page == "Alerts":
        dispatch_notifications(user)

if __name__ == "__main__":
    main()