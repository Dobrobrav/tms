import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestUserAPI:

    def test__when_user_is_created_then_api_returns_user_id(self, api_client: APIClient) -> None:
        user_data = {'name': 'test_name'}

        response = api_client.post('/tasks/users/', user_data)

        assert response.status_code == 201
        assert str.isdigit(str(response.data['id']))

    def test__when_user_is_created_then_it_can_be_retrieved(self, api_client: APIClient) -> None:
        user_data = {'name': 'test_name'}

        created_user_id = api_client.post('/tasks/users/', user_data).data['id']
        created_user_response = api_client.get(f'/tasks/users/{created_user_id}')

        assert created_user_response.status_code == 200
        assert created_user_response.data['name'] == user_data['name']
        assert created_user_response.data['id'] == created_user_id


@pytest.mark.django_db
class TestTaskAPI:
    def test__when_task_is_created_api_returns_task_id(self, api_client: APIClient) -> None:
        test_title = 'test title'
        test_reporter_id = self._create_user(api_client, username='foo')
        test_description = 'test description'
        test_related_task_ids = self._create_2_tasks(api_client, reporter_id=self._create_user(api_client, 'baz'))
        test_assignee_id = self._create_user(api_client, username='bar')

        task_data = {
            'title': test_title,
            'reporter_id': test_reporter_id,
            'description': test_description,
            'related_task_ids': test_related_task_ids,
            'assignee_id': test_assignee_id,
        }

        response = api_client.post('/tasks/tasks/', data=task_data)

        assert response.status_code == 201
        assert str.isdigit(str(response.data['id']))

    def _create_user(self, api_client: APIClient, username: str) -> int:
        response = api_client.post('/tasks/users/', {'name': username})
        return response.data['id']

    def _create_2_tasks(self, api_client: APIClient, reporter_id: int) -> list[int]:
        task_data_1 = {
            'title': 'title_1',
            'reporter_id': reporter_id,
        }
        task_data_2 = {
            'title': 'title_2',
            'reporter_id': reporter_id,
        }

        created_task_ids = [
            api_client.post('/tasks/tasks/', data=task_data_1).data['id'],
            api_client.post('/tasks/tasks/', data=task_data_2).data['id'],
        ]

        return created_task_ids

    def test__when_task_is_created_then_it_can_be_retrieved(self, api_client: APIClient) -> None:
        test_title = 'test title'
        test_reporter_id = self._create_user(api_client, username='foo')
        test_description = 'test description'
        test_related_task_ids = self._create_2_tasks(api_client, reporter_id=self._create_user(api_client, 'baz'))
        test_assignee_id = self._create_user(api_client, username='bar')

        task_data = {
            'title': test_title,
            'reporter_id': test_reporter_id,
            'description': test_description,
            'related_task_ids': test_related_task_ids,
            'assignee_id': test_assignee_id,
        }

        created_task_id = api_client.post('/tasks/tasks/', data=task_data).data['id']
        get_task_response = api_client.get(f'/tasks/tasks/{created_task_id}')

        assert get_task_response.status_code == 200
        assert get_task_response.data['title'] == test_title
        assert get_task_response.data['reporter_id'] == test_reporter_id
        assert get_task_response.data['description'] == test_description
        assert get_task_response.data['related_task_ids'] == test_related_task_ids
        assert get_task_response.data['assignee_id'] == task_data['assignee_id']
        assert get_task_response.data['id'] == created_task_id


# TODO: how to check create_time ??
@pytest.mark.django_db
class TestCommentAPI:

    def test__when_comment_is_created_api_returns_comment_id(self, api_client: APIClient) -> None:
        test_user_id = api_client.post('/tasks/users/', {'name': 'test comment user'}).data['id']
        test_reporter_id = api_client.post('/tasks/users/', {'name': 'test reporter'}).data['id']
        test_task_id = api_client.post(
            '/tasks/tasks/',
            data={'title': 'test_title', 'reporter_id': test_reporter_id},
        ).data['id']
        test_text = 'test text'

        response = api_client.post(
            '/tasks/comments/',
            data={'task_id': test_task_id, 'user_id': test_user_id, 'text': test_text},
        )

        assert response.status_code == 201
        assert str.isdigit(str(response.data['id']))

    def test__when_comment_is_created_then_it_can_be_seen_in_task(self, api_client: APIClient) -> None:
        test_user_id = api_client.post('/tasks/users/', {'name': 'test comment user'}).data['id']
        test_reporter_id = api_client.post('/tasks/users/', {'name': 'test reporter'}).data['id']
        test_task_id = api_client.post(
            '/tasks/tasks/',
            data={'title': 'test_title', 'reporter_id': test_reporter_id},
        ).data['id']
        test_text = 'test text'
        comment_id = api_client.post(
            '/tasks/comments/',
            data={'task_id': test_task_id, 'user_id': test_user_id, 'text': test_text},
        ).data['id']

        response = api_client.get(f'/tasks/tasks/{test_task_id}')

        assert response.status_code == 200
        assert response.data['comments'] == [
            {
                'id': comment_id,
                'user_id': test_user_id,
                'text': test_text,
            }
        ]
