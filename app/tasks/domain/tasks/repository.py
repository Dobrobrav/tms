from typing import Sequence

from tasks.domain.comments.comment import CommentEntity, CommentContent
from tasks.domain.tasks.task import TaskEntity, TaskTitle
from tasks.exceptions import InvalidTaskID, CommentNotExists
from tasks.models import TaskModel, CommentModel, TaskAttachmentModel


class TaskRepository:
    def get(self, task_id: int) -> TaskEntity:
        try:
            task_orm = TaskModel.preload_all(task_id)
        except TaskModel.DoesNotExist:
            raise InvalidTaskID(task_id=task_id)
        return TaskEntity(
            title=TaskTitle(value=task_orm.title),
            reporter_id=task_orm.reporter_id,
            description=task_orm.description,
            related_task_ids=[related_task.pk for related_task in task_orm.related_tasks.all()],
            comments=[
                CommentEntity(
                    content=CommentContent(value=c.text),
                    create_time=c.create_time,
                    comment_id=c.pk,
                    user_id=c.commenter_id,
                )
                for c in task_orm.comments.all()
            ],
            attachment_ids=[attachment.pk for attachment in task_orm.attachments.all()],
            assignee_id=task_orm.assignee_id,
            task_id=task_orm.pk,
        )

    def set(self, task_entity: TaskEntity) -> int:
        task_already_stored = task_entity.task_id is not None
        if task_already_stored:
            return self._update_existent_task(task_entity).pk

        return self._store_new_task(task_entity).pk

    def _update_existent_task(self, task_entity: TaskEntity) -> TaskModel:
        # TODO: cover with tests
        TaskModel.objects.filter(pk=task_entity.task_id).update(
            title=task_entity.title,
            reporter_id=task_entity.reporter_id,
            description=task_entity.description,
            assignee_id=task_entity.assignee_id,
        )

        task_orm = TaskModel.objects.get(pk=task_entity.task_id)
        task_orm.related_tasks.set(self._get_related_tasks(task_entity.related_task_ids))
        task_orm.attachments.set(self._get_attachments(task_entity.attachment_ids))
        return task_orm

    def _get_attachments(self, ids: list[int]):
        return TaskAttachmentModel.objects.filter(pk__in=ids)

    def _get_related_tasks(self, ids: list[int]):
        return TaskModel.objects.filter(pk__in=ids)

    def _store_new_task(self, task_entity: TaskEntity) -> TaskModel:
        task_orm = TaskModel.objects.create(
            title=task_entity.title,
            reporter_id=task_entity.reporter_id,
            description=task_entity.description,
            assignee_id=task_entity.assignee_id,
        )
        task_orm.related_tasks.set(self._get_related_tasks(task_entity.related_task_ids))
        task_orm.attachments.set(self._get_attachments(task_entity.attachment_ids))
        return task_orm

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

    def get_comment(self, comment_id: int) -> tuple[CommentEntity, int]:
        try:
            comment_orm = CommentModel.objects.get(pk=comment_id)
        except CommentModel.DoesNotExist:
            raise CommentNotExists(comment_id)
        return (
            CommentEntity(
                user_id=comment_orm.commenter_id,
                comment_id=comment_orm.pk,
                content=CommentContent(value=comment_orm.text),
                create_time=comment_orm.create_time
            ),
            comment_orm.task_id,
        )
