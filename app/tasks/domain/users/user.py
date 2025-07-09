from tasks.domain.base_aggregate_root import AggregateRoot
from tasks.domain.users.value_objects import UserName


class UserEntity(AggregateRoot):
    def __init__(
            self,
            name: UserName,
            user_id: int | None = None,
    ) -> None:
        self._name = name
        self._user_id = user_id

    @property
    def name(self) -> str:
        return self._name.value

    @property
    def user_id(self) -> int:
        return self._user_id
