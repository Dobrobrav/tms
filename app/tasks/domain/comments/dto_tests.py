from datetime import datetime

from tasks.domain.comments.dto import CommentDTO
from tasks.domain.comments.entity import CommentEntity


def test__dto_casted_from_comment_entity_has_correct_data() -> None:
    comment_entity = CommentEntity(
        user_id=444,
        content='foobar',
        comment_id=15,
        create_time=datetime(2025, 6, 16)
    )

    comment_dto = CommentDTO.from_entity(comment_entity)

    assert comment_dto.comment_id == comment_entity.comment_id
    assert comment_dto.text == comment_entity.content
    assert comment_dto.user_id == comment_entity.commenter_id
    assert comment_dto.create_time == comment_entity.create_time
