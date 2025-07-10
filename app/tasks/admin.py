from django.contrib import admin

from tasks.models import TaskModel


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'related_tasks', 'reporter', 'assignee', 'attachments']
    readonly_fields = ['attachments']

    def attachments(self, obj):
        return "\n".join([a.filename for a in obj.attachments.all()])
