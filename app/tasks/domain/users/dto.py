from typing import Self

from pydantic import BaseModel

from tasks.domain.users.entity import UserEntity


class UserDTO(BaseModel):
    name: str
    user_id: int | None = None

    @classmethod
    def from_entity(cls, user: UserEntity) -> Self:
        return cls(name=user.name, user_id=user.user_id)

    def to_entity(self) -> UserEntity:
        return UserEntity(name=self.name, user_id=self.user_id)
