"""Basic pytest coverage for PawPal+ task behavior."""

from datetime import date, time, timedelta

from pawpal_system import Frequency, Owner, Pet, Scheduler, Task


def test_mark_complete():
    """A task starts incomplete and becomes complete after mark_complete()."""
    task = Task("Morning walk", pet_name="Mochi")
    assert task.completed is False

    task.mark_complete()
    assert task.completed is True


def test_add_task():
    """Adding a task to a pet grows its task list by one."""
    pet = Pet(name="Mochi")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task("Feeding", pet_name="Mochi"))
    assert len(pet.get_tasks()) == 1


# --- Sorting -------------------------------------------------------------


def test_sort_by_time_orders_ascending():
    """Tasks with distinct times come back in ascending chronological order."""
    scheduler = Scheduler()
    noon = Task("Lunch", pet_name="Mochi", time=time(12, 0))
    morning = Task("Walk", pet_name="Mochi", time=time(8, 0))
    evening = Task("Dinner", pet_name="Mochi", time=time(18, 0))

    ordered = scheduler.sort_by_time([noon, morning, evening])

    assert [t.time for t in ordered] == [time(8, 0), time(12, 0), time(18, 0)]


def test_sort_by_time_returns_new_list_without_mutating_input():
    """Sorting returns a new list and leaves the original order untouched."""
    scheduler = Scheduler()
    noon = Task("Lunch", pet_name="Mochi", time=time(12, 0))
    morning = Task("Walk", pet_name="Mochi", time=time(8, 0))
    original = [noon, morning]

    ordered = scheduler.sort_by_time(original)

    assert ordered is not original
    assert original == [noon, morning]
    assert ordered == [morning, noon]


# --- Filtering -----------------------------------------------------------


def test_filter_by_pet_name_only():
    """Filtering by pet_name returns only that pet's tasks."""
    scheduler = Scheduler()
    mochi_task = Task("Walk", pet_name="Mochi")
    kiwi_task = Task("Feed", pet_name="Kiwi")

    result = scheduler.filter_tasks([mochi_task, kiwi_task], pet_name="Mochi")

    assert result == [mochi_task]


def test_filter_by_completed_splits_correctly():
    """Filtering by completed=True/False returns the correct split."""
    scheduler = Scheduler()
    done = Task("Walk", pet_name="Mochi", completed=True)
    pending = Task("Feed", pet_name="Mochi", completed=False)
    tasks = [done, pending]

    assert scheduler.filter_tasks(tasks, completed=True) == [done]
    assert scheduler.filter_tasks(tasks, completed=False) == [pending]


def test_filter_by_pet_name_and_completed_applies_and_logic():
    """Filtering by both pet_name and completed applies AND logic."""
    scheduler = Scheduler()
    mochi_done = Task("Walk", pet_name="Mochi", completed=True)
    mochi_pending = Task("Feed", pet_name="Mochi", completed=False)
    kiwi_done = Task("Feed", pet_name="Kiwi", completed=True)
    tasks = [mochi_done, mochi_pending, kiwi_done]

    result = scheduler.filter_tasks(tasks, pet_name="Mochi", completed=True)

    assert result == [mochi_done]


def test_filter_with_both_none_returns_everything():
    """Passing no filters returns all tasks unchanged."""
    scheduler = Scheduler()
    tasks = [
        Task("Walk", pet_name="Mochi"),
        Task("Feed", pet_name="Kiwi"),
    ]

    assert scheduler.filter_tasks(tasks) == tasks


# --- Recurrence ----------------------------------------------------------


def test_mark_complete_daily_returns_next_day_occurrence():
    """A DAILY task is completed and yields a fresh occurrence one day later."""
    task = Task(
        "Walk",
        pet_name="Mochi",
        time=time(8, 0),
        date=date(2026, 7, 5),
        frequency=Frequency.DAILY,
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.date == date(2026, 7, 6)
    assert next_task.time == time(8, 0)
    assert next_task.completed is False


def test_mark_complete_weekly_returns_next_week_occurrence():
    """A WEEKLY task yields a fresh occurrence seven days later."""
    task = Task(
        "Grooming",
        pet_name="Mochi",
        date=date(2026, 7, 5),
        frequency=Frequency.WEEKLY,
    )

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.date == date(2026, 7, 5) + timedelta(days=7)


def test_mark_complete_once_returns_none():
    """A ONCE task is completed but produces no next occurrence."""
    task = Task("Vet visit", pet_name="Mochi", frequency=Frequency.ONCE)

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is None


def test_complete_task_once_appends_nothing_to_pet():
    """Completing a ONCE task leaves the pet's task list length unchanged."""
    pet = Pet(name="Mochi")
    task = Task("Vet visit", pet_name="Mochi", frequency=Frequency.ONCE)
    pet.add_task(task)

    result = pet.complete_task(task)

    assert result is None
    assert len(pet.get_tasks()) == 1


def test_complete_task_appends_recurring_next_occurrence():
    """Completing a recurring task appends its next occurrence to the pet."""
    pet = Pet(name="Mochi")
    task = Task(
        "Walk",
        pet_name="Mochi",
        date=date(2026, 7, 5),
        frequency=Frequency.DAILY,
    )
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert len(pet.get_tasks()) == 2
    assert next_task in pet.get_tasks()
    assert next_task.date == date(2026, 7, 6)


# --- Conflict detection --------------------------------------------------


def test_two_tasks_same_slot_produce_one_warning_naming_both():
    """Two tasks at the identical date and time produce exactly one warning."""
    scheduler = Scheduler()
    slot = date(2026, 7, 5)
    walk = Task("Walk", pet_name="Mochi", time=time(8, 0), date=slot)
    feed = Task("Feed", pet_name="Kiwi", time=time(8, 0), date=slot)

    warnings = scheduler.detect_conflicts([walk, feed])

    assert len(warnings) == 1
    assert "Walk" in warnings[0]
    assert "Feed" in warnings[0]


def test_distinct_times_produce_no_warnings():
    """Tasks at distinct times produce no conflict warnings."""
    scheduler = Scheduler()
    slot = date(2026, 7, 5)
    walk = Task("Walk", pet_name="Mochi", time=time(8, 0), date=slot)
    feed = Task("Feed", pet_name="Mochi", time=time(9, 0), date=slot)

    assert scheduler.detect_conflicts([walk, feed]) == []


def test_three_tasks_same_slot_produce_single_warning_listing_all():
    """Three tasks at the same slot yield one warning naming all three."""
    scheduler = Scheduler()
    slot = date(2026, 7, 5)
    tasks = [
        Task("Walk", pet_name="Mochi", time=time(8, 0), date=slot),
        Task("Feed", pet_name="Kiwi", time=time(8, 0), date=slot),
        Task("Meds", pet_name="Rex", time=time(8, 0), date=slot),
    ]

    warnings = scheduler.detect_conflicts(tasks)

    assert len(warnings) == 1
    assert "Walk" in warnings[0]
    assert "Feed" in warnings[0]
    assert "Meds" in warnings[0]


def test_same_time_different_dates_do_not_conflict():
    """Two tasks at the same time on different dates do not conflict."""
    scheduler = Scheduler()
    walk = Task("Walk", pet_name="Mochi", time=time(8, 0), date=date(2026, 7, 5))
    feed = Task("Feed", pet_name="Mochi", time=time(8, 0), date=date(2026, 7, 6))

    assert scheduler.detect_conflicts([walk, feed]) == []


# --- Edge cases ----------------------------------------------------------


def test_pet_with_no_tasks_returns_empty_list():
    """A pet with no tasks returns an empty task list."""
    pet = Pet(name="Mochi")

    assert pet.get_tasks() == []


def test_owner_with_no_pets_returns_empty_collections():
    """An owner with no pets yields empty task views and schedules."""
    owner = Owner(name="Sam")
    scheduler = Scheduler()

    assert owner.view_all_tasks() == []
    assert scheduler.generate_daily_schedule(owner) == []
