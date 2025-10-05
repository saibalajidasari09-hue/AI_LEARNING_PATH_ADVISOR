import streamlit as st
from modules.exams import manage_exams
from modules.study_sessions import show_study_plan
from modules.schedule import export_exam_calendar
from modules.db import get_connection, ensure_study_sessions_table

def show_study_plan(user):
    ensure_study_sessions_table()  # ✅ Ensure table exists before querying

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject, date, time
        FROM study_sessions
        WHERE user = ?
        ORDER BY date
    """, (user,))
    sessions = cursor.fetchall()

    st.subheader("📚 Your Study Plan")
    if sessions:
        for idx, (subject, date, time) in enumerate(sessions):
            st.write(f"• {subject} on {date} at {time}")
    else:
        st.info("No study sessions scheduled yet.")

    conn.close()
    print(f"Study plan for {user} loaded.")

def show_dashboard(user):
    st.title("📈 Learning & Productivity Dashboard")
    st.markdown(f"Welcome, **{user}**! Here's your personalized academic overview.")

    st.markdown("---")
    st.subheader("📘 Exam Summary")
    manage_exams(user)

    st.markdown("---")
    st.subheader("📚 AI-Generated Study Plan")
    show_study_plan(user)

    st.markdown("---")
    st.subheader("📤 Export Calendar")
    if st.button("Generate .ics Calendar File", key="generate_ics_button"):
        file_path = export_exam_calendar(user)
        with open(file_path, "rb") as f:
            st.download_button(
                label="📥 Download exams.ics",
                data=f,
                file_name="exams.ics",
                mime="text/calendar",
                key="download_ics_button"
            )

    st.markdown("---")
    st.subheader("🧬 Learning Style Insights")

    # Static example — you can wire this to dynamic quiz results later
    dominant_style = "Visual"
    average_quiz_score = 2.5
    suggestion = "Consider blending Visual with Kinesthetic methods if scores plateau."

    st.markdown(f"""
    - **Dominant Style**: 🎨 {dominant_style}  
    - **Average Quiz Score**: 📊 {average_quiz_score}  
    - **Suggestion**: 💡 {suggestion}
    """)

    st.markdown("---")
    st.caption("Built with ❤️ by Dasari • GenAI Productivity OS")