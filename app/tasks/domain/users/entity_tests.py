import pytest

from tasks.domain.exceptions import DomainValidationError
from tasks.domain.users.entity import UserEntity


def test_create_user_fails_if_provided_name_empty() -> None:
    with pytest.raises(DomainValidationError):
        UserEntity(name='')
