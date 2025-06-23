import pytest

from tasks.domain.users.repository import UserRepository


@pytest.mark.django_db
def test__repository_indicates_entity_doesnt_exist() -> None:
    repo = UserRepository()

    assert repo.exists(test_id := 777) == False
