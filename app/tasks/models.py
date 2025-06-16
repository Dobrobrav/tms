from django.db import models

from tms_types import UserModel


class TaskModel(models.Model):
    # TODO: add create time
    title = models.CharField(max_length=200, blank=True, null=False)
    description = models.TextField(blank=True, null=False)
    related_tasks = models.ManyToManyField(to='TaskModel')
    reporter = models.ForeignKey(to=UserModel, on_delete=models.PROTECT, related_name='reported_tasks')
    assignee = models.ForeignKey(to=UserModel, null=True, on_delete=models.SET_NULL)
    # TODO: add manager for preloading comments


class CommentModel(models.Model):
    text = models.TextField(blank=False, null=False)
    task = models.ForeignKey(to=TaskModel, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(to=UserModel, on_delete=models.PROTECT)
    create_time = models.DateTimeField(blank=False, null=False)
