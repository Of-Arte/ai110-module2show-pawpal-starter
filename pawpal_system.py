from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    name: str
    category: str
    duration_minutes: int
    priority: str          # "high", "medium", "low"
    recurrence: str        # "daily", "weekly", "none"
    time: str = "08:00"    # "HH:MM" format
    completed: bool = False
    due_date: date | None = None

    def __post_init__(self) -> None:
        """Initializes defaults for fields after data class construction."""
        if self.due_date is None:
            self.due_date = date.today()

    def mark_complete(self) -> None:
        """Marks the task as completed."""
        self.completed = True

    def is_due_today(self) -> bool:
        """Checks if the task is scheduled to be performed today."""
        return self.due_date == date.today()

    def advance_due_date(self) -> None:
        """Advances the due_date forward based on recurrence and resets completed flag."""
        if self.recurrence == "daily":
            self.due_date = self.due_date + timedelta(days=1)
        elif self.recurrence == "weekly":
            self.due_date = self.due_date + timedelta(weeks=1)
        self.completed = False

    def get_priority_value(self) -> int:
        """Gets the numeric value corresponding to the task's priority level."""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(self.priority.lower(), 1)


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Adds a task to the pet's list of tasks."""
        self.tasks.append(task)

    def remove_task(self, task_name: str) -> None:
        """Removes a task from the pet's list of tasks by name."""
        self.tasks = [t for t in self.tasks if t.name != task_name]

    def get_tasks(self) -> list[Task]:
        """Returns the list of tasks associated with this pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: list[str] | None = None):
        """Initializes an Owner instance with basic details and an empty list of pets."""
        self.name = name
        self.available_minutes = available_minutes
        self.preferences: list[str] = preferences or []
        self._pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's pet list."""
        self._pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Removes a pet from the owner's pet list by name."""
        self._pets = [p for p in self._pets if p.name != pet_name]

    def get_pets(self) -> list[Pet]:
        """Returns the list of pets owned by this owner."""
        return self._pets

    def get_all_tasks(self) -> list[Task]:
        """Collects all tasks across all pets owned by this owner."""
        all_tasks = []
        for pet in self.get_pets():
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet | None = None, schedule_date: date | None = None):
        """Initializes a Scheduler instance to plan tasks for an owner's pet(s)."""
        self.owner = owner
        self.pet = pet
        self.date = schedule_date or date.today()
        self.scheduled_tasks: list[Task] = []
        self.skipped_tasks: list[Task] = []

    def generate_plan(self) -> list[Task]:
        """Generates the daily plan of tasks that fit within the available time constraint.

        Steps:
        1. Collect tasks from the relevant pet(s).
        2. Sort by priority (desc) then time (asc).
        3. Greedily schedule tasks that fit in remaining owner time.
        4. Advance due dates for completed recurring tasks.
        5. Detect and store time-slot conflicts.
        """
        self.scheduled_tasks = []
        self.skipped_tasks = []
        self.conflicts: list[tuple[Task, Task]] = []
        total_time = 0
        limit = self.owner.available_minutes

        if self.pet:
            all_tasks = self.pet.get_tasks()
        else:
            all_tasks = self.owner.get_all_tasks()

        sorted_tasks = self.sort_tasks(all_tasks)
        for task in sorted_tasks:
            if not task.completed and task.is_due_today():
                if total_time + task.duration_minutes <= limit:
                    self.scheduled_tasks.append(task)
                    total_time += task.duration_minutes
                else:
                    self.skipped_tasks.append(task)

        self.handle_recurring_tasks()
        self.conflicts = self.detect_conflicts()
        return self.scheduled_tasks

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sorts tasks by priority (descending), then by scheduled time (ascending)."""
        return sorted(tasks, key=lambda t: (-t.get_priority_value(), t.time))

    def filter_by_time(self, tasks: list[Task]) -> list[Task]:
        """Filters tasks to only include those that fit within available time."""
        return [t for t in tasks if t.duration_minutes <= self.owner.available_minutes]

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Returns all scheduled tasks belonging to the named pet."""
        for pet in self.owner.get_pets():
            if pet.name.lower() == pet_name.lower():
                return [t for t in self.scheduled_tasks if t in pet.get_tasks()]
        return []

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Returns scheduled tasks filtered by completion status."""
        return [t for t in self.scheduled_tasks if t.completed == completed]

    def handle_recurring_tasks(self) -> None:
        """Advances due dates for completed recurring tasks so they stay schedulable."""
        all_tasks = self.owner.get_all_tasks()
        for task in all_tasks:
            if task.recurrence != "none" and task.completed and task.due_date is not None:
                if task.due_date <= date.today():
                    task.advance_due_date()

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Detects time-slot conflicts among scheduled tasks.

        A conflict occurs when task A starts before task B but A's end time
        (start + duration) exceeds B's start time.
        Returns a list of (task_a, task_b) conflict pairs.
        """
        conflicts: list[tuple[Task, Task]] = []
        sorted_by_time = sorted(self.scheduled_tasks, key=lambda t: t.time)
        for i, task_a in enumerate(sorted_by_time):
            for task_b in sorted_by_time[i + 1:]:
                # Parse HH:MM into total minutes for arithmetic
                a_h, a_m = map(int, task_a.time.split(":"))
                b_h, b_m = map(int, task_b.time.split(":"))
                a_start = a_h * 60 + a_m
                b_start = b_h * 60 + b_m
                a_end = a_start + task_a.duration_minutes
                if a_start == b_start or a_end > b_start:
                    conflicts.append((task_a, task_b))
        return conflicts

    def get_pet_for_task(self, task: Task) -> str:
        """Finds and returns the name of the pet associated with a task."""
        for pet in self.owner.get_pets():
            if task in pet.get_tasks():
                return pet.name
        return "Unknown"

    def explain_plan(self) -> str:
        """Returns a human-readable text explanation of the generated task schedule."""
        lines = [f"Daily plan for {self.owner.name}'s pets on {self.date}:"]
        if not self.scheduled_tasks:
            lines.append("  No tasks scheduled.")

        # Print tasks in chronological order
        for task in sorted(self.scheduled_tasks, key=lambda t: t.time):
            pet_name = self.get_pet_for_task(task)
            lines.append(f"  {task.time} — {task.name} ({task.duration_minutes} min) [priority: {task.priority}] for {pet_name}")

        if self.skipped_tasks:
            lines.append("\nSkipped tasks due to time limits:")
            for task in self.skipped_tasks:
                pet_name = self.get_pet_for_task(task)
                lines.append(f"  * {task.name} ({task.duration_minutes} min) [priority: {task.priority}] for {pet_name}")

        conflicts = getattr(self, "conflicts", [])
        if conflicts:
            lines.append("\n⚠️  TIME CONFLICTS DETECTED:")
            for task_a, task_b in conflicts:
                lines.append(f"  ⚡ '{task_a.name}' ({task_a.time}, {task_a.duration_minutes} min) overlaps with '{task_b.name}' ({task_b.time})")

        return "\n".join(lines)
