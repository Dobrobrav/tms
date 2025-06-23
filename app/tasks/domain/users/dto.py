from typing import Self

from pydantic import BaseModel

from tasks.domain.users.user import UserEntity


class UserDTO(BaseModel):
    name: str | None = None
    user_id: int | None = None

    @classmethod
    def from_entity(cls, user: UserEntity) -> Self:
        return cls(name=user.name, user_id=user.user_id)
