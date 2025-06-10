from django.urls import path

from . import views
from .domain.use_cases.create_task import create_task_usecase_factory
from .domain.use_cases.create_user import create_user_usecase_factory
from .domain.use_cases.get_user import get_user_usecase_factory

urlpatterns = [
    path('users/', views.UserView.as_view(create_user_usecase=create_user_usecase_factory())),
    path('users/<int:user_id>', views.UserView.as_view(get_user_usecase=get_user_usecase_factory()))
]
