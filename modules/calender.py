def export_plan_to_ics(user):
    from ics import Calendar, Event
    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("study_plans.db")
    cursor = conn.cursor()
    cursor.execute("SELECT week, day, task, timestamp FROM plans WHERE user = ?", (user,))
    rows = cursor.fetchall()
    conn.close()

    cal = Calendar()
    for week, day, task, ts in rows:
        e = Event()
        e.name = f"{week} {day}: {task}"
        e.begin = datetime.fromisoformat(ts)
        e.duration = {"minutes": 60}
        cal.events.add(e)

    return str(cal)