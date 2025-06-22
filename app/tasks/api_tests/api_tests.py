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

    def test__when_creating_user__empty_name_causes_400(self, api_client: APIClient) -> None:
        create_user_response = api_client.post(reverse('users'), data={'name': ''})

        assert create_user_response.status_code == 400

    def test__when_getting_user__invalid_id_causes_400(self, api_client: APIClient):
        invalid_id = 'foobar'

        get_user_response = api_client.get(reverse('user', kwargs={'user_id': invalid_id}))

        assert get_user_response.status_code == 400

    def test__when_getting_user__non_existent_id_causes_404(self, api_client: APIClient):
        non_existent_id = 123

        get_user_response = api_client.get(reverse('user', kwargs={'user_id': non_existent_id}))

        assert get_user_response.status_code == 404


@pytest.mark.django_db
class TestTaskAPI:

    def test__when_task_is_created_api_returns_task_id(self, api_client: APIClient) -> None:
        test_title = 'test title'
        test_reporter_id = self._create_user(api_client, username='foo')
        test_description = 'test description'
        test_related_task_ids = create_n_tasks(
            api_client,
            reporter_id=self._create_user(api_client, username='baz'),
            n=2,
        )
        test_assignee_id = self._create_user(api_client, username='bar')

        task_data = {
            'title': test_title,
            'reporter_id': test_reporter_id,
            'description': test_description,
            'related_task_ids': test_related_task_ids,
            'assignee_id': test_assignee_id,
        }

        create_task_response = api_client.post(path=reverse('tasks'), data=task_data, format='json')

        assert create_task_response.status_code == 201
        assert str.isdigit(str(create_task_response.data['id']))

    def test__when_task_is_created_then_it_can_be_retrieved(self, api_client: APIClient) -> None:
        test_title = 'test title'
        test_reporter_id = self._create_user(api_client, username='foo')
        test_description = 'test description'
        test_related_task_ids = create_n_tasks(
            api_client,
            reporter_id=self._create_user(api_client, username='baz'),
            n=2,
        )
        test_assignee_id = self._create_user(api_client, username='bar')

        task_data = {
            'title': test_title,
            'reporter_id': test_reporter_id,
            'description': test_description,
            'related_task_ids': test_related_task_ids,
            'assignee_id': test_assignee_id,
        }

        created_task_id = api_client.post(reverse('tasks'), data=task_data, format='json').data['id']
        get_task_response = api_client.get(reverse('task', kwargs={'task_id': created_task_id}), format='json')

        assert get_task_response.status_code == 200
        assert get_task_response.data['title'] == test_title
        assert get_task_response.data['reporter_id'] == test_reporter_id
        assert get_task_response.data['description'] == test_description
        assert get_task_response.data['related_task_ids'] == test_related_task_ids
        assert get_task_response.data['assignee_id'] == task_data['assignee_id']
        assert get_task_response.data['id'] == created_task_id

    # TODO: make these tests fail to make sure they're correct
    @pytest.mark.parametrize(
        'is_reporter_id_valid, is_assignee_id_valid, is_related_task_ids_valid',
        [
            (False, True, True),  # reporter_id is invalid
            (True, False, True),  # assignee_id is invalid
            (True, True, False),  # related_task_ids are invalid
        ]
    )
    def test__when_creating_task__invalid_entity_ids_cause_400(
            self,
            api_client: APIClient,
            is_reporter_id_valid: bool,
            is_assignee_id_valid: bool,
            is_related_task_ids_valid: bool,
    ) -> None:
        test_reporter_id = self._create_user(api_client, username='reporter', is_valid=is_reporter_id_valid)
        test_assignee_id = self._create_user(api_client, username='assignee', is_valid=is_assignee_id_valid)
        test_related_task_ids = create_n_tasks(
            api_client,
            reporter_id=self._create_user(api_client, username='user for related tasks'),
            should_tasks_be_valid=is_related_task_ids_valid,
            n=2,
        )

        task_data = {
            'title': 'test_title',
            'reporter_id': test_reporter_id,
            'description': 'test_description',
            'related_task_ids': test_related_task_ids,
            'assignee_id': test_assignee_id,
        }

        task_response = api_client.post(reverse('tasks'), task_data)

        assert task_response.status_code == 400

    def test__invalid_task_id_cause_400_when_getting_task(self, api_client: APIClient) -> None:
        invalid_task_id = create_n_tasks(api_client, n=1, should_tasks_be_valid=False)[0]

        get_task_response = api_client.get(path=reverse('task', kwargs={'task_id': invalid_task_id}))

        assert get_task_response.status_code == 400

    def test__when_creating_task__empty_title_causes_400(self, api_client: APIClient) -> None:
        task_data = {
            'title': '',
            'reporter_id': self._create_user(api_client, username='reporter', is_valid=True),
        }

        create_task_response = api_client.post(reverse('tasks'), data=task_data)

        assert create_task_response.status_code == 400

    @staticmethod
    def _create_user(api_client: APIClient, username: str | None = None, is_valid: bool = True) -> int:
        if not is_valid:
            return random.randint(-100_000, -10_000)

        assert username is not None
        response = api_client.post(reverse('users'), {'name': username})
        return response.data['id']


def create_n_tasks(
        api_client: APIClient,
        reporter_id: int | None = None,
        should_tasks_be_valid: bool = True,
        n: int = 1,
) -> list[int]:
    if not should_tasks_be_valid:
        return [random.randint(10_000, 100_000) for _ in range(n)]

    assert reporter_id is not None

    created_task_ids = []
    for task_count in range(n):
        task_data = {
            'title': f'title_{task_count}',
            'reporter_id': reporter_id,
        }
        created_task_ids.append(api_client.post(path=reverse('tasks'), data=task_data, format='json').data['id'])

    return created_task_ids


@pytest.mark.django_db
class TestCommentAPI:

    def test__when_comment_is_created_api_returns_comment_id(self, api_client: APIClient) -> None:
        test_user_id = self._create_user(api_client, 'test_commenter_id')
        test_reporter_id = self._create_user(api_client, 'test_reporter_id')
        test_task_id = create_n_tasks(api_client, test_reporter_id, n=1)[0]
        test_text = 'test text'

        comment_response = api_client.post(
            path=reverse('comments'),
            data={'task_id': test_task_id, 'user_id': test_user_id, 'text': test_text},
            format='json',
        )

        assert comment_response.status_code == 201
        assert str.isdigit(str(comment_response.data['id']))

    def test__when_comment_is_created_then_it_can_be_retrieved(self, api_client: APIClient) -> None:
        test_user_id = self._create_user(api_client, 'test_commenter_id')
        test_reporter_id = self._create_user(api_client, 'test_reporter_id')
        test_task_id = create_n_tasks(api_client, test_reporter_id, n=1)[0]
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
        test_task_id = create_n_tasks(api_client, test_reporter_id, n=1)[0]
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

    def test__when_getting_comment__invalid_id_causes_400(self, api_client: APIClient):
        invalid_id = 'foobar'

        get_comment_response = api_client.get(reverse('comment', kwargs={'comment_id': invalid_id}))

        assert get_comment_response.status_code == 400

    def test__when_getting_user__non_existent_id_causes_404(self, api_client: APIClient):
        non_existent_id = 123

        get_user_response = api_client.get(reverse('comment', kwargs={'comment_id': non_existent_id}))

        assert get_user_response.status_code == 404

    def _create_user(self, api_client: APIClient, username: str):
        return api_client.post(reverse('users'), {'name': username}, format='json').data['id']

    def _create_comment(self, api_client: APIClient, test_task_id: int, test_text: str, test_user_id: int):
        return api_client.post(
            path=reverse('comments'),
            data={'task_id': test_task_id, 'user_id': test_user_id, 'text': test_text},
            format='json',
        ).data['id']

    def _assert_create_time_roughly_equals_now(self, create_time_str: str):
        datetime_from_response = datetime.fromisoformat(create_time_str).replace(tzinfo=None)
        allowed_delta = timedelta(minutes=1)
        assert datetime.now() - datetime_from_response < allowed_delta
