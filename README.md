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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Today's Schedule:
08:00 - Morning walk (Mochi) [HIGH]
09:30 - Feeding (Biscuit) [MEDIUM]
18:00 - Evening play (Mochi) [LOW] 

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest 

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
platform darwin -- Python 3.11.7, pytest-7.4.0, pluggy-1.0.0
rootdir: /Users/harithaadhikarla/Desktop/CodePath/ai110-module2show-pawpal-starter
plugins: dash-3.2.0, anyio-4.2.0
collected 19 items                                                                                                                                                      

tests/test_pawpal.py ...................                                                                                                                          [100%]

========================================================================== 19 passed in 0.02s ===========================================================================
(base) harithaadhikarla@Mac ai110-module2show-pawp

**Confidence Level:** (4/5)
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

PawPal+'s scheduler includes four intelligent features:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks chronologically by time attribute |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name and/or completion status |
| Conflict detection | `Scheduler.detect_conflicts()` | Flags exact same-time-slot tasks across all pets |
| Recurring tasks | `Task.mark_complete()`, `Pet.complete_task()` | Auto-generates next occurrence for DAILY/WEEKLY tasks |

- **Sorting by time** — `Scheduler.sort_by_time()` orders all tasks chronologically by their `time` attribute, so the daily schedule always displays in the correct sequence regardless of the order tasks were added.
- **Filtering by pet or status** — `Scheduler.filter_tasks()` returns a subset of tasks filtered by `pet_name`, completion status, or both.
- **Conflict detection** — `Scheduler.detect_conflicts()` groups tasks by exact date and time, flagging any slot with two or more tasks and returning a human-readable warning instead of crashing. It only catches exact time matches, not overlapping durations.
- **Recurring tasks** — `Task.mark_complete()` and `Pet.complete_task()` work together so completing a `DAILY` or `WEEKLY` task automatically generates the next occurrence using `timedelta`.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

**Main UI features:**
- Add a new pet (name, species, breed)
- Add a care task to a specific pet (description, time, priority, frequency)
- View today's schedule, sorted chronologically
- Filter the schedule by pet or completion status
- See conflict warnings if two tasks are scheduled at the same time
- Mark tasks complete — recurring tasks automatically generate their next occurrence

**Example workflow:**
1. Add a pet (e.g., "Mochi", a Golden Retriever).
2. Add a task for that pet (e.g., "Morning walk" at 08:00, HIGH priority, DAILY frequency).
3. Add a second pet and a task at a conflicting time to see the conflict warning appear.
4. View "Today's Schedule" — tasks appear sorted by time, with a warning banner if any conflicts exist.
5. Filter the schedule by pet name or by incomplete tasks only.
6. Mark the "Morning walk" task complete — a new task for tomorrow is automatically created.

**Key Scheduler behaviors demonstrated:**
- `Scheduler.sort_by_time()` — chronological ordering
- `Scheduler.filter_tasks()` — filtering by pet/status
- `Scheduler.detect_conflicts()` — same-time-slot warnings
- `Task.mark_complete()` / `Pet.complete_task()` — automatic recurrence

**Sample CLI output** (from running `python main.py`):

\`\`\`
Today's Schedule:
07:00 - Grooming (Mochi) [MEDIUM]
07:00 - Vet visit (Biscuit) [HIGH]
08:00 - Morning walk (Mochi) [HIGH]
09:30 - Feeding (Biscuit) [MEDIUM]
12:15 - Litter change (Biscuit) [MEDIUM]
18:00 - Evening play (Mochi) [LOW]
22:30 - Night potty (Mochi) [MEDIUM]

Conflicts:
  Conflict at 07:00 on 2026-07-05: Grooming (Mochi) and Vet visit (Biscuit)
\`\`\`


**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
