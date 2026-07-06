# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
============================================================
📅 TODAY'S SCHEDULE FOR JORDAN'S PETS
Total Available Owner Time: 120 minutes
============================================================
Daily plan for Jordan's pets on 2026-07-05:
  08:00 — Morning Walk (30 min) [priority: high] for Mochi
  08:15 — Playtime (20 min) [priority: medium] for Mochi
  09:00 — Breakfast Feeding (15 min) [priority: high] for Biscuit
  14:00 — Grooming Session (45 min) [priority: medium] for Mochi
  20:00 — Medication (10 min) [priority: high] for Biscuit

Skipped tasks due to time limits:
  * Evening Brush (10 min) [priority: low] for Mochi

⚠️  TIME CONFLICTS DETECTED:
  ⚡ 'Morning Walk' (08:00, 30 min) overlaps with 'Playtime' (08:15)
============================================================

🐾  Filter: Mochi's scheduled tasks only
----------------------------------------
  08:00 — Morning Walk (30 min)
  08:15 — Playtime (20 min)
  14:00 — Grooming Session (45 min)

✅  Filter: Pending (incomplete) tasks across all pets
----------------------------------------
  ⏳ 08:00 — Morning Walk
  ⏳ 08:15 — Playtime
  ⏳ 09:00 — Breakfast Feeding
  ⏳ 14:00 — Grooming Session
  ⏳ 20:00 — Medication

🔄  Recurring task — auto-spawn on complete
----------------------------------------
  Before: 1 task(s) named 'Evening Brush'
    • completed=False, due_date=2026-07-05

  mochi.mark_task_complete('Evening Brush') returned: True
  After: 2 task(s) named 'Evening Brush'
    • [✅ completed] due_date=2026-07-05
    • [⏳ pending] due_date=2026-07-06
============================================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python3 -m pytest
```

Sample test output:

```
========================================== test session starts ===========================================
platform darwin -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/agentv/Projects/studysessions/AI110/pawpal-starter
plugins: anyio-4.14.0
collected 8 items

tests/test_pawpal.py ........                                                                      [100%]

=========================================== 8 passed in 0.01s ============================================
```

### Confidence Level

**Confidence Level:** ⭐⭐⭐⭐⭐ (5/5 stars)

## 📐 Smarter Scheduling

| Feature               | Method(s)                                                                     | Notes                                                                                                                     |
| --------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Task sorting**      | `Scheduler.sort_tasks()`                                                      | Sorts tasks by priority descending (high=3, medium=2, low=1) first, and then chronologically by time ascending.           |
| **Filtering**         | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()`                   | `filter_by_pet(pet_name)` retrieves tasks for a specific pet. `filter_by_status(completed)` retrieves done/pending tasks. |
| **Conflict handling** | `Scheduler.detect_conflicts()`                                                | Compares overlapping durations (start time + duration) chronologically to detect and report conflicts without crashing.   |
| **Recurring tasks**   | `Task.mark_complete()`, `Pet.mark_task_complete()`, `Task.advance_due_date()` | Bumps `due_date` using `timedelta` (+1 day for daily, +7 days for weekly) and spawns a new instance on complete.          |

## 📸 Demo Walkthrough

The PawPal+ application features a modern Streamlit interface designed to help pet owners plan and optimize their daily schedules.

### 🔄 Example User Workflow

1. **Load or Setup Profile**: Open the application, and either click **✨ Load Demo Data** in the sidebar to populate the system or manually save a profile with owner name `Jordan` and `120` available minutes.
2. **Add a Pet**: Under the "Add a Pet" section in the sidebar, input `Mochi`, select `dog`, type `Golden Retriever`, specify age `3`, and click **Add Pet**.
3. **Schedule a Task**: Under "Schedule a Task", select `Mochi` from the dropdown. Input a task named `Morning Walk` with a duration of `30 minutes`, set priority to `High`, recurrence to `Daily`, time to `08:00`, and click **Add Task**.
4. **View & Interact**: The main panel instantly displays the metrics dashboard and today's schedule table. Click **Complete** next to a task (such as a daily recurring task like _Evening Brush_). The UI immediately refreshes, marks the current task complete, and auto-spawns a new pending instance for the next occurrence (e.g. tomorrow).
5. **Filter Results**: Scroll down to "Filter & Analyze Schedule", select `Mochi` from the pet filter, and choose `Completed` from the status filter to see only Mochi's completed tasks.

---

### 🧠 Key Scheduler Behaviors Demonstrated

- **Priority-First Sorting**: The scheduler automatically prioritizes critical tasks. Tasks are ordered by priority, and sorted chronologically within the same priority level.
- **Greedy Time Constraint Allocation**: Tasks are scheduled in sorted order until the owner's available minutes limit is reached. Any additional tasks are safely placed into the **Skipped Tasks** section.
- **Conflict Detection Warnings**: The system detects overlapping time windows. For example, if a 30-minute walk starts at `08:00` and playtime starts at `08:15`, the scheduler flags it as a conflict in a prominent warning block without crashing.
- **Auto-Scheduling Recurrence**: When a daily or weekly task is marked complete, the backend uses `dataclasses.replace()` to duplicate the task template, advance its due date, and automatically add it back to the pet's pending list.
