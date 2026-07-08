# testing grounds 
from pawpal_system import Owner, Pet, Task
from datetime import date, datetime

def main():
    # Create an Owner
    owner = Owner(
        name="Jane Doe", 
        email="janeDoe@email.com"
    )


    # Create two Pet objects
    dog = Pet(
        name="Martha",
        species= "Dog",
        age= 2
    )
    hamster = Pet(
        name="Billy",
        species= "Hamster",
        age= 1
    )

    owner.add_pet(dog)
    owner.add_pet(hamster)

    # Create tasks
    vet = Task(
        name="Vet Appointment",
        duration= 60,
        due_date = date.today(),
        start_time= datetime(2026, 7, 8, 9, 0),
        priority= 5, 
        frequency= "once"
    )

    buy_treats = Task(
        name="Buy more treats",
        duration= 20,
        due_date = date.today(),
        start_time=datetime(2026, 7, 7, 11, 0),
        priority= 1, 
        frequency= "once"       
    )

    walk = Task(
        name= "Go on a walk",
        duration= 30,
        due_date = date.today(),
        start_time= datetime(2026, 7, 8, 9, 0),
        priority= 4, 
        frequency= "daily" 
    )

    # Add tasks out of order (walk 11:00 before vet 9:00) to show the
    # scheduler sorts them chronologically regardless of insertion order.
    owner.create_task(dog, walk)          # 11:00
    owner.create_task(hamster, buy_treats)  # unscheduled
    owner.create_task(hamster, vet)       # 9:00

    # Mark a task done, then demonstrate filtering by status and by pet.
    buy_treats.mark_complete()
    print("\nAll Pet Tasks")
    print("-" * 50)

    for pet in owner.pets:
        print(f"\n{pet.name}'s Tasks:")

        # Sort this pet's tasks by time
        pet_tasks = sorted(pet.tasks, key=lambda t: t.start_time)

        for task in pet_tasks:
            when = task.start_time.strftime("%I:%M %p")
            status = " (Completed)" if task.completed else ""
            print(f"[{when}] {task.name}{status}")  

    # Check for conflicts
    warnings = owner.scheduler.detect_conflicts(owner.pets)

    if warnings:
        print("\nConflicts Detected")
        print("-" * 50)
        for warning in warnings:
            print(warning)
    else:
        print("\nNo scheduling conflicts.")
#    print("\nBilly's tasks")
#    print("-"*50)
 #   for task in owner.filter_tasks(pet_name="Billy"):
 #       status = " (Completed)" if task.completed else ""
 #       print(f"{task.name}{status}")

 #   print("\nCompleted tasks")
 #   print("-"*50)
#    for task in owner.filter_tasks(completed=True):
 #       print(f"{task.name} ({task.pet.name})")

if __name__ == "__main__":
    main()
