import streamlit as st

def show_career_path(user):
    st.subheader("🧭 Career Navigator")
    st.markdown(f"**User:** {user}")
    
    career_data = {
        "role": "GenAI Engineer",
        "skills": ["Python", "ML", "NLP", "LLMs"],
        "certifications": ["DeepLearning.AI GenAI", "AWS ML Specialty"],
        "next_steps": ["Build GenAI apps", "Contribute to open source"]
    }

    st.write("**Target Role:**", career_data["role"])
    st.write("**Skills to Master:**")
    st.markdown(", ".join(career_data["skills"]))
    st.write("**Recommended Certifications:**")
    st.markdown(", ".join(career_data["certifications"]))
    st.write("**Next Steps:**")
    for step in career_data["next_steps"]:
        st.markdown(f"- {step}")

def track_applications(user):
    st.subheader("📌 Application Tracker")
    st.markdown(f"**User:** {user}")
    
    company = st.text_input("Company")
    role = st.text_input("Role")
    deadline = st.date_input("Deadline")
    status = st.selectbox("Status", ["Applied", "Interviewing", "Offer", "Rejected"])
    
    if st.button("Save Application"):
        st.success(f"Saved: {role} at {company} ({status}) — Deadline: {deadline}")
        # Optional: Save to database or session_state