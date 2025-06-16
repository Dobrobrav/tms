from typing import Self

from pydantic import BaseModel

from tasks.domain.comments.entity import CommentEntity


class CommentDTO(BaseModel):
    text: str
    user_id: int
    task_id: int | None = None
    comment_id: int | None = None

    @classmethod
    def from_entity_comment(cls, comment_entity: CommentEntity) -> Self:
        return cls(
            text=comment_entity.content,
            user_id=comment_entity.commenter_id,
            comment_id=comment_entity.comment_id,
        )
