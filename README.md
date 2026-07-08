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

    Today's Schedule
    --------------------------------------------------
    [2026-07-07 09:00] Vet Appointment (Billy, 60m)
    [2026-07-07 11:00] Go on a walk (Martha, 30m)
    [unscheduled] Buy more treats (Billy, 20m)

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
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================================== \test session starts ==============================================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Desktop\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 3 items


tests\test_pawpal.py ...                                                                                     [100%]

================================================ 3 passed in 0.07s ================================================


# Paste your pytest output here
```

platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Desktop\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0, cov-7.1.0
collected 3 items

tests\test_pawpal.py ... [100%]

====================================== tests coverage =======================================
****\*\*****\_\_****\*\***** coverage: platform win32, python 3.14.3-final-0 ****\*\*****\_\_****\*\*****

## Name Stmts Miss Cover

pawpal_system.py 126 61 52%
tests\test_pawpal.py 27 3 89%

---

TOTAL 153 64 58%
===================================== 3 passed in 0.20s =====================================

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature           | Method(s)             | Notes                        |
| ----------------- | --------------------- | ---------------------------- |
| Task sorting      | sort_by_time(...)     | by priority, by the due date |
| Filtering         | filter_tasks(...)     | by completion                |
| Conflict handling | detect_conflicts(...) | Error warning                |
| Recurring tasks   | next_occurrence(...)  | daily vs. weekly vs. monthly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- First step to is enter the owner (users) name and email adress -->
2. <!-- Next user has to enter their pet information (name, specices, age) and add the pet -->
3. <!-- User creates tasks for one or more pets -->
4. <!-- Can then  view the current tasks -->
5. <!-- user can generate the schedule for the day -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
