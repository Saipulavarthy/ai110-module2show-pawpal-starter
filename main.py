"""CLI demo for the PawPal+ logic layer — verifies pawpal_system.py works end to end."""

from datetime import time

from pawpal_system import Owner, Pet, Task, Scheduler, Priority, Frequency


def main() -> None:
    # One owner with two pets.
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="dog", breed="Shiba Inu")
    biscuit = Pet(name="Biscuit", species="cat", breed="Tabby")
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    # A handful of tasks with different times and priorities, spread across pets.
    # Deliberately added OUT of chronological order to show sort_by_time() working.
    # add_task() stamps each task's pet_name, so it's left blank here.
    mochi.add_task(
        Task("Evening play", pet_name="", time=time(18, 0),
             duration=20, priority=Priority.LOW, frequency=Frequency.DAILY)
    )
    biscuit.add_task(
        Task("Feeding", pet_name="", time=time(9, 30),
             duration=10, priority=Priority.MEDIUM)
    )
    mochi.add_task(
        Task("Morning walk", pet_name="", time=time(8, 0),
             duration=30, priority=Priority.HIGH)
    )
    biscuit.add_task(
        Task("Litter change", pet_name="", time=time(12, 15),
             duration=5, priority=Priority.MEDIUM)
    )
    mochi.add_task(
        Task("Night potty", pet_name="", time=time(22, 30),
             duration=10, priority=Priority.MEDIUM)
    )

    # Two tasks at the SAME date+time for DIFFERENT pets, to show detect_conflicts()
    # catches cross-pet clashes. (date defaults to today for both, so it matches.)
    mochi.add_task(
        Task("Grooming", pet_name="", time=time(7, 0),
             duration=15, priority=Priority.MEDIUM)
    )
    biscuit.add_task(
        Task("Vet visit", pet_name="", time=time(7, 0),
             duration=30, priority=Priority.HIGH)
    )

    # Mark one task complete so the completed=False filter has something to exclude.
    mochi.get_tasks()[0].mark_complete()  # Evening play

    scheduler = Scheduler()

    # Sort the unsorted task list by time and print the result.
    all_tasks = owner.view_all_tasks()
    print("Schedule sorted by time:")
    for task in scheduler.sort_by_time(all_tasks):
        slot = task.time.strftime("%H:%M") if task.time else "  --  "
        print(f"{slot} - {task.description} ({task.pet_name}) [{task.priority.name}]")

    # Filter by a single pet's name.
    print("\nTasks for Mochi:")
    for task in scheduler.filter_tasks(all_tasks, pet_name="Mochi"):
        slot = task.time.strftime("%H:%M") if task.time else "  --  "
        print(f"{slot} - {task.description} ({task.pet_name})")

    # Filter by completion status.
    print("\nIncomplete tasks:")
    for task in scheduler.filter_tasks(all_tasks, completed=False):
        slot = task.time.strftime("%H:%M") if task.time else "  --  "
        print(f"{slot} - {task.description} ({task.pet_name})")

    # Check for scheduling conflicts (same date + time).
    print("\nConflicts:")
    conflicts = scheduler.detect_conflicts(all_tasks)
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts detected.")


if __name__ == "__main__":
    main()
