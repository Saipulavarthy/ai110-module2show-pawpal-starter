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

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    schedule = scheduler.generate_daily_schedule(owner)
    if schedule:
        st.write(f"**Today's Schedule for {owner.name}:**")
        for t in schedule:
            slot = t.time.strftime("%H:%M") if t.time else "--:--"
            st.write(f"{slot} — {t.description} ({t.pet_name}) [{t.priority.name}]")
    else:
        st.info("Nothing to schedule yet. Add some pets and tasks first.")
