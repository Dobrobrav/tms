from django.urls import path

from . import views
from .use_cases.add_task_attachment import add_task_attachment_usecase_factory
from .use_cases.create_comment import create_comment_usecase_factory
from .use_cases.create_task import create_task_usecase_factory
from .use_cases.create_user import create_user_usecase_factory
from .use_cases.get_comment import get_comment_usecase_factory
from .use_cases.get_task import get_task_usecase_factory
from .use_cases.get_user import get_user_usecase_factory

urlpatterns = [
    path(
        route='users/',
        view=views.UserView.as_view(create_user_usecase=create_user_usecase_factory()),
        name='users',
    ),
    path(
        route='users/<user_id>',
        view=views.UserView.as_view(get_user_usecase=get_user_usecase_factory()),
        name='user',
    ),
    path(
        route='tasks/',
        view=views.TaskView.as_view(create_task_usecase=create_task_usecase_factory()),
        name='tasks',
    ),
    path(
        route='tasks/<int:task_id>',
        view=views.TaskView.as_view(get_task_usecase=get_task_usecase_factory()),
        name='task',
    ),
    path(  # TODO: should be 'tasks/{task_id}/comments/' for creating. But 'comments/{comment_id}' is fine for getting
        route='comments/',
        view=views.CommentView.as_view(create_comment_usecase=create_comment_usecase_factory()),
        name='comments',
    ),
    path(
        route='comments/<comment_id>',
        view=views.CommentView.as_view(get_comment_usecase=get_comment_usecase_factory()),
        name='comment',
    ),
    path(
        route='tasks/<task_id>/attachments/',
        view=views.TaskAttachmentView.as_view(add_task_attachment_usecase=add_task_attachment_usecase_factory()),
        name='task-attachments'
    )
]
