import icontract

from tasks.domain.aggregate_root import AggregateRoot
from tasks.domain.exceptions import DomainValidationError


class UserEntity(AggregateRoot):
    def __init__(
            self,
            name: str,
            user_id: int | None = None,
    ) -> None:
        self.name = name
        self._user_id = user_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    @icontract.require(lambda self, value: len(value) > 0, 'name must be non-empty', error=DomainValidationError)
    def name(self, value: str) -> None:
        self._name = value

    @property
    def user_id(self) -> int:
        return self._user_id
