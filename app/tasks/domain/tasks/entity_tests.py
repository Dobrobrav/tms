import uuid

from tasks.domain.tasks.dto import TaskDTO
from tasks.domain.tasks.entity import Task


def test_create_task_from_dto() -> None:
    # arrange
    expected_task = Task(
        title=(test_title := "Sample Task"),
        reporter_id=(test_reporter_id := uuid.uuid4()),
        description=(test_description := "This is a sample task."),
        assignee_id=(test_assignee_id := uuid.uuid4()),
        related_task_ids=(test_related_task_ids := [uuid.uuid4(), uuid.uuid4()]),
        task_id=(test_task_id := uuid.uuid4()),
    )
    task_dto = TaskDTO(
        title=test_title,
        reporter_id=test_reporter_id,
        description=test_description,
        assignee_id=test_assignee_id,
        related_task_ids=test_related_task_ids,
        task_id=test_task_id,
    )

    # act
    actual_task = task_dto.to_task()

    # assert
    assert_tasks_equal_without_id(actual_task, expected_task)


def assert_tasks_equal_without_id(task1: Task, task2: Task) -> None:
    assert task1.title == task2.title, f"Title mismatch: {task1.title} != {task2.title}"
    assert task1.reporter_id == task2.reporter_id, f"Reporter mismatch: {task1.reporter_id} != {task2.reporter_id}"
    assert task1.description == task2.description, f"Description mismatch: {task1.description} != {task2.description}"
    assert task1.assignee_id == task2.assignee_id, f"Assignee mismatch: {task1.assignee_id} != {task2.assignee_id}"
    assert task1.get_comment_ids() == task2.get_comment_ids(), f"Comment IDs mismatch: {task1.get_comment_ids()} != {task2.get_comment_ids()}"
    assert task1.get_related_task_ids() == task2.get_related_task_ids(), f"Related Task IDs mismatch: {task1.get_related_task_ids()} != {task2.get_related_task_ids()}"
