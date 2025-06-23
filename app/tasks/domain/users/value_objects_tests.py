import pytest
from pydantic import ValidationError

from tasks.domain.users.value_objects import UserName


def test_username_cannot_be_empty():
    with pytest.raises(ValidationError):
        UserName(value="")
