"""Basic pytest coverage for PawPal+ task behavior."""

from pawpal_system import Pet, Task


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
