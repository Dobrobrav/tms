from typing import Iterable
from uuid import UUID

import icontract

from tasks.domain.aggregate_root import AggregateRoot


class Task(AggregateRoot):
    def __init__(
            self,
            title: str,
            reporter_id: UUID,
            description: str = '',
            related_task_ids: Iterable[UUID] = None,
            assignee_id: UUID | None = None,
            task_id: UUID | None = None,
    ) -> None:
        # TODO: how to make sure that the ids are of the correct type entities
        self.title = title
        self.description = description
        self.reporter_id = reporter_id
        self.assignee_id = assignee_id
        self._comment_ids: list[UUID] = []
        self._related_task_ids: list[UUID] = list(related_task_ids) or []
        self._id = task_id

    def add_comment_id(self, comment_id: UUID) -> None:
        self._comment_ids.append(comment_id)

    @icontract.require(lambda self, comment_id: comment_id in self._comment_ids)
    def remove_comment_id(self, comment_id: UUID) -> None:
        self._comment_ids.remove(comment_id)

    def get_comment_ids(self) -> list[UUID]:
        return self._comment_ids.copy()

    def add_related_task_id(self, task_id: UUID) -> None:
        self._related_task_ids.append(task_id)

    @icontract.require(lambda self, task_id: task_id in self._related_task_ids)
    def remove_related_task_id(self, task_id: UUID) -> None:
        self._related_task_ids.remove(task_id)

    def get_related_task_ids(self) -> list[UUID]:
        return self._related_task_ids.copy()

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    @icontract.require(lambda self, value: len(value) > 0, 'title must not be empty')
    def title(self, value: str) -> None:
        self._title = value
