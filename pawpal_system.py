"""PawPal+ class skeletons generated from diagrams/uml.mmd (structure only)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
from enum import Enum
from typing import List, Optional


class Priority(Enum):
    """Relative importance of a care task."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Frequency(Enum):
    """How often a care task recurs."""

    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class Task:
    """A single pet-care activity with timing, priority, and completion state."""

    description: str
    pet_name: str
    time: Optional[time] = None
    duration: int = 0
    priority: Priority = Priority.MEDIUM
    frequency: Frequency = Frequency.DAILY
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    """A pet's details and the list of care tasks it needs."""

    name: str
    species: str = ""
    breed: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet and stamp it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return this pet's list of tasks."""
        return self.tasks


@dataclass
class Owner:
    """A pet owner who manages one or more pets and views their tasks."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Append a pet to this owner's list of pets."""
        self.pets.append(pet)

    def view_all_tasks(self) -> List[Task]:
        """Collect and return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.get_tasks()]


class Scheduler:
    """Retrieves, organizes, and orders an owner's tasks into a daily schedule."""

    def get_tasks(self, owner: Owner) -> List[Task]:
        """Retrieve all of the owner's tasks via owner.view_all_tasks()."""
        return owner.view_all_tasks()

    def organize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Return the tasks sorted by their time field in ascending order."""
        return sorted(tasks, key=lambda task: (task.time is None, task.time))

    def generate_daily_schedule(self, owner: Owner) -> List[Task]:
        """Retrieve the owner's tasks and return them ordered by time."""
        tasks = self.get_tasks(owner)
        return self.organize_tasks(tasks)
