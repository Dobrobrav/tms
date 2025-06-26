from datetime import datetime, timedelta
from typing import Sequence

import pytest
from pydantic import ValidationError, HttpUrl

from tasks.domain.comments.comment import CommentEntity, CommentContent
from tasks.domain.tasks.task import TaskEntity, TaskTitle


@pytest.fixture
def minimal_task() -> TaskEntity:
    return TaskEntity(
        title=TaskTitle(value='task title'),
        reporter_id=123,
        related_task_ids=[],
        comments=[],
        attachment_urls=[],
    )


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
    test_attachment_urls = [
        HttpUrl('https://some.domain/attachment-endpoint/id_1'),
        HttpUrl('https://some.domain/attachment-endpoint/id_2'),
    ]

    task = TaskEntity(
        title=TaskTitle(value=test_title),
        reporter_id=test_reporter_id,
        comments=test_comments,
        description=test_description,
        assignee_id=test_assignee_id,
        task_id=test_task_id,
        related_task_ids=test_related_task_ids,
        attachment_urls=test_attachment_urls,
    )

    assert _comments_are_the_same(task.comments, test_comments)
    assert task.title == test_title
    assert task.task_id == test_task_id
    assert task.description == test_description
    assert task.reporter_id == test_reporter_id
    assert task.assignee_id == test_assignee_id
    assert task.attachment_urls == test_attachment_urls


def test__task_creates_comment(minimal_task: TaskEntity) -> None:
    test_commenter_id = 228
    test_comment_text = 'test_comment'
    test_create_time = datetime.now()

    minimal_task.create_comment(
        user_id=test_commenter_id,
        text=test_comment_text,
        create_time=test_create_time
    )

    assert len(minimal_task.comments) == 1
    comment = minimal_task.comments[0]
    assert comment.comment_id is None
    assert comment.create_time == test_create_time
    assert comment.commenter_id == test_commenter_id
    assert comment.content == test_comment_text


def test__add_attachment_url_to_task(minimal_task: TaskEntity) -> None:
    test_attachment_url = HttpUrl('https://some.domain/attachment-endpoint/id_1')

    minimal_task.add_attachment_url(test_attachment_url)

    assert minimal_task.attachment_urls == [test_attachment_url]


def _comments_are_the_same(comments_1: Sequence[CommentEntity], comments_2: Sequence[CommentEntity]) -> bool:
    if len(comments_1) != len(comments_2):
        return False

    for c1, c2 in zip(comments_1, comments_2):
        if (
                c1.content != c2.content
                or c1.commenter_id != c2.commenter_id
                or c1.create_time != c2.create_time
                or c1.comment_id != c2.comment_id
        ):
            return False

    return True
