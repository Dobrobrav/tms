from datetime import datetime

import pytest
from pydantic import ValidationError

from tasks.domain.tasks.task import TaskEntity, TaskTitle


def test__task_title_cant_be_empty() -> None:
    with pytest.raises(ValidationError):
        TaskTitle(value='')


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
