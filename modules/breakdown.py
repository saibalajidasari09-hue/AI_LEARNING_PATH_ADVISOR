def breakdown_goal(goal):
    # Simulated GenAI breakdown — replace with LLM later
    goal = goal.lower()
    if "ai" in goal:
        return ["Learn Python", "Understand ML basics", "Explore Deep Learning", "Study NLP", "Build GenAI apps"]
    elif "web" in goal:
        return ["HTML & CSS", "JavaScript", "Frontend frameworks", "Backend with Flask/Django", "Deploy to cloud"]
    else:
        return [f"Step 1: Research {goal}", f"Step 2: Learn fundamentals", f"Step 3: Practice projects", f"Step 4: Advanced topics", f"Step 5: Build portfolio"]