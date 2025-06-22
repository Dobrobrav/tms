from tasks.domain.users.dto import UserDTO
from tasks.domain.users.user import UserEntity


def test__dto_casted_from_user_entity_has_correct_data() -> None:
    user_entity = UserEntity(name="John Doe", user_id=123)

    user_dto = UserDTO.from_entity(user_entity)

    assert user_dto.user_id == user_entity.user_id
    assert user_dto.name == user_entity.name


def test__cast_user_entity_to_dto_then_cast_dto_to_entity_equals_original_entity() -> None:
    original_user_entity = UserEntity(name="John Doe", user_id=123)

    user_dto = UserDTO.from_entity(original_user_entity)
    user_entity = user_dto.to_entity()

    assert user_entity.name == original_user_entity.name, f"Name mismatch: {user_entity.name} != {original_user_entity.name}"
    assert user_entity.user_id == original_user_entity.user_id, f"User ID mismatch: {user_entity.user_id} != {original_user_entity.user_id}"
