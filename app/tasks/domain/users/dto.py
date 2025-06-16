from typing import Self

from pydantic import BaseModel

from tasks.domain.users.entity import UserEntity


class UserDTO(BaseModel):
    name: str
    user_id: int | None = None

    @classmethod
    def from_user(cls, user: UserEntity) -> Self:
        return cls(name=user.name, user_id=user.user_id)
