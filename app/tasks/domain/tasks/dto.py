from uuid import UUID

from pydantic import BaseModel

from tasks.domain.tasks.entity import Task


class TaskDTO(BaseModel):
    title: str
    reporter_id: UUID
    description: str
    comment_ids: list[UUID] = []
    related_task_ids: list[UUID]
    assignee_id: UUID
    task_id: UUID | None = None

    def to_task(self) -> Task:
        return Task(
            title=self.title,
            reporter_id=self.reporter_id,
            description=self.description,
            related_task_ids=self.related_task_ids,
            assignee_id=self.assignee_id,
            task_id=self.task_id,
        )
