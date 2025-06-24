from typing import Sequence

from tasks.domain.base_repository import Repository
from tasks.domain.comments.comment import CommentEntity
from tasks.domain.exceptions import InvalidTaskID, CommentNotExists
from tasks.domain.tasks.task import TaskEntity
from tasks.models import TaskModel, CommentModel


class TaskRepository(Repository):
    def get(self, entity_id: int) -> TaskEntity:
        # TODO: make it prefetch all comments?
        try:
            task_orm = TaskModel.objects.get(pk=entity_id)
        except TaskModel.DoesNotExist:
            raise InvalidTaskID(task_id=entity_id)
        return TaskEntity(
            title=task_orm.title,
            reporter_id=task_orm.reporter_id,
            description=task_orm.description,
            related_task_ids=[related_task.pk for related_task in task_orm.related_tasks.all()],
            comments=[
                CommentEntity(
                    content=c.text,
                    create_time=c.create_time,
                    comment_id=c.pk,
                    user_id=c.commenter_id,
                )
                for c in task_orm.comments.all()
            ],
            assignee_id=task_orm.assignee_id,
            task_id=task_orm.pk,
        )

    def set(self, task_entity: TaskEntity) -> int:
        related_tasks_orm = TaskModel.objects.filter(pk__in=task_entity.related_task_ids)
        if task_already_exists := task_entity.task_id:
            raise NotImplementedError('this area is not covered with tests')

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

    def set_comment(self, task_entity: TaskEntity, comment_entity: CommentEntity) -> int:
        comment_orm = CommentModel.objects.create(
            text=comment_entity.content,
            task=TaskModel.objects.get(pk=task_entity.task_id),
            create_time=comment_entity.create_time,
            commenter_id=comment_entity.commenter_id,
        )
        return comment_orm.pk

    def get_comment(self, comment_id: int) -> CommentEntity:
        try:
            comment_orm = CommentModel.objects.get(pk=comment_id)
        except CommentModel.DoesNotExist:
            raise CommentNotExists(comment_id)
        return CommentEntity(
            user_id=comment_orm.commenter_id,
            comment_id=comment_orm.pk,
            content=comment_orm.text,
            create_time=comment_orm.create_time
        )
