import uuid
from typing import Sequence
from unittest.mock import Mock

import pytest

from tasks.domain.comments.repository import CommentRepository
from tasks.domain.exceptions import (
    InvalidRelatedTaskIDs,
    InvalidAssigneeID,
    InvalidReporterID,
    InvalidCommentIDs,
)
from tasks.domain.tasks.dto import TaskDTO
from tasks.domain.tasks.repository import TaskRepository
from tasks.domain.use_cases.create_task import CreateTaskUsecase
from tasks.domain.users.repository import UserRepository


@pytest.mark.parametrize(
    ('task_repo_return_on_exists, '
     'comment_repo_return_on_exists, '
     'user_repo_return_on_exists_with_reporter_id, '
     'user_repo_return_on_exists_with_assignee_id, '
     'expected_error'),
    [
        (True, True, True, False, InvalidAssigneeID),
        (True, True, False, True, InvalidReporterID),
        (True, False, True, True, InvalidCommentIDs),
        (False, True, True, True, InvalidRelatedTaskIDs),
    ]
)
def test_usecase_raises_errors_on_invalid_input_data(
        task_repo_return_on_exists: bool,
        comment_repo_return_on_exists: bool,
        user_repo_return_on_exists_with_reporter_id: bool,
        user_repo_return_on_exists_with_assignee_id: bool,
        expected_error: type[Exception],
) -> None:
    # arrange
    def _user_repo_exists_mock(id_or_ids: uuid.UUID | Sequence[uuid.UUID]):
        if id_or_ids == test_reporter_id:
            return user_repo_return_on_exists_with_reporter_id
        elif id_or_ids == test_assignee_id:
            return user_repo_return_on_exists_with_assignee_id
        else:
            raise ValueError()

    use_case = CreateTaskUsecase(
        task_repo=(task_repo := Mock(spec=TaskRepository)),
        user_repo=(user_repo := Mock(spec=UserRepository)),
        comment_repo=(comment_repo := Mock(spec=CommentRepository)),
    )

    user_repo.exists = _user_repo_exists_mock
    task_repo.exists.return_value = task_repo_return_on_exists
    comment_repo.exists.return_value = comment_repo_return_on_exists

    task_dto = TaskDTO(
        title="Sample Task",
        reporter_id=(test_reporter_id := uuid.uuid4()),
        description="This is a sample task.",
        comment_ids=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
        assignee_id=(test_assignee_id := uuid.uuid4()),
        related_task_ids=[uuid.uuid4(), uuid.uuid4()],
        task_id=uuid.uuid4(),
    )

    # act & assert
    with pytest.raises(expected_error):
        use_case.execute(task_dto)

# TODO: add integration test(s)
