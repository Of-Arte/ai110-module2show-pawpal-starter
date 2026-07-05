import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session State: Initialize Owner ---
if "owner" not in st.session_state:
    st.session_state.owner = None

st.divider()

# --- Owner Setup ---
st.subheader("👤 Owner Setup")
with st.form("owner_form"):
    owner_name = st.text_input("Owner name", value="Jordan")
    available_minutes = st.number_input("Available time today (minutes)", min_value=10, max_value=480, value=90)
    submit_owner = st.form_submit_button("Set Owner")

if submit_owner:
    st.session_state.owner = Owner(name=owner_name, available_minutes=int(available_minutes))
    st.success(f"Owner '{owner_name}' set with {available_minutes} minutes available.")

if st.session_state.owner is None:
    st.info("Please set an owner above to get started.")
    st.stop()

owner = st.session_state.owner

st.divider()

# --- Add a Pet ---
st.subheader("🐾 Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="Golden Retriever")
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
    submit_pet = st.form_submit_button("Add Pet")

if submit_pet:
    new_pet = Pet(name=pet_name, species=species, breed=breed, age=int(age))
    owner.add_pet(new_pet)
    st.success(f"Pet '{pet_name}' added to {owner.name}'s profile!")

pets = owner.get_pets()
if pets:
    st.markdown(f"**{owner.name}'s Pets:** " + ", ".join(p.name for p in pets))
else:
    st.info("No pets added yet. Add one above.")

st.divider()

# --- Add a Task ---
st.subheader("📋 Schedule a Task")
if not pets:
    st.warning("Add a pet first before scheduling tasks.")
else:
    with st.form("add_task_form"):
        col1, col2 = st.columns(2)
        with col1:
            selected_pet_name = st.selectbox("Select pet", [p.name for p in pets])
            task_name = st.text_input("Task name", value="Morning Walk")
            category = st.selectbox("Category", ["Exercise", "Feeding", "Grooming", "Health", "Other"])
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
            recurrence = st.selectbox("Recurrence", ["daily", "weekly", "none"])
            time = st.text_input("Time (HH:MM)", value="08:00")
        submit_task = st.form_submit_button("Add Task")

    if submit_task:
        # Find the selected pet and call add_task()
        selected_pet = next(p for p in pets if p.name == selected_pet_name)
        new_task = Task(
            name=task_name,
            category=category,
            duration_minutes=int(duration),
            priority=priority,
            recurrence=recurrence,
            time=time
        )
        selected_pet.add_task(new_task)
        st.success(f"Task '{task_name}' added to {selected_pet_name}'s schedule!")

    # Show current tasks per pet
    for pet in pets:
        tasks = pet.get_tasks()
        if tasks:
            with st.expander(f"{pet.name}'s Tasks ({len(tasks)})"):
                for t in tasks:
                    status = "✅" if t.completed else "⏳"
                    st.write(f"{status} **{t.name}** — {t.time} | {t.duration_minutes} min | Priority: {t.priority}")

st.divider()

# --- Generate Schedule ---
st.subheader("📅 Generate Today's Schedule")
if st.button("Generate schedule", id="generate_schedule_btn"):
    scheduler = Scheduler(owner=owner)
    plan = scheduler.generate_plan()

    if plan:
        st.success("Schedule generated!")
        st.text(scheduler.explain_plan())
    else:
        st.warning("No tasks due today or all tasks already completed.")

    if scheduler.skipped_tasks:
        st.info(f"{len(scheduler.skipped_tasks)} task(s) were skipped due to time limits.")
