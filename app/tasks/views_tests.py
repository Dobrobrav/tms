import os
from unittest.mock import Mock

import pytest
from django.core.validators import URLValidator
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from tasks.domain.attachments.repository import AttachmentRepository
from tasks.domain.tasks.repository import TaskRepository
from tasks.domain.users.repository import UserRepository
from tasks.use_cases.add_task_attachment import AddTaskAttachmentUsecase, AttachmentS3Uploader, \
    StorageForAttachmentS3Meta, S3Gateway
from tasks.use_cases.create_task import CreateTaskUsecase
from tasks.use_cases.create_user import CreateUserUsecase
from tasks.use_cases.get_user import GetUserUsecase
from tasks.views import TaskView, UserView, TaskAttachmentView


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


@pytest.mark.django_db
class TestTaskAttachmentView:

    def test__when_attachment_added__view_returns_attachment_url(self) -> None:
        # Arrange
        view = self._get_task_attachment_view(Mock(spec=S3Gateway))
        test_task_id = _create_minimal_task()

        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'file.jpeg')
        with open(fixture_path, 'rb') as file_stream:
            request = APIRequestFactory().generic(
                method='post',
                path=reverse('task-attachments', kwargs={'task_id': test_task_id}),
                data=file_stream.read(),
                headers={'Filename': 'foobar'},
            )

        # Act
        response = view(request, test_task_id)

        # Assert
        assert response.status_code == 201

        attachment_url = response.data['attachment_url']
        assert len(attachment_url) != 0
        URLValidator()(attachment_url)

    def test__when_attachment_added__s3_gateway_was_called_correctly(self) -> None:
        # Arrange
        m_s3_gateway = Mock(spec=S3Gateway)
        view = self._get_task_attachment_view(m_s3_gateway)
        test_task_id = _create_minimal_task()

        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'file.jpeg')
        with open(fixture_path, 'rb') as file_stream:
            test_filename = 'test_filename'
            request = APIRequestFactory().generic(
                method='post',
                path=reverse('task-attachments', kwargs={'task_id': test_task_id}),
                data=file_stream.read(),
                headers={'Filename': test_filename},
            )

        # Act
        view(request, test_task_id)

        # Assert
        m_s3_gateway.upload_file.assert_called_once()

        _, call_kwargs = m_s3_gateway.upload_file.call_args
        assert call_kwargs['filename'] == test_filename
        assert 'file_key' in call_kwargs

        with open(fixture_path, 'rb') as file_stream:
            expected_bytes = file_stream.read()
            assert call_kwargs['bytes_stream'].read() == expected_bytes

    @staticmethod
    def _get_task_attachment_view(m_s3_mock: Mock):
        return TaskAttachmentView.as_view(
            add_task_attachment_usecase=AddTaskAttachmentUsecase(
                task_repo=TaskRepository(),
                attachment_s3_uploader=AttachmentS3Uploader(s3_gateway=m_s3_mock),
                attachment_repo=AttachmentRepository(),
                storage_for_attachment_s3_meta=StorageForAttachmentS3Meta()
            )
        )


def _create_minimal_task() -> int:
    task_data = {'title': 'foo', 'reporter_id': _create_minimal_user()}
    view = TaskView.as_view(
        create_task_usecase=CreateTaskUsecase(
            task_repo=TaskRepository(),
            user_repo=UserRepository(),
        )
    )
    request = APIRequestFactory().post(reverse('tasks'), task_data)
    task_id = view(request).data['id']
    return task_id


def _create_minimal_user() -> int:
    view = UserView.as_view(create_user_usecase=CreateUserUsecase(user_repo=UserRepository()))
    request = APIRequestFactory().post(reverse('users'), data={'name': 'foobar'})
    user_id = view(request).data['id']
    return user_id
