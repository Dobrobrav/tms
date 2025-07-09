from pydantic import BaseModel, Field

from tasks.domain.base_aggregate_root import AggregateRoot


class AttachmentEntity(AggregateRoot):
    def __init__(self, filename: 'Filename', attachment_id: int | None = None) -> None:
        self._filename = filename
        self._attachment_id = attachment_id

    @property
    def filename(self) -> str:
        return self._filename.value

    @property
    def attachment_id(self) -> int:
        return self._attachment_id


class Filename(BaseModel):
    value: str = Field(min_length=1)
