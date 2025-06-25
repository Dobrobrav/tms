from tasks.domain.comments.dto import CommentDTO
from tasks.domain.tasks.repository import TaskRepository
from tasks.domain.use_cases.base import Usecase


class GetCommentUsecase(Usecase):
    def __init__(self, task_repo: TaskRepository):
        self._task_repo = task_repo

    def execute(self, comment_id: int) -> tuple[CommentDTO, int]:
        comment_entity, task_id = self._task_repo.get_comment(comment_id)
        return CommentDTO.from_entity(comment_entity), task_id


def get_comment_usecase_factory() -> GetCommentUsecase:
    return GetCommentUsecase(task_repo=TaskRepository())
