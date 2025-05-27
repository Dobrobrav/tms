from django.urls import path

from . import views
from .domain.use_cases.create_task import create_task_use_case_factory

urlpatterns = [
    path('task/', views.TaskView.as_view(create_task_use_case=create_task_use_case_factory()))
]
