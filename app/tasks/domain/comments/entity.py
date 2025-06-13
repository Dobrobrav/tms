import datetime
from uuid import UUID

import icontract

from tasks.domain.aggregate_root import AggregateRoot


class Comment(AggregateRoot):
    def __init__(
            self,
            user_id: UUID,
            content: str,
            create_time: datetime.datetime,
            id: UUID | None = None,
    ) -> None:
        self._user_id = user_id
        self.content = content
        self._create_time = create_time
        self._id = id

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    @icontract.require(lambda self, value: len(value) > 0, 'content must not be empty')
    def content(self, value: str) -> None:
        self._content = value

    @property
    def create_time(self) -> datetime.datetime:
        return self._create_time
