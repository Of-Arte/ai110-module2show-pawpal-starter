import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+ Smart Pet Scheduler", page_icon="🐾", layout="wide")

# Custom CSS for card aesthetic
st.markdown("""
<style>
.stMetric {
    background-color: rgba(240, 242, 246, 0.5);
    padding: 15px;
    border-radius: 10px;
    border: 1px solid rgba(220, 224, 230, 0.8);
}
</style>
""", unsafe_allow_html=True)

st.title("🐾 PawPal+ Smart Pet Scheduler")
st.markdown("Optimize your pet care schedule, handle time limits, and resolve conflicts instantly.")

# --- Session State Initialize ---
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Demo Data Loader helper ---
def load_demo_data():
    owner = Owner(name="Jordan", available_minutes=120)
    
    mochi = Pet(name="Mochi", species="dog", breed="Golden Retriever", age=3)
    biscuit = Pet(name="Biscuit", species="dog", breed="Corgi", age=1)
    
    owner.add_pet(mochi)
    owner.add_pet(biscuit)
    
    # Add Mochi's tasks
    mochi.add_task(Task(name="Morning Walk", category="Exercise", duration_minutes=30, priority="high", recurrence="daily", time="08:00"))
    mochi.add_task(Task(name="Playtime", category="Exercise", duration_minutes=20, priority="medium", recurrence="none", time="08:15"))
    mochi.add_task(Task(name="Grooming Session", category="Grooming", duration_minutes=45, priority="medium", recurrence="none", time="14:00"))
    mochi.add_task(Task(name="Evening Brush", category="Grooming", duration_minutes=10, priority="low", recurrence="daily", time="19:00"))
    
    # Add Biscuit's tasks
    biscuit.add_task(Task(name="Breakfast Feeding", category="Feeding", duration_minutes=15, priority="high", recurrence="daily", time="09:00"))
    biscuit.add_task(Task(name="Medication", category="Health", duration_minutes=10, priority="high", recurrence="daily", time="20:00"))
    
    st.session_state.owner = owner

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Demo Data Button
    if st.button("✨ Load Demo Data"):
        load_demo_data()
        st.success("Demo data loaded successfully!")
        st.rerun()
        
    st.divider()
    
    # Owner Setup
    st.subheader("👤 Owner Setup")
    owner_name_val = "Jordan"
    available_mins_val = 90
    if st.session_state.owner:
        owner_name_val = st.session_state.owner.name
        available_mins_val = st.session_state.owner.available_minutes
        
    with st.form("owner_form"):
        owner_name = st.text_input("Owner name", value=owner_name_val)
        available_minutes = st.number_input("Available time today (minutes)", min_value=10, max_value=480, value=available_mins_val)
        submit_owner = st.form_submit_button("Save Setup")
        
    if submit_owner:
        if st.session_state.owner:
            st.session_state.owner.name = owner_name
            st.session_state.owner.available_minutes = int(available_minutes)
        else:
            st.session_state.owner = Owner(name=owner_name, available_minutes=int(available_minutes))
        st.success(f"Owner '{owner_name}' saved!")
        st.rerun()

    if st.session_state.owner:
        owner = st.session_state.owner
        st.divider()
        
        # Add a Pet
        st.subheader("🐾 Add a Pet")
        with st.form("add_pet_form", clear_on_submit=True):
            pet_name = st.text_input("Pet name", value="Mochi")
            species = st.selectbox("Species", ["dog", "cat", "other"])
            breed = st.text_input("Breed", value="Golden Retriever")
            age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
            submit_pet = st.form_submit_button("Add Pet")

        if submit_pet:
            new_pet = Pet(name=pet_name, species=species, breed=breed, age=int(age))
            owner.add_pet(new_pet)
            st.success(f"Pet '{pet_name}' added!")
            st.rerun()

        pets = owner.get_pets()
        if pets:
            st.divider()
            st.subheader("📋 Schedule a Task")
            with st.form("add_task_form", clear_on_submit=True):
                selected_pet_name = st.selectbox("Select pet", [p.name for p in pets])
                task_name = st.text_input("Task name", value="Morning Walk")
                category = st.selectbox("Category", ["Exercise", "Feeding", "Grooming", "Health", "Other"])
                duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
                priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
                recurrence = st.selectbox("Recurrence", ["daily", "weekly", "none"])
                time = st.text_input("Time (HH:MM)", value="08:00")
                submit_task = st.form_submit_button("Add Task")

            if submit_task:
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
                st.success(f"Task '{task_name}' added to {selected_pet_name}!")
                st.rerun()

# --- Main Panel ---
if st.session_state.owner is None:
    st.info("👈 Please set an owner or load the demo data in the sidebar to get started.")
    st.stop()

owner = st.session_state.owner
pets = owner.get_pets()

# Profile Header
st.subheader(f"👤 {owner.name}'s Profile")
if pets:
    st.markdown(f"**Pets:** " + ", ".join(f"**{p.name}** ({p.species.capitalize()})" for p in pets))
else:
    st.info("No pets added yet. Add a pet in the sidebar or click 'Load Demo Data' to see it in action.")
    st.stop()

# Generate schedule using Scheduler
scheduler = Scheduler(owner=owner)
plan = scheduler.generate_plan()

st.divider()

# --- Metrics Dashboard ---
st.header("📊 Schedule Overview")
col_t1, col_t2, col_t3, col_t4 = st.columns(4)

total_available = owner.available_minutes
total_scheduled = sum(t.duration_minutes for t in plan)
completed_tasks = [t for t in plan if t.completed]
completion_pct = (len(completed_tasks) / len(plan) * 100) if plan else 0.0

with col_t1:
    st.metric(label="Owner Available Time", value=f"{total_available} mins")
with col_t2:
    st.metric(label="Total Scheduled Time", value=f"{total_scheduled} mins", delta=f"{total_available - total_scheduled} left")
with col_t3:
    st.metric(label="Tasks Count", value=f"{len(plan)} active")
with col_t4:
    st.metric(label="Completion Rate", value=f"{completion_pct:.1f}%")

# --- Conflicts section ---
conflicts = getattr(scheduler, "conflicts", [])
if conflicts:
    st.subheader("⚠️ Schedule Conflicts Detected")
    for task_a, task_b in conflicts:
        pet_a = scheduler.get_pet_for_task(task_a)
        pet_b = scheduler.get_pet_for_task(task_b)
        st.warning(
            f"⚡ **Conflict:** '{task_a.name}' for **{pet_a}** ({task_a.time}, {task_a.duration_minutes}m) "
            f"overlaps with '{task_b.name}' for **{pet_b}** ({task_b.time}, {task_b.duration_minutes}m)."
        )

# --- Today's Active Schedule ---
st.divider()
st.header("📅 Today's Smart Schedule")
if not plan:
    st.info("No tasks scheduled for today. Increase available time or add tasks.")
else:
    # Render interactive list
    # Sort chronologically by time for display
    display_tasks = sorted(plan, key=lambda t: t.time)
    
    # Custom interactive table layout using columns
    cols_hdr = st.columns([1, 1.5, 3, 2, 1.5, 1.5, 1.5, 2])
    cols_hdr[0].markdown("**Time**")
    cols_hdr[1].markdown("**Pet**")
    cols_hdr[2].markdown("**Task**")
    cols_hdr[3].markdown("**Category**")
    cols_hdr[4].markdown("**Duration**")
    cols_hdr[5].markdown("**Priority**")
    cols_hdr[6].markdown("**Recurrence**")
    cols_hdr[7].markdown("**Action**")
    
    for idx, t in enumerate(display_tasks):
        p_name = scheduler.get_pet_for_task(t)
        cols = st.columns([1, 1.5, 3, 2, 1.5, 1.5, 1.5, 2])
        
        prio_color = "🔴" if t.priority == "high" else ("🟡" if t.priority == "medium" else "🟢")
        prio_str = f"{prio_color} {t.priority.capitalize()}"
        
        cols[0].write(t.time)
        cols[1].write(p_name)
        
        if t.completed:
            cols[2].markdown(f"~~{t.name}~~")
            cols[3].markdown(f"~~{t.category}~~")
            cols[4].markdown(f"~~{t.duration_minutes} min~~")
            cols[5].markdown(f"~~{prio_str}~~")
            cols[6].markdown(f"~~{t.recurrence.capitalize()}~~")
            cols[7].markdown("✅ **Completed**")
        else:
            cols[2].write(t.name)
            cols[3].write(t.category)
            cols[4].write(f"{t.duration_minutes} min")
            cols[5].write(prio_str)
            cols[6].write(t.recurrence.capitalize())
            
            btn_key = f"comp_{p_name}_{t.name}_{t.time}_{idx}"
            if cols[7].button("Complete", key=btn_key):
                target_pet = next(p for p in pets if p.name == p_name)
                success = target_pet.mark_task_complete(t.name)
                if success:
                    st.success(f"Marked '{t.name}' as complete!")
                    st.rerun()

# --- Skipped Tasks ---
if scheduler.skipped_tasks:
    st.divider()
    st.subheader("🚫 Skipped Tasks (Exceeded Available Time)")
    st.info("The following tasks were skipped because they exceed your daily available minutes:")
    
    skipped_data = []
    for t in scheduler.skipped_tasks:
        p_name = scheduler.get_pet_for_task(t)
        skipped_data.append({
            "Pet": p_name,
            "Task Name": t.name,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority.capitalize(),
            "Time": t.time
        })
    st.table(skipped_data)

# --- Filter & Analysis Section ---
st.divider()
st.header("🔍 Filter & Analyze Schedule")
col_f1, col_f2 = st.columns(2)

with col_f1:
    filter_pet = st.selectbox("Filter by Pet", ["All Pets"] + [p.name for p in pets])
with col_f2:
    filter_status = st.selectbox("Filter by Status", ["All Statuses", "Pending", "Completed"])

# Combine filter methods from Scheduler
filtered_tasks = plan

if filter_pet != "All Pets":
    filtered_tasks = scheduler.filter_by_pet(filter_pet)

if filter_status == "Pending":
    status_tasks = scheduler.filter_by_status(completed=False)
    filtered_tasks = [t for t in filtered_tasks if t in status_tasks]
elif filter_status == "Completed":
    status_tasks = scheduler.filter_by_status(completed=True)
    filtered_tasks = [t for t in filtered_tasks if t in status_tasks]

if filtered_tasks:
    filtered_table = []
    for t in sorted(filtered_tasks, key=lambda t: t.time):
        p_name = scheduler.get_pet_for_task(t)
        filtered_table.append({
            "Time": t.time,
            "Pet": p_name,
            "Task": t.name,
            "Category": t.category,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority.capitalize(),
            "Recurrence": t.recurrence.capitalize(),
            "Completed": "Yes ✅" if t.completed else "No ⏳"
        })
    st.table(filtered_table)
else:
    st.info("No tasks found matching the filter criteria.")

# --- How sorting works ---
with st.expander("ℹ️ Learn How the Scheduler Sorts and Selects"):
    st.markdown("""
    The `Scheduler` runs an algorithmic sorting phase before selecting which tasks fit in your day:
    1. **Priority Sorting**: Tasks are sorted by priority (High ➡️ Medium ➡️ Low).
    2. **Time Sorting**: Within the same priority, tasks are sorted chronologically by scheduled time.
    3. **Greedy Allocation**: Tasks are scheduled one by one in this sorted order. If a task exceeds the remaining available owner time, it is skipped.
    
    Here is the pre-filtered, sorted list of all due tasks today (run through `Scheduler.sort_tasks`):
    """)
    all_due_tasks = [t for t in owner.get_all_tasks() if not t.completed and t.is_due_today()]
    if all_due_tasks:
        sorted_due = scheduler.sort_tasks(all_due_tasks)
        sort_table = []
        for t in sorted_due:
            p_name = scheduler.get_pet_for_task(t)
            sort_table.append({
                "Priority": t.priority.capitalize(),
                "Time": t.time,
                "Pet": p_name,
                "Task": t.name,
                "Duration (min)": t.duration_minutes
            })
        st.table(sort_table)
    else:
        st.write("No due tasks left to sort today.")
