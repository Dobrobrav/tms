from typing import Sequence
from uuid import UUID

from tasks.domain.base_repository import Repository
from tasks.domain.comments.entity import Comment


class CommentRepository(Repository):
    def get(self) -> Comment:
        ...

    def set(self, entity: Comment) -> None:
        ...

    def exists(self, id_or_ids: UUID | Sequence[UUID]) -> bool:
        ...
