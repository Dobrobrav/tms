import pytest
from rest_framework.test import APIClient


class TestUserAPI:

    @pytest.mark.django_db
    def test__when_user_is_created_then_returns_user_id(self) -> None:
        client = APIClient()
        user_data = {'name': 'test_name'}

        response = client.post('/tasks/users/', user_data, format='json')

        assert response.status_code == 201
        assert str.isdigit(str(response.json()['id']))

    @pytest.mark.django_db
    def test__when_user_is_created_then_it_can_be_retrieved(self):
        client = APIClient()
        user_data = {'name': 'test_name'}

        created_user_id = client.post('/tasks/users/', user_data, format='json').json()['id']
        created_user_response = client.get(f'/tasks/users/{created_user_id}')

        assert created_user_response.status_code == 200
        assert created_user_response.json()['name'] == user_data['name']
        assert created_user_response.json()['id'] == created_user_id
