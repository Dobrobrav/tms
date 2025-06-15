from typing import Self

from pydantic import BaseModel

from tasks.domain.tasks.entity import TaskEntity


class TaskDTO(BaseModel):
    title: str
    reporter_id: int
    description: str = ''
    comment_ids: list[int] = []
    related_task_ids: list[int] = []
    assignee_id: int | None = None
    task_id: int | None = None

    def to_task_entity(self) -> TaskEntity:
        return TaskEntity(
            title=self.title,
            reporter_id=self.reporter_id,
            description=self.description,
            related_task_ids=self.related_task_ids,
            assignee_id=self.assignee_id,
            task_id=self.task_id,
        )

    @classmethod
    def from_entity_task(cls, task: TaskEntity) -> Self:
        return cls(
            title=task.title,
            reporter_id=task.reporter_id,
            description=task.description,
            comment_ids=task.comment_ids,
            related_task_ids=task.related_task_ids,
            assignee_id=task.assignee_id,
            task_id=task.task_id,
        )
