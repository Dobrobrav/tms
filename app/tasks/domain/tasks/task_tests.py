from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from tasks.domain.comments.comment import CommentEntity, CommentContent
from tasks.domain.tasks.task import TaskEntity, TaskTitle


def test__task_title_cant_be_empty() -> None:
    with pytest.raises(ValidationError):
        TaskTitle(value='')


def test__create_task() -> None:
    test_title = 'test title'
    test_reporter_id = 123
    test_comments = [
        CommentEntity(
            user_id=1, content=CommentContent(value='test content'),
            create_time=datetime.now() - timedelta(days=1),
        ),
        CommentEntity(user_id=2, content=CommentContent(value='test content 2'), create_time=datetime.now()),
    ]
    test_description = "This is a sample task."
    test_assignee_id = 333
    test_task_id = 15
    test_related_task_ids = [11, 22, 33]

    task = TaskEntity(
        title=TaskTitle(value=test_title),
        reporter_id=test_reporter_id,
        comments=test_comments,
        description=test_description,
        assignee_id=test_assignee_id,
        task_id=test_task_id,
        related_task_ids=test_related_task_ids,
    )

    assert task.comments == test_comments
    assert task.title == test_title
    assert task.task_id == test_task_id
    assert task.description == test_description
    assert task.reporter_id == test_reporter_id
    assert task.assignee_id == test_assignee_id


def test__task_creates_comment() -> None:
    task = TaskEntity(
        title=TaskTitle(value='task title'),
        reporter_id=123,
        description="This is a sample task.",
        comments=[],
        related_task_ids=[],
    )
    test_commenter_id = 228
    test_comment_text = 'test_comment'
    test_create_time = datetime.now()

    task.create_comment(
        user_id=test_commenter_id,
        text=test_comment_text,
        create_time=test_create_time
    )

    assert len(task.comments) == 1
    comment = task.comments[0]
    assert comment.comment_id is None
    assert comment.create_time == test_create_time
    assert comment.commenter_id == test_commenter_id
    assert comment.content == test_comment_text
