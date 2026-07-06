#Where the back end logic lives

from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Task:
    name: str
    duration: int          # minutes
    due_date: date
    notes: str = ""
    priority: int = 0

    def edit(self, **details) -> None:
        """Update task fields (name, duration, due_date, notes, priority)."""
        ...


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        ...

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        ...


@dataclass
class Owner:
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        ...

    def create_task(self, pet: Pet, task: Task) -> None:
        """Create a task and assign it to one of the owner's pets."""
        ...

    def view_schedule(self) -> List[Task]:
        """Return the generated schedule (ordered tasks) for this owner's pets."""
        ...


@dataclass
class Scheduler:
    tasks: List[Task] = field(default_factory=list)

    def generate_schedule(self) -> List[Task]:
        """Build a schedule (ordered tasks) from the tasks based on constraints/preferences."""
        ...

    def view_schedule(self) -> None:
        """Display the generated schedule."""
        ...
