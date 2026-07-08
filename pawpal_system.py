#Where the back end logic lives

import calendar
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Optional
from uuid import uuid4


def _add_months(value, months: int):
    """Shift a date/datetime forward by whole months, clamping the day to the
    target month's length (e.g. Jan 31 + 1 month -> Feb 28)."""
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)


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

    def mark_complete(self, done: bool = True) -> Optional["Task"]:
        """Set completion status; on a fresh completion of a recurring task,
        spawn and return the next occurrence (attached to the same pet)."""
        was_completed = self.completed
        self.completed = done
        if done and not was_completed:
            nxt = self.next_occurrence()
            if nxt is not None:
                if self.pet is not None:
                    self.pet.add_task(nxt)
                return nxt
        return None

    def next_occurrence(self) -> Optional["Task"]:
        """Return a fresh, incomplete Task for this task's next cycle, or None
        if it does not recur ("once"). due_date and start_time advance by the
        frequency interval; identity/completion do not carry over."""
        if self.frequency == "daily":
            shift = lambda v: v + timedelta(days=1)
        elif self.frequency == "weekly":
            shift = lambda v: v + timedelta(weeks=1)
        elif self.frequency == "monthly":
            shift = lambda v: _add_months(v, 1)
        else:
            return None  # "once" or unknown cadence: no repeat
        return Task(
            name=self.name,
            duration=self.duration,
            due_date=shift(self.due_date),
            start_time=shift(self.start_time) if self.start_time else None,
            notes=self.notes,
            priority=self.priority,
            frequency=self.frequency,
            pet=self.pet,
        )

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

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        pet_name: Optional[str] = None,
    ) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name.

        Pass `completed` to keep only done/undone tasks, `pet_name` to keep
        only one pet's tasks; omit both to return everything. Filters combine.
        """
        tasks = self.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet is not None and t.pet.name == pet_name]
        return tasks

    def view_schedule(self) -> List[Task]:
        """Return the schedule the scheduler builds from all this owner's pets' tasks."""
        return self.scheduler.generate_schedule(self.pets)


@dataclass
class Scheduler:
    def collect_tasks(self, pets: List[Pet]) -> List[Task]:
        """Aggregate tasks across all pets (single source of truth stays on Pet)."""
        return [task for pet in pets for task in pet.tasks]

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered by start_time; unscheduled tasks (None) go last."""
        return sorted(
            tasks,
            key=lambda t: (t.start_time is None, t.start_time or datetime.max),
        )

    def detect_conflicts(self, pets: List[Pet]) -> List[str]:
        """Return warning messages for scheduled tasks whose time windows overlap.

        Lightweight and non-fatal: returns an empty list when there are no
        conflicts and never raises. Unscheduled or completed tasks are ignored.
        """
        scheduled = self.sort_by_time(
            [t for t in self.collect_tasks(pets)
             if not t.completed and t.start_time is not None]
        )
        warnings: List[str] = []
        for i, first in enumerate(scheduled):
            for second in scheduled[i + 1:]:
                # Sorted by start_time, so once a task starts at/after `first`
                # ends, nothing later can overlap it -- stop scanning early.
                if second.start_time >= first.end_time:
                    break
                if first.overlaps(second):
                    warnings.append(
                        f"WARNING: '{first.name}' "
                        f"({self._label(first)}) overlaps '{second.name}' "
                        f"({self._label(second)})"
                    )
        return warnings

    @staticmethod
    def _label(task: Task) -> str:
        """Short 'HH:MM-HH:MM, pet' descriptor used in conflict warnings."""
        pet_name = task.pet.name if task.pet else "?"
        span = f"{task.start_time:%H:%M}-{task.end_time:%H:%M}"
        return f"{span}, {pet_name}"

    def generate_schedule(self, pets: List[Pet]) -> List[Task]:
        """Return all incomplete tasks ordered by start time (unscheduled last)."""
        tasks = [t for t in self.collect_tasks(pets) if not t.completed]
        return self.sort_by_time(tasks)


    def view_schedule(self, pets: List[Pet]) -> None:
        """Print the day's schedule in time order, then list any time conflicts."""
        schedule = self.generate_schedule(pets)

        if not schedule:
            print("No tasks scheduled.")
            return

        print("Today's Schedule")
        print("-" * 50)

        for task in schedule:
            when = task.start_time.strftime("%I:%M %p")
            pet_name = task.pet.name if task.pet else "?"
            freq = "" if task.frequency == "once" else f", {task.frequency}"

            print(f"[{when}] {task.name} ({pet_name}, {task.duration}m{freq})")

        warnings = self.detect_conflicts(pets)

        if warnings:
            print("\nConflicts Detected")
            print("-" * 50)
            for warning in warnings:
                print(warning)
