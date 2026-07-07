#Where the back end logic lives

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Optional
from uuid import uuid4


@dataclass
class Task:
    name: str
    duration: int                     # minutes
    due_date: date
    start_time: Optional[datetime] = None   # when the task is scheduled; None until placed
    notes: str = ""
    priority: int = 0                 # convention: higher value = more urgent
    frequency: str = "once"           # "once", "daily", "weekly", "monthly"
    completed: bool = False           # completion status
    task_id: str = field(default_factory=lambda: uuid4().hex)  # stable identity
    # Back-reference to the owning pet; excluded from eq/repr to avoid recursion.
    pet: Optional["Pet"] = field(default=None, repr=False, compare=False)

    @property
    def end_time(self) -> Optional[datetime]:
        """When the task finishes, or None if it has no start_time."""
        if self.start_time is None:
            return None
        return self.start_time + timedelta(minutes=self.duration)

    def edit(self, **details) -> None:
        """Update whitelisted task fields from keyword arguments."""
        allowed = {"name", "duration", "due_date", "start_time", "notes",
                   "priority", "frequency", "completed"}
        for key, value in details.items():
            if key not in allowed:
                raise AttributeError(f"Task has no editable field {key!r}")
            setattr(self, key, value)

    def mark_complete(self, done: bool = True) -> None:
        """Set the task's completion status."""
        self.completed = done

    def overlaps(self, other: "Task") -> bool:
        """Return True if this task's scheduled time window collides with another's."""
        if self.start_time is None or other.start_time is None:
            return False
        return self.start_time < other.end_time and other.start_time < self.end_time


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet and set its back-reference."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet by task_id."""
        self.tasks = [t for t in self.tasks if t.task_id != task.task_id]


@dataclass
class Owner:
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)
    scheduler: "Scheduler" = field(default_factory=lambda: Scheduler())  # Owner uses a Scheduler

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        if pet not in self.pets:
            self.pets.append(pet)

    def create_task(self, pet: Pet, task: Task) -> None:
        """Create a task and assign it to one of the owner's pets."""
        if pet not in self.pets:
            raise ValueError(f"{pet.name} is not one of {self.name}'s pets")
        pet.add_task(task)
        
    def get_all_tasks(self) -> List[Task]:
        """Return all tasks for every pet owned by this owner."""
        return [task for pet in self.pets for task in pet.tasks]

    def view_schedule(self) -> List[Task]:
        """Return the schedule the scheduler builds from all this owner's pets' tasks."""
        return self.scheduler.generate_schedule(self.pets)


@dataclass
class Scheduler:
    def collect_tasks(self, pets: List[Pet]) -> List[Task]:
        """Aggregate tasks across all pets (single source of truth stays on Pet)."""
        return [task for pet in pets for task in pet.tasks]

    def generate_schedule(self, pets: List[Pet]) -> List[Task]:
        """Build an ordered schedule from the pets' tasks, resolving overlaps by priority."""
        tasks = [t for t in self.collect_tasks(pets) if not t.completed]
        scheduled = sorted(
            (t for t in tasks if t.start_time is not None),
            key=lambda t: t.start_time,
        )
        unscheduled = [t for t in tasks if t.start_time is None]

        placed: List[Task] = []
        for task in scheduled:
            conflict = next((p for p in placed if p.overlaps(task)), None)
            if conflict is None:
                placed.append(task)
            elif task.priority > conflict.priority:
                # New task wins the slot; the previous occupant is deferred.
                placed.remove(conflict)
                placed.append(task)
                unscheduled.append(conflict)
            else:
                unscheduled.append(task)

        unscheduled.sort(key=lambda t: (-t.priority, t.due_date))
        return placed + unscheduled

    def view_schedule(self, pets: List[Pet]) -> None:
        """Display the generated schedule."""
        schedule = self.generate_schedule(pets)
        if not schedule:
            print("No tasks scheduled.")
            return
        for task in schedule:
            when = task.start_time.strftime("%Y-%m-%d %H:%M") if task.start_time else "unscheduled"
            pet_name = task.pet.name if task.pet else "?"
            freq = "" if task.frequency == "once" else f", {task.frequency}"
            print(f"[{when}] {task.name} ({pet_name}, {task.duration}m, p{task.priority}{freq})")
