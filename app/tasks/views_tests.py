import uuid
from unittest.mock import Mock

import pytest
from pydantic import ValidationError
from rest_framework.test import APIRequestFactory

from tasks.domain.exceptions import (
    InvalidReporterID,
    InvalidAssigneeID,
    InvalidRelatedTaskIDs,
    TitleEmptyError,
    DomainValidationError,
)
from tasks.domain.use_cases.create_user import CreateUserUsecase
from tasks.domain.use_cases.get_user import GetUserUsecase
from tasks.views import TaskView, UserView


class TestCreatingTask:

    @pytest.mark.parametrize(
        "exception, status_code",
        [
            (InvalidReporterID(123), 400),
            (InvalidAssigneeID(123), 400),
            (InvalidRelatedTaskIDs([]), 400),
            (TitleEmptyError(123), 400),
            (Exception, 500),
        ],
    )
    def test__usecase_exceptions_cause_error_status_codes(
            self,
            exception: Exception,
            status_code: int,
    ) -> None:
        view = TaskView.as_view(create_task_usecase=(use_case := Mock()))
        use_case.execute.side_effect = exception
        task_data = {
            'title': 'test title',
            'reporter_id': uuid.uuid4(),
            'description': 'test description',
            'related_task_ids': [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
            'assignee_id': uuid.uuid4(),
        }
        request = APIRequestFactory().post("/tasks/", task_data)  # TODO: path seems to be missing prefix

        response = view(request)

        assert response.status_code == status_code

    def test__invalid_input_data_types_cause_400(self) -> None:
        view = TaskView.as_view(create_task_usecase=(stub_use_case := Mock()))
        stub_use_case.execute.side_effect = ValidationError  # TODO: use case DOESN'T CAUSE ValidationError!! Fix this
        task_data = {
            'title': 'test title',
            'reporter_id': 'invalid reporter id',
            'description': 'test description',
            'related_task_ids': 'invalid related task ids',
            'assignee_id': 'invalid assignee id',
        }
        request = APIRequestFactory().post("/tasks/", task_data)  # TODO: path seems to be missing prefix

        response = view(request)

        assert response.status_code == 400


class TestGettingUser:

    # TODO: add assertion for response text
    @pytest.mark.parametrize(
        'exception, status_code', [
            (Exception(), 500),
            (ValidationError('', []), 400),
            (DomainValidationError(), 400),
        ]
    )
    def test__usecase_exceptions_cause_error_status_codes(self, exception: Exception, status_code: int) -> None:
        view = UserView.as_view(get_user_usecase=(stub_use_case := Mock(spec=GetUserUsecase)))
        stub_use_case.execute.side_effect = exception
        request = APIRequestFactory().get('/tasks/users/{user_id}')
        test_user_id = 123

        response = view(request, user_id=test_user_id)

        assert response.status_code == status_code

    def test__user_view_returns_400_on_invalid_input_data(self) -> None:
        view = UserView.as_view(create_user_usecase=CreateUserUsecase(user_repo=Mock()))
        request = APIRequestFactory().post('/users/', data={'name': ''}, content_type='application/json')

        response = view(request)

        assert response.status_code == 400
