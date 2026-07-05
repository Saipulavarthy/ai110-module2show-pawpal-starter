"""PawPal+ class skeletons generated from diagrams/uml.mmd (structure only)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, time, timedelta
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
    date: date = field(default_factory=date.today)
    duration: int = 0
    priority: Priority = Priority.MEDIUM
    frequency: Frequency = Frequency.DAILY
    completed: bool = False

    def mark_complete(self) -> Optional["Task"]:
        """Mark done; for DAILY/WEEKLY return the next occurrence (date advanced), else None."""
        self.completed = True
        if self.frequency is Frequency.DAILY:
            next_date = self.date + timedelta(days=1)
        elif self.frequency is Frequency.WEEKLY:
            next_date = self.date + timedelta(weeks=1)
        else:
            return None
        return Task(
            description=self.description,
            pet_name=self.pet_name,
            time=self.time,
            date=next_date,
            duration=self.duration,
            priority=self.priority,
            frequency=self.frequency,
            completed=False,
        )


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

    def complete_task(self, task: Task) -> Optional[Task]:
        """Complete a task; if it recurs, append and return the next occurrence, else None."""
        next_task = task.mark_complete()
        if next_task is not None:
            self.tasks.append(next_task)
        return next_task


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
        """Return the tasks sorted ascending by time (timeless tasks last)."""
        return sorted(tasks, key=lambda task: (task.time is None, task.time))

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return a new list of tasks sorted ascending by time (timeless tasks last)."""
        return sorted(tasks, key=lambda task: (task.time is None, task.time))

    def filter_tasks(
        self,
        tasks: List[Task],
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> List[Task]:
        """Return tasks matching pet_name and/or completed, or all tasks if both are None."""
        return [
            task
            for task in tasks
            if (pet_name is None or task.pet_name == pet_name)
            and (completed is None or task.completed == completed)
        ]

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warnings for tasks sharing an exact date+time (exact matches only, not overlapping ranges)."""
        by_slot: dict[tuple[date, time], list[Task]] = defaultdict(list)
        for task in tasks:
            if task.time is None:
                continue
            by_slot[(task.date, task.time)].append(task)

        warnings: List[str] = []
        for (slot_date, slot_time), clashing in sorted(by_slot.items()):
            if len(clashing) < 2:
                continue
            names = " and ".join(f"{t.description} ({t.pet_name})" for t in clashing)
            warnings.append(
                f"Conflict at {slot_time.strftime('%H:%M')} on {slot_date}: {names}"
            )
        return warnings

    def generate_daily_schedule(self, owner: Owner) -> List[Task]:
        """Retrieve the owner's tasks and return them ordered by time."""
        tasks = self.get_tasks(owner)
        return self.organize_tasks(tasks)
