"""Simple tests for PawPal+ core behaviors."""

from datetime import date, datetime

from pawpal_system import Owner, Pet, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() flips a task's completed status to True."""
    task = Task("Walk", 30, date(2026, 7, 7))
    assert task.completed is False        # starts incomplete
    task.mark_complete()
    assert task.completed is True         # now marked done


def test_add_task_increases_pet_task_count():
    """Adding a task to a pet increases that pet's task count by one."""
    pet = Pet("Rex", "dog", 3)
    assert len(pet.tasks) == 0            # no tasks yet
    pet.add_task(Task("Feed", 15, date(2026, 7, 7)))
    assert len(pet.tasks) == 1            # count went up
def test_generate_schedule_orders_by_time():
    owner = Owner("Jane", "jane@email.com")

    dog = Pet("Martha", "Dog", 2)
    owner.add_pet(dog)

    late = Task(
        "Walk",
        30,
        date(2026, 7, 7),
        start_time=datetime(2026, 7, 7, 10, 0)
    )

    early = Task(
        "Breakfast",
        15,
        date(2026, 7, 7),
        start_time=datetime(2026, 7, 7, 8, 0)
    )

    owner.create_task(dog, late)
    owner.create_task(dog, early)

    schedule = owner.view_schedule()

    assert schedule[0].name == "Breakfast"
    assert schedule[1].name == "Walk"

if __name__ == "__main__":
    test_mark_complete_changes_status()
    test_add_task_increases_pet_task_count()
    print("All tests passed.")
