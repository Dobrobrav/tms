from unittest.mock import Mock

import pytest
from pydantic import ValidationError
from rest_framework.test import APIRequestFactory

from tasks.domain.exceptions import (
    DomainValidationError,
)
from tasks.domain.use_cases.create_user import CreateUserUsecase
from tasks.domain.use_cases.get_user import GetUserUsecase
from tasks.views import UserView


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
        test_user_id = 123
        request = APIRequestFactory().get(f'/tasks/users/{test_user_id}')

        response = view(request, user_id=test_user_id)

        assert response.status_code == status_code

    def test__user_view_returns_400_on_invalid_input_data(self) -> None:
        view = UserView.as_view(create_user_usecase=CreateUserUsecase(user_repo=Mock()))
        request = APIRequestFactory().post('/users/', data={'name': ''}, content_type='application/json')

        response = view(request)

        assert response.status_code == 400
