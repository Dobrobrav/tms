import datetime

from pydantic import BaseModel, Field


class CommentEntity:
    """ All modifications of comments must go strictly through TaskEntity class! """

    def __init__(
            self,
            user_id: int,
            content: 'CommentContent',
            create_time: datetime.datetime,
            comment_id: int | None = None,
    ) -> None:
        self._commenter_id = user_id
        self._content = content
        self._create_time = create_time
        self._comment_id = comment_id

    @property
    def content(self) -> str:
        return self._content.value

    @property
    def create_time(self) -> datetime.datetime:
        return self._create_time

    @property
    def commenter_id(self) -> int:
        return self._commenter_id

    @property
    def comment_id(self) -> int:
        return self._comment_id


class CommentContent(BaseModel):
    value: str = Field(min_length=1)
