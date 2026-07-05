import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler, Priority, Frequency

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+ — a pet care planning assistant.

Add your pets and their care tasks below, then generate a daily schedule ordered by time.
The scheduling logic lives in `pawpal_system.py`; this app is the interactive demo on top of it.
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

# Persist a single Owner across Streamlit reruns so pets/tasks accumulate
# instead of being rebuilt from scratch every time the script re-runs.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
owner = st.session_state.owner

# Owner name stays in sync with the text box.
owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Pets")
pcol1, pcol2 = st.columns([2, 1])
with pcol1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with pcol2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if new_pet_name.strip():
        owner.add_pet(Pet(name=new_pet_name.strip(), species=new_pet_species))
    else:
        st.warning("Give the pet a name first.")

if owner.pets:
    st.caption("Current pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above to get started.")

st.markdown("### Tasks")

# Map the UI's priority label onto the Priority enum from the logic layer.
PRIORITY_LABELS = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}

if owner.pets:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        priority_label = st.selectbox("Priority", list(PRIORITY_LABELS), index=2)
    with col4:
        task_pet_name = st.selectbox("For pet", [p.name for p in owner.pets])

    task_time = st.time_input("Time")

    if st.button("Add task"):
        # Find the selected pet and attach the task to it.
        pet = next(p for p in owner.pets if p.name == task_pet_name)
        pet.add_task(
            Task(
                description=task_title,
                pet_name=pet.name,
                time=task_time,
                duration=int(duration),
                priority=PRIORITY_LABELS[priority_label],
            )
        )

    all_tasks = owner.view_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table(
            [
                {
                    "time": t.time.strftime("%H:%M") if t.time else "--",
                    "task": t.description,
                    "pet": t.pet_name,
                    "priority": t.priority.name,
                    "duration": t.duration,
                }
                for t in all_tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.caption("Add a pet before adding tasks.")

st.divider()

st.subheader("Daily Schedule")

scheduler = Scheduler()
# Ordered chronologically (timeless tasks last) via the scheduling logic layer.
schedule = scheduler.generate_daily_schedule(owner)

if not schedule:
    st.info("Nothing to schedule yet. Add some pets and tasks first.")
else:
    st.write(f"**Today's Schedule for {owner.name}:**")

    # Surface double-bookings first, before the owner scans the full table.
    # Conflicts are computed on the whole day's tasks, not the filtered view.
    conflicts = scheduler.detect_conflicts(schedule)
    if conflicts:
        for warning in conflicts:
            st.warning(f"⚠️ {warning}")
    else:
        st.success("No scheduling conflicts today!")

    # Filter controls — narrow the displayed tasks without touching the schedule.
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        pet_options = ["All pets"] + [p.name for p in owner.pets]
        selected_pet = st.selectbox("Filter by pet", pet_options)
    with fcol2:
        status_choice = st.radio(
            "Completion status",
            ["All", "Completed", "Not completed"],
            horizontal=True,
        )

    pet_filter = None if selected_pet == "All pets" else selected_pet
    completed_filter = {"All": None, "Completed": True, "Not completed": False}[
        status_choice
    ]

    visible = scheduler.filter_tasks(
        schedule, pet_name=pet_filter, completed=completed_filter
    )

    if visible:
        st.table(
            [
                {
                    "time": t.time.strftime("%H:%M") if t.time else "--:--",
                    "task": t.description,
                    "pet": t.pet_name,
                    "priority": t.priority.name,
                    "duration": t.duration,
                    "done": "✓" if t.completed else "",
                }
                for t in visible
            ]
        )
    else:
        st.info("No tasks match the current filters.")
