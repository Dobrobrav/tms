import pytest

from tasks.domain.tasks.repository import TaskRepository


@pytest.mark.django_db
def test__repository_indicates_entity_doesnt_exist() -> None:
    repo = TaskRepository()

    assert repo.exists(test_id := 777) == False
