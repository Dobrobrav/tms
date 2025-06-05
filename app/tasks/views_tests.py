import uuid
from unittest.mock import Mock

import pytest
from pydantic import ValidationError
from rest_framework.test import APIRequestFactory

from tasks.domain.exceptions import InvalidReporterID, InvalidAssigneeID, InvalidRelatedTaskIDs, TitleEmptyError
from tasks.views import TaskView


@pytest.mark.parametrize(
    "exception, status_code",
    [
        (InvalidReporterID(uuid.uuid4()), 400),
        (InvalidAssigneeID(uuid.uuid4()), 400),
        (InvalidRelatedTaskIDs([uuid.uuid4()]), 400),
        (TitleEmptyError(uuid.uuid4()), 400),
        (Exception, 500),
    ],
)
def test_task_view_returns_error_status_codes_on_usecase_exceptions(
        exception: Exception,
        status_code: int,
) -> None:
    # Arrange
    view = TaskView.as_view(create_task_use_case=(use_case := Mock()))
    use_case.execute.side_effect = exception

    task_data = {
        'title': 'test title',
        'reporter_id': uuid.uuid4(),
        'description': 'test description',
        'related_task_ids': [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
        'assignee_id': uuid.uuid4(),
        # 'task_id': None
    }
    request = APIRequestFactory().post("/tasks/", task_data)

    # Act
    response = view(request)

    # Assert
    assert response.status_code == status_code


def test_task_view_returns_400_on_invalid_input_data_types() -> None:  # Arrange
    view = TaskView.as_view(create_task_use_case=(use_case := Mock()))
    use_case.execute.side_effect = ValidationError

    task_data = {
        'title': 'test title',
        'reporter_id': 'invalid reporter id',
        'description': 'test description',
        'related_task_ids': 'invalid related task ids',
        'assignee_id': 'invalid assignee id',
        # 'task_id': None
    }
    request = APIRequestFactory().post("/tasks/", task_data)

    # Act
    response = view(request)

    # Assert
    assert response.status_code == 400
