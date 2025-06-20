from tasks.domain.use_cases.base import Usecase
from tasks.domain.users.dto import UserDTO
from tasks.domain.users.entity import User
from tasks.domain.users.repository import UserRepository


class CreateUserUsecase(Usecase):
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    def execute(self, user_dto: UserDTO) -> int:
        user = User(name=user_dto.name)
        user_id = self._user_repo.set(user)
        return user_id


def create_user_usecase_factory() -> CreateUserUsecase:
    return CreateUserUsecase(UserRepository())
