from tasks.domain.users.dto import UserDTO
from tasks.domain.users.repository import UserRepository
from tasks.domain.users.user import UserEntity
from tasks.domain.users.value_objects import UserName
from tasks.use_cases.base_usecase import Usecase


class CreateUserUsecase(Usecase):
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    def execute(self, user_dto: UserDTO) -> int:
        user_entity = UserEntity(name=UserName(value=user_dto.name))
        user_id = self._user_repo.set(user_entity)
        return user_id


def create_user_usecase_factory() -> CreateUserUsecase:
    return CreateUserUsecase(UserRepository())
