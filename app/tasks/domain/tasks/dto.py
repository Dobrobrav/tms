from typing import Self

from pydantic import BaseModel

from tasks.domain.comments.dto import CommentDTO
from tasks.domain.tasks.comment import TaskEntity


class TaskDTO(BaseModel):
    title: str
    reporter_id: int
    description: str = ''
    comments: list[CommentDTO] = []
    related_task_ids: list[int] = []
    assignee_id: int | None = None
    task_id: int | None = None

    def to_entity(self) -> TaskEntity:
        return TaskEntity(
            title=self.title,
            reporter_id=self.reporter_id,
            description=self.description,
            related_task_ids=self.related_task_ids,
            assignee_id=self.assignee_id,
            task_id=self.task_id,
        )

    @classmethod
    def from_entity(cls, task: TaskEntity) -> Self:
        return cls(
            title=task.title,
            reporter_id=task.reporter_id,
            description=task.description,
            comments=[CommentDTO.from_entity(c) for c in task.comments],
            related_task_ids=task.related_task_ids,
            assignee_id=task.assignee_id,
            task_id=task.task_id,
        )
