from datetime import datetime

import pytest

from tasks.domain.comments.comment import CommentEntity
from tasks.domain.exceptions import DomainValidationError


def test__cant_create_comment_with_empty_content() -> None:
    with pytest.raises(DomainValidationError):
        CommentEntity(
            user_id=777,
            content='',
            create_time=datetime(2025, 6, 16)
        )
