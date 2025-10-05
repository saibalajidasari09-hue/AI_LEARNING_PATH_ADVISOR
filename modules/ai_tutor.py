import random

def ask_tutor(goal, query):
    # Simulated response — replace with OpenRouter or Gemini API later
    responses = [
        f"To understand {goal}, start by breaking it into smaller concepts.",
        f"Great question! Try exploring {goal} through hands-on projects.",
        f"That’s a common challenge in {goal}. Focus on examples and repetition.",
        f"Use visual tools like diagrams or videos to grasp {goal} better."
    ]
    return random.choice(responses)