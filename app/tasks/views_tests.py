from unittest.mock import Mock

from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from tasks.domain.use_cases.create_user import CreateUserUsecase
from tasks.domain.use_cases.get_user import GetUserUsecase
from tasks.views import TaskView, UserView


class TestTaskView:

    def test__generic_exception_from_create_task_usecase_causes_500(self) -> None:
        view = TaskView.as_view(create_task_usecase=(m_use_case := Mock()))
        m_use_case.execute.side_effect = Exception()
        task_data = {
            'title': 'test title',
            'reporter_id': 123,
        }
        request = APIRequestFactory().post(reverse('tasks'), task_data)

        response = view(request)

        assert response.status_code == 500

    def test__generic_exception_from_get_task_usecase_causes_500(self) -> None:
        view = TaskView.as_view(create_task_usecase=(s_use_case := Mock()))
        s_use_case.execute.side_effect = Exception()
        request = APIRequestFactory().get(reverse('task', kwargs={'task_id': (task_id := 123)}))

        response = view(request, task_id=task_id)

        assert response.status_code == 500


class TestUserView:

    def test__generic_exception_from_get_user_usecase_causes_500(self) -> None:
        view = UserView.as_view(get_user_usecase=(s_use_case := Mock(spec=GetUserUsecase)))
        s_use_case.execute.side_effect = Exception()
        test_user_id = 123
        request = APIRequestFactory().get(f'/tasks/users/{test_user_id}')

        response = view(request, user_id=test_user_id)

        assert response.status_code == 500

    def test__generic_exception_from_create_user_usecase_causes_500(self) -> None:
        view = UserView.as_view(create_user_usecase=(s_use_case := Mock(spec=CreateUserUsecase)))
        s_use_case.execute.side_effect = Exception()
        request = APIRequestFactory().post('/tasks/users/', data={'name': 'test name'})

        response = view(request)

        assert response.status_code == 500
