"""PawPal+ class skeletons generated from diagrams/uml.mmd (structure only)."""

from __future__ import annotations

from dataclasses import dataclass, field
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
    time: Optional[str] = None
    duration: int = 0
    priority: Priority = Priority.MEDIUM
    frequency: Frequency = Frequency.DAILY
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        # TODO: implement
        pass


@dataclass
class Pet:
    """A pet's details and the list of care tasks it needs."""

    name: str
    species: str = ""
    breed: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        # TODO: implement
        pass

    def get_tasks(self) -> List[Task]:
        """Return this pet's tasks."""
        # TODO: implement
        pass


@dataclass
class Owner:
    """A pet owner who manages one or more pets and views their tasks."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        # TODO: implement
        pass

    def view_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        # TODO: implement
        pass


class Scheduler:
    """Retrieves, organizes, and orders an owner's tasks into a daily schedule."""

    def get_tasks(self, owner: Owner) -> List[Task]:
        """Collect all tasks belonging to an owner."""
        # TODO: implement
        pass

    def organize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Order tasks (e.g., by priority and time)."""
        # TODO: implement
        pass

    def generate_daily_schedule(self, owner: Owner) -> List[Task]:
        """Produce an ordered daily schedule for an owner."""
        # TODO: implement
        pass
