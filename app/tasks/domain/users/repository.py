from typing import Sequence
from uuid import UUID

from tasks.domain.base_repository import Repository
from tasks.domain.users.entity import UserEntity
from tms_types import UserModel


class UserRepository(Repository):
    def get(self, entity_id: int) -> UserEntity:
        user = UserModel.objects.get(pk=entity_id)
        return UserEntity(name=user.username, user_id=user.pk)

    def set(self, entity: UserEntity) -> int:
        user_already_exists = entity.user_id
        if user_already_exists:
            # NOTE (SemenK): not tested
            UserModel.objects.filter(pk=entity.user_id).update(username=entity.name)
            return entity.user_id
        else:
            created_user = UserModel.objects.create(username=entity.name)
            return created_user.pk

    def exists(self, id_or_ids: int | Sequence[UUID]) -> bool:
        """ Returns true if ALL provided ids exist in repo """
        ids = [id_or_ids] if isinstance(id_or_ids, int) else id_or_ids
        return UserModel.objects.filter(pk__in=list(ids)).count() == len(ids)
