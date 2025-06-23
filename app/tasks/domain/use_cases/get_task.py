from tasks.domain.tasks.dto import TaskDTO
from tasks.domain.tasks.repository import TaskRepository
from tasks.domain.use_cases.base import Usecase


class GetTaskUsecase(Usecase):
    def __init__(self, task_repo: TaskRepository) -> None:
        self._task_repo = task_repo

    def execute(self, task_id: int) -> TaskDTO:
        task = self._task_repo.get(task_id)
        return TaskDTO.from_entity(task)


def get_task_usecase_factory() -> GetTaskUsecase:
    return GetTaskUsecase(TaskRepository())
