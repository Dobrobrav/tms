from datetime import datetime

from tasks.domain.comments.comment import CommentEntity, CommentContent
from tasks.domain.comments.dto import CommentDTO
from tasks.domain.tasks.dto import TaskDTO
from tasks.domain.tasks.task import TaskEntity, TaskTitle


def _assert_tasks_equal_without_id(task1: TaskEntity, task2: TaskEntity) -> None:
    assert task1.title == task2.title, f"Title mismatch: {task1.title} != {task2.title}"
    assert task1.reporter_id == task2.reporter_id, f"Reporter mismatch: {task1.reporter_id} != {task2.reporter_id}"
    assert task1.description == task2.description, f"Description mismatch: {task1.description} != {task2.description}"
    assert task1.assignee_id == task2.assignee_id, f"Assignee mismatch: {task1.assignee_id} != {task2.assignee_id}"
    assert task1.comments == task2.comments, f"Comment IDs mismatch: {task1.comments} != {task2.comments}"
    assert task1.related_task_ids == task2.related_task_ids, f"Related Task IDs mismatch: {task1.related_task_ids} != {task2.related_task_ids}"


def test__dto_casted_from_entity_has_correct_data() -> None:
    task_entity = TaskEntity(
        title=TaskTitle(value=(test_title := "Sample Task")),
        reporter_id=(test_reporter_id := 123),
        description=(test_description := "This is a sample task."),
        assignee_id=(test_assignee_id := 123),
        comments=[
            test_comment_entity_1 := CommentEntity(
                user_id=444, content=CommentContent(value='foobar'), comment_id=15,
                create_time=datetime(2025, 6, 16)
            ),
            test_comment_entity_2 := CommentEntity(
                user_id=333, content=CommentContent(value='fizbuz'), comment_id=5,
                create_time=datetime(2024, 5, 10)
            ),
        ],
        related_task_ids=(test_related_task_ids := [123, 456]),
        task_id=(test_task_id := 123),
    )

    task_dto = TaskDTO.from_entity(task_entity)

    assert task_dto.task_id == test_task_id
    assert task_dto.comments == [
        CommentDTO.from_entity(test_comment_entity_1),
        CommentDTO.from_entity(test_comment_entity_2),
    ]
    assert task_dto.related_task_ids == test_related_task_ids
    assert task_dto.assignee_id == test_assignee_id
    assert task_dto.description == test_description
    assert task_dto.title == test_title
    assert task_dto.reporter_id == test_reporter_id
