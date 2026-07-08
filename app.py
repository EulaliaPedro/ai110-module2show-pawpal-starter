from datetime import date, datetime

import streamlit as st
from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")

owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@pawpal.app")

# Persist the Owner across reruns: Streamlit re-runs this script top-to-bottom on
# every interaction, so only create the Owner if one isn't already in the session
# vault. Otherwise reuse the stored object so its pets/tasks survive navigation.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, email=owner_email)
owner = st.session_state.owner

# The stored object is only created once, so refresh its editable fields from the
# inputs without replacing it (pets/tasks stay attached to the same Owner).
owner.name = owner_name
owner.email = owner_email

st.caption(
    f"Persisted owner: {owner.name} · {len(owner.pets)} pet(s) · "
    f"{len(owner.get_all_tasks())} task(s) in session"
)

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age", min_value=0, max_value=50, value=1)

if st.button("Add Pet"):

    if any(p.name == pet_name for p in owner.pets):
        st.warning("That pet already exists.")

    else:
        pet = Pet(
            name=pet_name,
            species=species,
            age=age
        )

        owner.add_pet(pet)

        st.success(f"{pet.name} has been added!")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

task_date = st.date_input("Task Date")
task_time = st.time_input("Start Time")
frequency = st.selectbox(
    "Frequency",
    ["once", "daily", "weekly", "monthly"]
)

if owner.pets:
    selected_pet_name = st.selectbox(
        "Assign task to",
        [pet.name for pet in owner.pets]
    )

    selected_pet = next(
        pet for pet in owner.pets
        if pet.name == selected_pet_name
    )

    if st.button("Add task"):
        start = datetime.combine(task_date, task_time)

        task = Task(
            name=task_title,
            duration=int(duration),
            due_date=task_date,
            start_time=start,
            priority={"low": 1, "medium": 2, "high": 3}[priority],
            frequency=frequency
        )

        owner.create_task(selected_pet, task)

        st.success(f"{task.name} added for {selected_pet.name}")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": task.pet.name if task.pet else "?",
                "task": task.name,
                "duration_minutes": task.duration,
                "priority": task.priority,
                "done": task.completed,
            }
            for task in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

st.divider()

st.subheader("Today's Schedule")

if st.button("Generate Schedule"):

    schedule = owner.view_schedule()

    if not schedule:
        st.info("No tasks to schedule.")

    else:

        st.success("Schedule Generated!")

        for task in schedule:

            when = task.start_time.strftime("%I:%M %p")

            st.markdown(
                f"**{when}** — {task.name} "
                f"({task.pet.name}, {task.duration} min)"
            )

        warnings = owner.scheduler.detect_conflicts(owner.pets)

        if warnings:

            st.warning("Scheduling Conflicts")

            for warning in warnings:
                st.write(warning)