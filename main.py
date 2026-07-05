from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    # 1. Create an Owner with available time constraint
    owner = Owner(name="Jordan", available_minutes=90)
    
    # 2. Create at least two Pets
    mochi = Pet(name="Mochi", species="Dog", breed="Golden Retriever", age=3)
    biscuit = Pet(name="Biscuit", species="Dog", breed="Corgi", age=1)
    
    owner.add_pet(mochi)
    owner.add_pet(biscuit)
    
    # 3. Add at least three Tasks with different times to those pets
    # Params: name, category, duration_minutes, priority, recurrence, time
    task1 = Task(
        name="Morning Walk", 
        category="Exercise", 
        duration_minutes=30, 
        priority="high", 
        recurrence="daily", 
        time="08:00"
    )
    task2 = Task(
        name="Breakfast Feeding", 
        category="Feeding", 
        duration_minutes=15, 
        priority="high", 
        recurrence="daily", 
        time="09:00"
    )
    task3 = Task(
        name="Grooming Session", 
        category="Grooming", 
        duration_minutes=45, 
        priority="medium", 
        recurrence="none", 
        time="14:00"
    )
    task4 = Task(
        name="Medication", 
        category="Health", 
        duration_minutes=10, 
        priority="high", 
        recurrence="daily", 
        time="20:00"
    )
    
    mochi.add_task(task1)
    mochi.add_task(task3)
    
    biscuit.add_task(task2)
    biscuit.add_task(task4)
    
    # 4. Initialize Scheduler and generate today's plan
    scheduler = Scheduler(owner=owner)
    scheduler.generate_plan()
    
    # 5. Print a "Today's Schedule" to the terminal
    print("=" * 60)
    print(f"📅 TODAY'S SCHEDULE FOR {owner.name.upper()}'S PETS")
    print(f"Total Available Owner Time: {owner.available_minutes} minutes")
    print("=" * 60)
    print(scheduler.explain_plan())
    print("=" * 60)

if __name__ == "__main__":
    main()
