from typing import Sequence
from uuid import UUID

from tasks.domain.base_repository import Repository
from tasks.domain.tasks.entity import Task


class TaskRepository(Repository):
    def get(self) -> Task:
        ...

    def set(self, task: Task) -> None:
        ...

    def exists(self, id_or_ids: UUID | Sequence[UUID]) -> bool:
        ...
