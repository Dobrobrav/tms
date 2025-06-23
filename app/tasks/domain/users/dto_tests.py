from tasks.domain.users.dto import UserDTO
from tasks.domain.users.user import UserEntity
from tasks.domain.users.value_objects import UserName


def test__dto_casted_from_user_entity_has_correct_data() -> None:
    user_entity = UserEntity(name=UserName(value="John Doe"), user_id=123)

    user_dto = UserDTO.from_entity(user_entity)

    assert user_dto.user_id == user_entity.user_id
    assert user_dto.name == user_entity.name
