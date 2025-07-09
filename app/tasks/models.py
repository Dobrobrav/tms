from typing import Self

from django.db import models

from tms_types import UserModel


class TaskModel(models.Model):
    title = models.CharField(max_length=200, blank=True, null=False)
    description = models.TextField(blank=True, null=False)
    related_tasks = models.ManyToManyField(to='TaskModel')
    reporter = models.ForeignKey(to=UserModel, on_delete=models.PROTECT, related_name='reported_tasks')
    assignee = models.ForeignKey(to=UserModel, null=True, on_delete=models.SET_NULL)

    @classmethod
    def preload_all(cls, task_id: int) -> Self:
        return (
            cls.objects
            .prefetch_related('attachments', 'related_tasks')
            .select_related('reporter', 'assignee')
            .get(pk=task_id)
        )


class CommentModel(models.Model):
    text = models.TextField(blank=False, null=False)
    task = models.ForeignKey(to=TaskModel, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(to=UserModel, on_delete=models.PROTECT)
    create_time = models.DateTimeField(blank=False, null=False)


class TaskAttachmentModel(models.Model):
    filename = models.CharField(max_length=200, blank=False, null=False)
    task = models.ForeignKey(to=TaskModel, null=True, on_delete=models.CASCADE, related_name='attachments')


class AttachmentS3MetaModel(models.Model):
    s3_file_key = models.CharField(max_length=200)
    attachment_id = models.IntegerField()
