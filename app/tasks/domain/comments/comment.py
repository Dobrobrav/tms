import datetime

import icontract

from tasks.domain.exceptions import DomainValidationError


class CommentEntity:
    """
    All modifications of comments must go strictly through TaskEntity class!
    """
    def __init__(
            self,
            user_id: int,
            content: str,
            create_time: datetime.datetime,
            comment_id: int | None = None,
    ) -> None:
        self._commenter_id = user_id
        self._set_content(content)
        self._create_time = create_time
        self._comment_id = comment_id

    @property
    def content(self) -> str:
        return self._content

    @icontract.require(
        lambda self, value: len(value) > 0, 'content must not be empty',
        error=DomainValidationError,
    )
    def _set_content(self, value: str) -> None:
        self._content = value

    @property
    def create_time(self) -> datetime.datetime:
        return self._create_time

    @property
    def commenter_id(self) -> int:
        return self._commenter_id

    @property
    def comment_id(self) -> int:
        return self._comment_id
