from typing import Iterable

import icontract

from tasks.domain.aggregate_root import AggregateRoot


class TaskEntity(AggregateRoot):
    def __init__(
            self,
            title: str,
            reporter_id: int,
            description: str = '',
            related_task_ids: Iterable[int] = None,
            assignee_id: int | None = None,
            task_id: int | None = None,
    ) -> None:
        self.title = title
        self.description = description
        self.reporter_id = reporter_id
        self.assignee_id = assignee_id
        self._comment_ids: list[int] = []
        self._related_task_ids: list[int] = list(related_task_ids) or []
        self._task_id = task_id

    def get_comment_ids(self) -> list[int]:
        return self._comment_ids.copy()

    def get_related_task_ids(self) -> list[int]:
        return self._related_task_ids.copy()

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    @icontract.require(lambda self, value: len(value) > 0, 'title must not be empty')
    def title(self, value: str) -> None:
        self._title = value

    @property
    def task_id(self) -> int:
        return self._task_id

    @property
    def related_task_ids(self) -> list[int]:
        return self._related_task_ids.copy()

    @property
    def comment_ids(self) -> list[int]:
        return self._comment_ids.copy()
