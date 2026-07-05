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
Total Available Owner Time: 90 minutes
============================================================
Daily plan for Jordan's pets on 2026-07-04:
  08:00 — Morning Walk (30 min) [priority: high] for Mochi
  09:00 — Breakfast Feeding (15 min) [priority: high] for Biscuit
  20:00 — Medication (10 min) [priority: high] for Biscuit

Skipped tasks due to time limits:
  * Grooming Session (45 min) [priority: medium] for Mochi
============================================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
========================================== test session starts ===========================================
platform darwin -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/agentv/Projects/studysessions/AI110/pawpal-starter
plugins: anyio-4.14.0
collected 5 items

tests/test_pawpal.py .....                                                                         [100%]

=========================================== 5 passed in 0.02s ============================================
```

## 📐 Smarter Scheduling

| Feature               | Method(s)                                                                     | Notes                                                                                                                     |
| --------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Task sorting**      | `Scheduler.sort_tasks()`                                                      | Sorts tasks by priority descending (high=3, medium=2, low=1) first, and then chronologically by time ascending.           |
| **Filtering**         | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()`                   | `filter_by_pet(pet_name)` retrieves tasks for a specific pet. `filter_by_status(completed)` retrieves done/pending tasks. |
| **Conflict handling** | `Scheduler.detect_conflicts()`                                                | Compares overlapping durations (start time + duration) chronologically to detect and report conflicts without crashing.   |
| **Recurring tasks**   | `Task.mark_complete()`, `Pet.mark_task_complete()`, `Task.advance_due_date()` | Bumps `due_date` using `timedelta` (+1 day for daily, +7 days for weekly) and spawns a new instance on complete.          |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
