from tasks.domain.users.dto import UserDTO
from tasks.domain.users.repository import UserRepository
from tasks.use_cases.base_usecase import Usecase


class GetUserUsecase(Usecase):
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    def execute(self, user_id: int) -> UserDTO:
        user = self._user_repo.get(user_id)
        return UserDTO.from_entity(user)


def get_user_usecase_factory() -> GetUserUsecase:
    return GetUserUsecase(user_repo=UserRepository())
