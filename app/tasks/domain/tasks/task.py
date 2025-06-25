import datetime
from typing import Iterable

from pydantic import BaseModel, Field

from tasks.domain.aggregate_root import AggregateRoot
from tasks.domain.comments.comment import CommentEntity


class TaskTitle(BaseModel):
    value: str = Field(min_length=1)


class TaskEntity(AggregateRoot):
    def __init__(
            self,
            title: TaskTitle,
            reporter_id: int,
            related_task_ids: Iterable[int],
            comments: Iterable[CommentEntity],
            description: str = '',
            assignee_id: int | None = None,
            task_id: int | None = None,
    ) -> None:
        self._title = title
        self.description = description
        self.reporter_id = reporter_id
        self.assignee_id = assignee_id
        self._comments = list(comments)
        self._related_task_ids = list(related_task_ids)
        self._task_id = task_id

    @property
    def title(self) -> str:
        return self._title.value

    @property
    def task_id(self) -> int:
        return self._task_id

    @property
    def related_task_ids(self) -> list[int]:
        return self._related_task_ids.copy()

    @property
    def comments(self) -> list[CommentEntity]:
        return self._comments.copy()

    def create_comment(self, user_id: int, text: str, create_time: datetime.datetime) -> CommentEntity:
        comment_entity = CommentEntity(
            user_id=user_id,
            content=text,
            create_time=create_time,
        )
        self._comments.append(comment_entity)
        return comment_entity
