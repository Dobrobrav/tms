from tasks.domain.tasks.dto import TaskDTO
from tasks.domain.tasks.entity import TaskEntity


def test_create_task_entity_from_dto() -> None:
    expected_task_entity = TaskEntity(
        title=(test_title := "Sample Task"),
        reporter_id=(test_reporter_id := 123),
        description=(test_description := "This is a sample task."),
        assignee_id=(test_assignee_id := 123),
        related_task_ids=(test_related_task_ids := [123, 456]),
        task_id=(test_task_id := 123),
    )
    task_dto = TaskDTO(
        title=test_title,
        reporter_id=test_reporter_id,
        description=test_description,
        assignee_id=test_assignee_id,
        related_task_ids=test_related_task_ids,
        task_id=test_task_id,
    )

    assert_tasks_equal_without_id(task_dto.to_task_entity(), expected_task_entity)


def assert_tasks_equal_without_id(task1: TaskEntity, task2: TaskEntity) -> None:
    assert task1.title == task2.title, f"Title mismatch: {task1.title} != {task2.title}"
    assert task1.reporter_id == task2.reporter_id, f"Reporter mismatch: {task1.reporter_id} != {task2.reporter_id}"
    assert task1.description == task2.description, f"Description mismatch: {task1.description} != {task2.description}"
    assert task1.assignee_id == task2.assignee_id, f"Assignee mismatch: {task1.assignee_id} != {task2.assignee_id}"
    assert task1.comments == task2.comments, f"Comment IDs mismatch: {task1.comments} != {task2.comments}"
    assert task1.related_task_ids == task2.related_task_ids, f"Related Task IDs mismatch: {task1.related_task_ids} != {task2.related_task_ids}"
