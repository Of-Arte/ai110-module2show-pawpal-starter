from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

def test_task_completion():
    # Arrange: Create a task that is initially incomplete
    task = Task(
        name="Morning Walk",
        category="Exercise",
        duration_minutes=30,
        priority="high",
        recurrence="daily"
    )
    assert not task.completed

    # Act: Mark the task complete
    task.mark_complete()

    # Assert: Verify completion status is True
    assert task.completed

def test_task_addition():
    # Arrange: Create a pet and a task
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever", age=3)
    task = Task(
        name="Brush Teeth",
        category="Grooming",
        duration_minutes=5,
        priority="low",
        recurrence="daily"
    )
    assert len(pet.get_tasks()) == 0

    # Act: Add the task to the pet
    pet.add_task(task)

    # Assert: Verify the task count increased to 1 and matches the added task
    assert len(pet.get_tasks()) == 1
    assert pet.get_tasks()[0] == task

def test_scheduler_priority_sorting():
    # Arrange: Owner, Pet, and tasks with different priorities
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever", age=3)
    owner.add_pet(pet)

    low_task = Task(name="Play Fetch", category="Exercise", duration_minutes=15, priority="low", recurrence="daily", time="15:00")
    high_task = Task(name="Give Meds", category="Health", duration_minutes=5, priority="high", recurrence="daily", time="08:00")
    medium_task = Task(name="Brush Teeth", category="Grooming", duration_minutes=10, priority="medium", recurrence="daily", time="12:00")

    pet.add_task(low_task)
    pet.add_task(high_task)
    pet.add_task(medium_task)

    scheduler = Scheduler(owner=owner)

    # Act: Generate plan
    plan = scheduler.generate_plan()

    # Assert: Verify that tasks are scheduled in priority order (high -> medium -> low)
    assert len(plan) == 3
    assert plan[0].priority == "high"
    assert plan[1].priority == "medium"
    assert plan[2].priority == "low"

def test_scheduler_time_limit():
    # Arrange: Owner with limited time (30 minutes)
    owner = Owner(name="Jordan", available_minutes=30)
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever", age=3)
    owner.add_pet(pet)

    # Adding tasks that total 55 minutes
    task1 = Task(name="Walk", category="Exercise", duration_minutes=25, priority="high", recurrence="daily", time="08:00")
    task2 = Task(name="Feeding", category="Feeding", duration_minutes=10, priority="high", recurrence="daily", time="09:00")
    task3 = Task(name="Training", category="Exercise", duration_minutes=20, priority="medium", recurrence="daily", time="10:00")

    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)

    scheduler = Scheduler(owner=owner)

    # Act: Generate plan
    plan = scheduler.generate_plan()

    # Assert: Only task1 (25m) fits within the 30-minute limit. Others are skipped.
    assert len(plan) == 1
    assert plan[0] == task1
    assert task2 in scheduler.skipped_tasks
    assert task3 in scheduler.skipped_tasks

def test_scheduler_skips_completed_tasks():
    # Arrange: Owner, Pet, and one completed task, one incomplete task
    owner = Owner(name="Jordan", available_minutes=60)
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever", age=3)
    owner.add_pet(pet)

    completed_task = Task(name="Walk", category="Exercise", duration_minutes=20, priority="high", recurrence="daily", time="08:00", completed=True)
    incomplete_task = Task(name="Meds", category="Health", duration_minutes=5, priority="high", recurrence="daily", time="09:00", completed=False)

    pet.add_task(completed_task)
    pet.add_task(incomplete_task)

    scheduler = Scheduler(owner=owner)

    # Act: Generate plan
    plan = scheduler.generate_plan()

    # Assert: Only the incomplete task is scheduled
    assert len(plan) == 1
    assert plan[0] == incomplete_task
    assert completed_task not in plan
    assert completed_task not in scheduler.skipped_tasks

def test_scheduler_sorting_chronological():
    # Arrange: Create tasks with the SAME priority but different times
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever", age=3)
    owner.add_pet(pet)

    task_late = Task(name="Late Walk", category="Exercise", duration_minutes=30, priority="high", recurrence="none", time="17:00")
    task_early = Task(name="Early Meds", category="Health", duration_minutes=5, priority="high", recurrence="none", time="08:00")
    task_mid = Task(name="Lunch Feed", category="Feeding", duration_minutes=10, priority="high", recurrence="none", time="12:00")

    pet.add_task(task_late)
    pet.add_task(task_early)
    pet.add_task(task_mid)

    scheduler = Scheduler(owner=owner)

    # Act: Generate plan
    plan = scheduler.generate_plan()

    # Assert: All tasks are high priority, so they should be sorted chronologically by time
    assert len(plan) == 3
    assert plan[0] == task_early
    assert plan[1] == task_mid
    assert plan[2] == task_late

def test_recurrence_logic_daily_task():
    # Arrange: Create a pet and add a daily recurring task due today
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever", age=3)
    today = date.today()
    task = Task(
        name="Daily Walk",
        category="Exercise",
        duration_minutes=30,
        priority="high",
        recurrence="daily",
        due_date=today
    )
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1

    # Act: Mark the task complete
    success = pet.mark_task_complete("Daily Walk")

    # Assert: Verify completion and spawning of the next daily task
    assert success
    tasks = pet.get_tasks()
    assert len(tasks) == 2
    
    # Original task should be completed
    assert tasks[0].completed
    assert tasks[0].due_date == today

    # New task should be scheduled for tomorrow and incomplete
    tomorrow = today + timedelta(days=1)
    assert not tasks[1].completed
    assert tasks[1].due_date == tomorrow
    assert tasks[1].name == "Daily Walk"
    assert tasks[1].recurrence == "daily"

def test_scheduler_conflict_duplicate_times():
    # Arrange: Create two tasks scheduled at the exact same time
    owner = Owner(name="Jordan", available_minutes=120)
    pet = Pet(name="Mochi", species="Dog", breed="Golden Retriever", age=3)
    owner.add_pet(pet)

    task1 = Task(name="Morning Feeding", category="Feeding", duration_minutes=15, priority="high", recurrence="none", time="08:00")
    task2 = Task(name="Morning Meds", category="Health", duration_minutes=5, priority="high", recurrence="none", time="08:00")

    pet.add_task(task1)
    pet.add_task(task2)

    scheduler = Scheduler(owner=owner)

    # Act: Generate plan (both should fit in 120 minutes)
    plan = scheduler.generate_plan()

    # Assert: Both are scheduled, and a conflict is detected
    assert len(plan) == 2
    assert len(scheduler.conflicts) == 1
    # Verify that the two tasks are indeed the ones in conflict
    conflict = scheduler.conflicts[0]
    assert (task1 in conflict) and (task2 in conflict)
