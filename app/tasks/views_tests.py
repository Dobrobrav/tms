from unittest.mock import Mock

import pytest
from pydantic import ValidationError
from rest_framework.test import APIRequestFactory

from tasks.domain.exceptions import (
    TitleEmptyError,
    DomainValidationError,
)
from tasks.domain.use_cases.create_comment import CreateCommentUsecase
from tasks.domain.use_cases.create_user import CreateUserUsecase
from tasks.domain.use_cases.get_user import GetUserUsecase
from tasks.views import TaskView, UserView, CommentView


class TestCreatingTask:

    @pytest.mark.parametrize(
        "exception, status_code",
        [
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
            'reporter_id': 123,
            'description': 'test description',
            'related_task_ids': [14, 88, 228],
            'assignee_id': 456,
        }
        request = APIRequestFactory().post("/tasks/tasks/", task_data)

        response = view(request)

        assert response.status_code == status_code


class TestGettingUser:

    @pytest.mark.parametrize(
        'exception, status_code', [
            (Exception(), 500),
            (ValidationError('', []), 400),
            (DomainValidationError(), 400),
        ]
    )
    def test__usecase_exceptions_cause_error_status_codes(self, exception: Exception, status_code: int) -> None:
        sut_view = UserView.as_view(get_user_usecase=(stub_use_case := Mock(spec=GetUserUsecase)))
        stub_use_case.execute.side_effect = exception
        test_user_id = 123
        request = APIRequestFactory().get(f'/tasks/users/{test_user_id}')

        response = sut_view(request, user_id=test_user_id)

        assert response.status_code == status_code

    def test__user_view_returns_400_on_invalid_input_data(self) -> None:
        view = UserView.as_view(get_user_usecase=GetUserUsecase(user_repo=Mock()))
        test_user_id = 'invalid id'
        request = APIRequestFactory().get(f'/tasks/users/{test_user_id}')

        response = view(request, user_id=test_user_id)

        assert response.status_code == 400


class TestCreatingUser:

    @pytest.mark.parametrize(
        'exception, status_code', [
            (Exception(), 500),
            (ValidationError('', []), 400),
            (DomainValidationError(), 400),
        ]
    )
    def test__usecase_exceptions_cause_error_status_codes(self, exception: Exception, status_code: int) -> None:
        view = UserView.as_view(create_user_usecase=(stub_use_case := Mock(spec=CreateUserUsecase)))
        stub_use_case.execute.side_effect = exception
        request = APIRequestFactory().post('/tasks/users/', data={'name': 'test name'})

        response = view(request)

        assert response.status_code == status_code

    def test__user_view_returns_400_on_invalid_input_data(self) -> None:
        view = UserView.as_view(create_user_usecase=GetUserUsecase(user_repo=Mock()))
        request = APIRequestFactory().post('/tasks/users/', data={'name': ''})

        response = view(request)

        assert response.status_code == 400
