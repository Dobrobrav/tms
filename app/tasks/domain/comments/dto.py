from datetime import datetime
from typing import Self

from pydantic import BaseModel

from tasks.domain.comments.entity import CommentEntity


class CommentDTO(BaseModel):
    text: str
    user_id: int
    comment_id: int | None = None
    create_time: datetime | None = None

    @classmethod
    def from_entity(cls, comment_entity: CommentEntity) -> Self:
        return cls(
            text=comment_entity.content,
            user_id=comment_entity.commenter_id,
            comment_id=comment_entity.comment_id,
            create_time=comment_entity.create_time,
        )

    @property
    def create_time_str(self) -> str:
        return self.create_time.isoformat()
