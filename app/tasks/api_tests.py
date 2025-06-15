import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserAPI:

    def test__when_user_is_created_then_api_returns_user_id(self) -> None:
        user_data = {'name': 'test_name'}

        response = APIClient().post('/tasks/users/', user_data)

        assert response.status_code == 201
        assert str.isdigit(str(response.json()['id']))

    def test__when_user_is_created_then_it_can_be_retrieved(self) -> None:
        client = APIClient()
        user_data = {'name': 'test_name'}

        created_user_id = client.post('/tasks/users/', user_data).json()['id']
        created_user_response = client.get(f'/tasks/users/{created_user_id}')

        assert created_user_response.status_code == 200
        assert created_user_response.json()['name'] == user_data['name']
        assert created_user_response.json()['id'] == created_user_id


@pytest.mark.django_db
class TestTaskAPI:

    def test__when_task_is_created_api_returns_task_id(self) -> None:
        test_title = 'test title'
        test_reporter_id = self._create_user(username='foo')
        test_description = 'test description'
        test_related_task_ids = self._create_2_tasks(reporter_id=self._create_user('baz'))
        test_assignee_id = self._create_user(username='bar')

        task_data = {
            'title': test_title,
            'reporter_id': test_reporter_id,
            'description': test_description,
            'related_task_ids': test_related_task_ids,
            'assignee_id': test_assignee_id,
        }

        response = APIClient().post('/tasks/tasks/', data=task_data)

        assert response.status_code == 201
        assert str.isdigit(str(response.json()['id']))

    def _create_user(self, username: str) -> int:
        response = APIClient().post('/tasks/users/', {'name': username})
        return response.json()['id']

    def _create_2_tasks(self, reporter_id: int) -> list[int]:
        task_data_1 = {
            'title': 'title_1',
            'reporter_id': reporter_id,
        }
        task_data_2 = {
            'title': 'title_2',
            'reporter_id': reporter_id,
        }

        post = APIClient().post('/tasks/tasks/', data=task_data_1)
        created_task_ids = [
            post.json()['id'],
            APIClient().post('/tasks/tasks/', data=task_data_2).json()['id'],
        ]

        return created_task_ids

    def test__when_task_is_created_then_it_can_be_retrieved(self) -> None:
        test_title = 'test title'
        test_reporter_id = self._create_user(username='foo')
        test_description = 'test description'
        test_related_task_ids = self._create_2_tasks(reporter_id=self._create_user('baz'))
        test_assignee_id = self._create_user(username='bar')

        task_data = {
            'title': test_title,
            'reporter_id': test_reporter_id,
            'description': test_description,
            'related_task_ids': test_related_task_ids,
            'assignee_id': test_assignee_id,
        }

        created_task_id = APIClient().post('/tasks/tasks/', data=task_data).json()['id']
        get_task_response = APIClient().get(f'/tasks/tasks/{created_task_id}')

        assert get_task_response.status_code == 200
        assert get_task_response.json()['title'] == task_data['title']
        assert get_task_response.json()['reporter_id'] == task_data['reporter_id']
        assert get_task_response.json()['description'] == task_data['description']
        assert get_task_response.json()['related_task_ids'] == task_data['related_task_ids']
        assert get_task_response.json()['assignee_id'] == task_data['assignee_id']
        assert get_task_response.json()['id'] == created_task_id
