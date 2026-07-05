from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    # 1. Create an Owner with available time constraint
    owner = Owner(name="Jordan", available_minutes=120)

    # 2. Create two Pets
    mochi = Pet(name="Mochi", species="Dog", breed="Golden Retriever", age=3)
    biscuit = Pet(name="Biscuit", species="Dog", breed="Corgi", age=1)

    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    # 3. Add Tasks — mix of priorities, times, and recurrences
    task1 = Task(
        name="Morning Walk",
        category="Exercise",
        duration_minutes=30,
        priority="high",
        recurrence="daily",
        time="08:00",
    )
    task2 = Task(
        name="Breakfast Feeding",
        category="Feeding",
        duration_minutes=15,
        priority="high",
        recurrence="daily",
        time="09:00",
    )
    task3 = Task(
        name="Grooming Session",
        category="Grooming",
        duration_minutes=45,
        priority="medium",
        recurrence="none",
        time="14:00",
    )
    task4 = Task(
        name="Medication",
        category="Health",
        duration_minutes=10,
        priority="high",
        recurrence="daily",
        time="20:00",
    )

    # ── DEMO: Conflict detection ──────────────────────────────────────────────
    # task5 starts at 08:15 while task1 (Morning Walk) runs until 08:30 → conflict
    task5 = Task(
        name="Playtime",
        category="Exercise",
        duration_minutes=20,
        priority="medium",
        recurrence="none",
        time="08:15",
    )

    # ── DEMO: Recurring task advancement ─────────────────────────────────────
    # task6 is already marked complete (simulates yesterday's done task)
    task6 = Task(
        name="Evening Brush",
        category="Grooming",
        duration_minutes=10,
        priority="low",
        recurrence="daily",
        time="19:00",
        completed=True,
    )

    mochi.add_task(task1)   # 08:00 – 08:30
    mochi.add_task(task3)   # 14:00 – 14:45
    mochi.add_task(task5)   # 08:15 – 08:35  ← conflicts with task1
    mochi.add_task(task6)   # completed recurring task

    biscuit.add_task(task2)  # 09:00 – 09:15
    biscuit.add_task(task4)  # 20:00 – 20:10

    # 4. Initialize Scheduler and generate today's plan
    scheduler = Scheduler(owner=owner)
    scheduler.generate_plan()

    # 5. Print a "Today's Schedule" to the terminal
    print("=" * 60)
    print(f"📅 TODAY'S SCHEDULE FOR {owner.name.upper()}'S PETS")
    print(f"Total Available Owner Time: {owner.available_minutes} minutes")
    print("=" * 60)
    print(scheduler.explain_plan())
    print("=" * 60)

    # ── DEMO: Filter by pet ───────────────────────────────────────────────────
    print("\n🐾  Filter: Mochi's scheduled tasks only")
    print("-" * 40)
    mochi_tasks = scheduler.filter_by_pet("Mochi")
    if mochi_tasks:
        for t in sorted(mochi_tasks, key=lambda t: t.time):
            print(f"  {t.time} — {t.name} ({t.duration_minutes} min)")
    else:
        print("  No tasks found for Mochi.")

    # ── DEMO: Filter by status ────────────────────────────────────────────────
    print("\n✅  Filter: Pending (incomplete) tasks across all pets")
    print("-" * 40)
    pending = scheduler.filter_by_status(completed=False)
    if pending:
        for t in sorted(pending, key=lambda t: t.time):
            print(f"  ⏳ {t.time} — {t.name}")
    else:
        print("  All tasks completed!")

    # ── DEMO: Recurring task advancement ─────────────────────────────────────
    print("\n🔄  Recurring task advancement")
    print("-" * 40)
    print(f"  'Evening Brush' was completed={task6.completed}, due_date={task6.due_date}")
    print("  (handle_recurring_tasks() already ran inside generate_plan)")
    print(f"  → New due_date: {task6.due_date} | completed reset to: {task6.completed}")

    print("=" * 60)


if __name__ == "__main__":
    main()
