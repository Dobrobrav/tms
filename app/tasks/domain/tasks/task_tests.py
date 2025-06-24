import pytest

from tasks.domain.exceptions import DomainValidationError
from tasks.domain.tasks.task import TaskEntity


def test__cant_create_task_with_empty_title() -> None:
    with pytest.raises(DomainValidationError):
        TaskEntity(
            title='',
            reporter_id=123,
            description="This is a sample task.",
            comments=[],
            related_task_ids=[],
        )
