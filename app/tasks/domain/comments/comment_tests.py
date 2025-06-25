import pytest
from pydantic import ValidationError

from tasks.domain.comments.comment import CommentContent


def test__comment_content_cant_be_empty() -> None:
    with pytest.raises(ValidationError):
        CommentContent(value='')
