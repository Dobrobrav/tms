import uuid
from typing import Sequence
from unittest.mock import Mock

import pytest

from tasks.domain.exceptions import (
    InvalidRelatedTaskIDs,
    InvalidAssigneeID,
    InvalidReporterID,
)
from tasks.domain.tasks.dto import TaskDTO
from tasks.domain.tasks.repository import TaskRepository
from tasks.domain.use_cases.create_task import CreateTaskUsecase
from tasks.domain.users.repository import UserRepository


@pytest.mark.parametrize(
    ('provided_related_tasks_exist, '
     'provided_reporter_exists, '
     'provided_assignee_exists, '
     'expected_error'),
    [
        (True, True, False, InvalidAssigneeID),
        (True, False, True, InvalidReporterID),
        (False, True, True, InvalidRelatedTaskIDs),
    ]
)
def test_create_task_usecase_raises_on_invalid_input_data(
        provided_related_tasks_exist: bool,
        provided_reporter_exists: bool,
        provided_assignee_exists: bool,
        expected_error: type[Exception],
) -> None:
    # arrange
    def _user_repo_exists_mock(id_or_ids: uuid.UUID | Sequence[uuid.UUID]) -> bool:
        if id_or_ids == test_reporter_id:
            return provided_reporter_exists
        elif id_or_ids == test_assignee_id:
            return provided_assignee_exists
        else:
            raise ValueError()

    use_case = CreateTaskUsecase(
        task_repo=(task_repo := Mock(spec=TaskRepository)),
        user_repo=(user_repo := Mock(spec=UserRepository)),
    )

    user_repo.exists = _user_repo_exists_mock
    task_repo.exists.return_value = provided_related_tasks_exist

    task_dto = TaskDTO(
        title="Sample Task",
        reporter_id=(test_reporter_id := 123),
        description="This is a sample task.",
        assignee_id=(test_assignee_id := 456),
        related_task_ids=[123, 456],
        task_id=123,
    )

    # act & assert
    with pytest.raises(expected_error):
        use_case.execute(task_dto)
