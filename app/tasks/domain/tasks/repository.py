from typing import Sequence

from tasks.domain.base_repository import Repository
from tasks.domain.exceptions import InvalidRelatedTaskIDs
from tasks.domain.tasks.entity import TaskEntity
from tasks.models import TaskModel


class TaskRepository(Repository):
    def get(self, entity_id: int) -> TaskEntity:
        task_orm = TaskModel.objects.get(pk=entity_id)
        return TaskEntity(
            title=task_orm.title,
            reporter_id=task_orm.reporter_id,
            description=task_orm.description,
            related_task_ids=[related_task.pk for related_task in task_orm.related_tasks.all()],
            assignee_id=task_orm.assignee_id,
            task_id=task_orm.pk,
        )

    def set(self, task_entity: TaskEntity) -> int:
        related_tasks_orm = TaskModel.objects.filter(pk__in=task_entity.related_task_ids)
        if task_already_exists := task_entity.task_id:
            # NOTE (SemenK): not tested
            TaskModel.objects.filter(pk=task_entity.task_id).update(
                title=task_entity.title,
                reporter_id=task_entity.reporter_id,
                description=task_entity.description,
                assignee_id=task_entity.assignee_id,
            )
            task_orm = TaskModel.objects.get(pk=task_entity.task_id)
            task_orm.related_tasks.set(related_tasks_orm)

            assert task_orm.pk == task_entity.task_id

            return task_entity.task_id
        else:
            new_task = TaskModel.objects.create(
                title=task_entity.title,
                reporter_id=task_entity.reporter_id,
                description=task_entity.description,
                assignee_id=task_entity.assignee_id,
            )
            new_task.related_tasks.set(related_tasks_orm)
            return new_task.pk

    def exists(self, id_or_ids: int | Sequence[int]) -> bool:
        """ Returns true if ALL provided ids exist in repo """
        ids = [id_or_ids] if isinstance(id_or_ids, int) else id_or_ids
        return TaskModel.objects.filter(pk__in=list(ids)).count() == len(ids)
