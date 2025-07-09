from typing import Self

from pydantic import BaseModel

from tasks.domain.comments.dto import CommentDTO
from tasks.domain.tasks.task import TaskEntity


class TaskDTO(BaseModel):
    title: str
    reporter_id: int
    description: str = ''
    comments: list[CommentDTO] | None = None
    attachment_ids: list[int] | None = None
    related_task_ids: list[int] | None
    assignee_id: int | None = None
    task_id: int | None = None

    @classmethod
    def from_entity(cls, task: TaskEntity) -> Self:
        return cls(
            title=task.title,
            reporter_id=task.reporter_id,
            description=task.description,
            comments=[CommentDTO.from_entity(c) for c in task.comments],
            related_task_ids=task.related_task_ids,
            attachment_ids=task.attachment_ids,
            assignee_id=task.assignee_id,
            task_id=task.task_id,
        )
