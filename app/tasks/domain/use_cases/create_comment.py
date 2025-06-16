import datetime

from tasks.domain.comments.dto import CommentDTO
from tasks.domain.tasks.repository import TaskRepository
from tasks.domain.use_cases.base import Usecase


class CreateCommentUsecase(Usecase):
    def __init__(self, task_repo: TaskRepository) -> None:
        self._task_repo = task_repo

    def execute(self, comment_dto: CommentDTO) -> int:
        task_entity = self._task_repo.get(comment_dto.task_id)
        comment_entity = task_entity.create_comment(comment_dto, create_time=datetime.datetime.now())
        comment_id = self._task_repo.set_comment(task_entity, comment_entity)
        return comment_id


def create_comment_usecase_factory() -> CreateCommentUsecase:
    return CreateCommentUsecase(task_repo=TaskRepository())
