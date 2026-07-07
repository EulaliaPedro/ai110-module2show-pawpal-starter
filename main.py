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
        start_time= datetime(2026, 7, 7, 9, 0),
        priority= 5, 
        frequency= "once"
    )

    buy_treats = Task(
        name="Buy more treats",
        duration= 20,
        due_date = date.today(),
        priority= 1, 
        frequency= "once"       
    )

    walk = Task(
        name= "Go on a walk",
        duration= 30,
        due_date = date.today(),
        start_time= time(11, 0),
        priority= 4, 
        frequency= "daily" 
    )

    owner.create_task(dog, walk)
    owner.create_task(hamster, vet)
    owner.create_task(hamster, buy_treats)
    
    # Print schedule 
    print("Today's Schedule")
    print("-"*50)
    owner.scheduler.view_schedule(owner.pets)

if __name__ == "__main__":
    main()
