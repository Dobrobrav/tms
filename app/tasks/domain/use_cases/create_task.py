from tasks.domain.exceptions import InvalidReporterID, InvalidAssigneeID, InvalidRelatedTaskIDs
from tasks.domain.tasks.dto import TaskDTO
from tasks.domain.tasks.repository import TaskRepository
from tasks.domain.use_cases.base import Usecase
from tasks.domain.users.repository import UserRepository


class CreateTaskUsecase(Usecase):
    def __init__(
            self,
            task_repo: TaskRepository,
            user_repo: UserRepository,
    ) -> None:
        self._task_repo = task_repo
        self._user_repo = user_repo

    def execute(self, task_dto: TaskDTO) -> int:
        self._ensure_provided_entities_exist(task_dto)
        task_entity = task_dto.to_entity()
        return self._task_repo.set(task_entity)

    def _ensure_provided_entities_exist(self, task_dto: TaskDTO) -> None:
        if not self._user_repo.exists(id_or_ids=task_dto.reporter_id):
            raise InvalidReporterID(task_dto.reporter_id)
        if task_dto.assignee_id and not self._user_repo.exists(id_or_ids=task_dto.assignee_id):
            raise InvalidAssigneeID(task_dto.assignee_id)
        if task_dto.related_task_ids and not self._task_repo.exists(id_or_ids=task_dto.related_task_ids):
            raise InvalidRelatedTaskIDs(task_dto.related_task_ids)


def create_task_usecase_factory() -> CreateTaskUsecase:
    return CreateTaskUsecase(task_repo=TaskRepository(), user_repo=UserRepository())
