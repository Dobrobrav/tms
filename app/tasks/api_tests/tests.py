import random
from datetime import datetime, timedelta

import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestUserAPI:

    def test__when_user_is_created_then_api_returns_user_id(self, api_client: APIClient) -> None:
        user_data = {'name': 'test_name'}

        response = api_client.post(reverse('users'), user_data)

        assert response.status_code == 201
        assert str.isdigit(str(response.data['id']))

    def test__when_user_is_created_then_it_can_be_retrieved(self, api_client: APIClient) -> None:
        user_data = {'name': 'test_name'}

        created_user_id = api_client.post(reverse('users'), user_data).data['id']
        created_user_response = api_client.get(reverse('user', kwargs={'user_id': created_user_id}))

        assert created_user_response.status_code == 200
        assert created_user_response.data['name'] == user_data['name']
        assert created_user_response.data['id'] == created_user_id


@pytest.mark.django_db
def create_user(username: str) -> int:
    response = APIClient().post(reverse('users'), {'name': username})
    return response.data['id']


@pytest.mark.django_db
def create_2_tasks(reporter_id: int) -> list[int]:
    task_data_1 = {
        'title': 'title_1',
        'reporter_id': reporter_id,
    }
    task_data_2 = {
        'title': 'title_2',
        'reporter_id': reporter_id,
    }

    created_task_ids = [
        APIClient().post(path=reverse('tasks'), data=task_data_1).data['id'],
        APIClient().post(path=reverse('tasks'), data=task_data_2).data['id'],
    ]

    return created_task_ids


@pytest.mark.django_db
class TestTaskAPI:

    def test__when_task_is_created_api_returns_task_id(self, api_client: APIClient) -> None:
        test_title = 'test title'
        test_reporter_id = self._create_user(api_client, username='foo')
        test_description = 'test description'
        test_related_task_ids = self._create_2_tasks(api_client,
                                                     reporter_id=self._create_user(api_client, username='baz'))
        test_assignee_id = self._create_user(api_client, username='bar')

        task_data = {
            'title': test_title,
            'reporter_id': test_reporter_id,
            'description': test_description,
            'related_task_ids': test_related_task_ids,
            'assignee_id': test_assignee_id,
        }

        response = api_client.post(path=reverse('tasks'), data=task_data)

        assert response.status_code == 201
        assert str.isdigit(str(response.data['id']))

    def test__when_task_is_created_then_it_can_be_retrieved(self, api_client: APIClient) -> None:
        test_title = 'test title'
        test_reporter_id = self._create_user(api_client, username='foo')
        test_description = 'test description'
        test_related_task_ids = self._create_2_tasks(api_client,
                                                     reporter_id=self._create_user(api_client, username='baz'))
        test_assignee_id = self._create_user(api_client, username='bar')

        task_data = {
            'title': test_title,
            'reporter_id': test_reporter_id,
            'description': test_description,
            'related_task_ids': test_related_task_ids,
            'assignee_id': test_assignee_id,
        }

        created_task_id = api_client.post(path=reverse('tasks'), data=task_data).data['id']
        get_task_response = api_client.get(path=reverse('task', kwargs={'task_id': created_task_id}))

        assert get_task_response.status_code == 200
        assert get_task_response.data['title'] == test_title
        assert get_task_response.data['reporter_id'] == test_reporter_id
        assert get_task_response.data['description'] == test_description
        assert get_task_response.data['related_task_ids'] == test_related_task_ids
        assert get_task_response.data['assignee_id'] == task_data['assignee_id']
        assert get_task_response.data['id'] == created_task_id

    @pytest.mark.parametrize(
        'is_reporter_id_valid, is_assignee_id_valid, is_related_task_ids_valid',
        [
            (False, True, True),  # reporter_id is invalid
            (True, False, True),  # assignee_id is invalid
            (True, True, False),  # related_task_ids are invalid
        ]
    )
    def test__invalid_entity_ids_cause_400_when_creating_task(
            self,
            api_client: APIClient,
            is_reporter_id_valid: bool,
            is_assignee_id_valid: bool,
            is_related_task_ids_valid: bool,
    ) -> None:
        test_reporter_id = self._create_user(api_client, username='reporter', is_valid=is_reporter_id_valid, )
        test_assignee_id = self._create_user(api_client, username='assignee', is_valid=is_assignee_id_valid)
        test_related_task_ids = self._create_2_tasks(
            api_client,
            reporter_id=self._create_user(api_client, username='user for related tasks'),
            is_valid=is_related_task_ids_valid,
        )

        task_data = {
            'title': 'test_title',
            'reporter_id': test_reporter_id,
            'description': 'test_description',
            'related_task_ids': test_related_task_ids,
            'assignee_id': test_assignee_id,
        }

        task_response = api_client.post('/tasks/tasks/', task_data)

        assert task_response.status_code == 400

    @staticmethod
    def _create_user(api_client: APIClient, username: str | None = None, is_valid: bool = True) -> int:
        if not is_valid:
            return random.randint(-100_000, -10_000)

        assert username is not None
        response = api_client.post(reverse('users'), {'name': username})
        return response.data['id']

    @staticmethod
    def _create_2_tasks(api_client: APIClient, reporter_id: int | None = None, is_valid: bool = True) -> list[int]:
        if not is_valid:
            return [
                random.randint(-100_000, -10_000),
                random.randint(-100_000, -10_000),
            ]

        assert reporter_id is not None
        task_data_1 = {
            'title': 'title_1',
            'reporter_id': reporter_id,
        }
        task_data_2 = {
            'title': 'title_2',
            'reporter_id': reporter_id,
        }

        created_task_ids = [
            api_client.post(path=reverse('tasks'), data=task_data_1).data['id'],
            api_client.post(path=reverse('tasks'), data=task_data_2).data['id'],
        ]

        return created_task_ids


@pytest.mark.django_db
class TestCommentAPI:

    def test__when_comment_is_created_api_returns_comment_id(self, api_client: APIClient) -> None:
        test_user_id = self._create_user(api_client, 'test_commenter_id')
        test_reporter_id = self._create_user(api_client, 'test_reporter_id')
        test_task_id = self._create_task(api_client, test_reporter_id)
        test_text = 'test text'

        comment_response = api_client.post(
            path=reverse('comments'),
            data={'task_id': test_task_id, 'user_id': test_user_id, 'text': test_text},
        )

        assert comment_response.status_code == 201
        assert str.isdigit(str(comment_response.data['id']))

    def test__when_comment_is_created_then_it_can_be_retrieved(self, api_client: APIClient) -> None:
        test_user_id = self._create_user(api_client, 'test_commenter_id')
        test_reporter_id = self._create_user(api_client, 'test_reporter_id')
        test_task_id = self._create_task(api_client, test_reporter_id)
        test_text = 'test text'
        comment_id = self._create_comment(api_client, test_task_id, test_text, test_user_id)

        comment_response = api_client.get(reverse('comment', kwargs={'comment_id': comment_id}))

        assert comment_response.status_code == 200
        assert comment_response.data['user_id'] == test_user_id
        assert comment_response.data['text'] == test_text
        self._assert_create_time_roughly_equals_now(comment_response.data['create_time'])

    def test__when_comment_is_created_then_it_can_be_seen_in_task(self, api_client: APIClient) -> None:
        test_user_id = self._create_user(api_client, 'test_commenter_id')
        test_reporter_id = self._create_user(api_client, 'test_reporter_id')
        test_task_id = self._create_task(api_client, test_reporter_id)
        test_text = 'test text'
        comment_id = self._create_comment(api_client, test_task_id, test_text, test_user_id)

        task_response = api_client.get(path=reverse('task', kwargs={'task_id': test_task_id}))

        assert task_response.status_code == 200
        assert task_response.data['comments'] == [
            {
                'id': comment_id,
                'user_id': test_user_id,
                'text': test_text,
            }
        ]

    def _create_user(self, api_client: APIClient, username: str):
        return api_client.post(reverse('users'), {'name': username}).data['id']

    def _create_task(self, api_client: APIClient, test_reporter_id: int):
        return api_client.post(
            path=reverse('tasks'),
            data={'title': 'test_title', 'reporter_id': test_reporter_id},
        ).data['id']

    def _create_comment(self, api_client: APIClient, test_task_id: int, test_text: str, test_user_id: int):
        return api_client.post(
            path=reverse('comments'),
            data={'task_id': test_task_id, 'user_id': test_user_id, 'text': test_text},
        ).data['id']

    def _assert_create_time_roughly_equals_now(self, create_time_str: str):
        datetime_from_response = datetime.fromisoformat(create_time_str).replace(tzinfo=None)
        allowed_delta = timedelta(minutes=1)
        assert datetime.now() - datetime_from_response < allowed_delta
