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
    # add_task() stamps each task's pet_name, so it's left blank here.
    mochi.add_task(
        Task("Morning walk", pet_name="", time=time(8, 0),
             duration=30, priority=Priority.HIGH)
    )
    biscuit.add_task(
        Task("Feeding", pet_name="", time=time(9, 30),
             duration=10, priority=Priority.MEDIUM)
    )
    mochi.add_task(
        Task("Evening play", pet_name="", time=time(18, 0),
             duration=20, priority=Priority.LOW, frequency=Frequency.DAILY)
    )

    # Generate today's schedule, ordered by time.
    scheduler = Scheduler()
    schedule = scheduler.generate_daily_schedule(owner)

    print("Today's Schedule:")
    for task in schedule:
        slot = task.time.strftime("%H:%M") if task.time else "  --  "
        print(f"{slot} - {task.description} ({task.pet_name}) [{task.priority.name}]")


if __name__ == "__main__":
    main()
