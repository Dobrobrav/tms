import structlog
from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from rest_framework.views import APIView

from tasks.domain.comments.dto import CommentDTO
from tasks.domain.exceptions import (
    InvalidReporterID,
    InvalidAssigneeID,
    InvalidRelatedTaskIDs,
    TitleEmptyError,
    DomainValidationError,
)
from tasks.domain.tasks.dto import TaskDTO
from tasks.domain.use_cases.create_comment import CreateCommentUsecase
from tasks.domain.use_cases.create_task import CreateTaskUsecase
from tasks.domain.use_cases.create_user import CreateUserUsecase
from tasks.domain.use_cases.get_comment import GetCommentUsecase
from tasks.domain.use_cases.get_task import GetTaskUsecase
from tasks.domain.use_cases.get_user import GetUserUsecase
from tasks.domain.users.dto import UserDTO
from utils import log_error

logger = structlog.get_logger(__name__)


class UserView(APIView):
    create_user_usecase: CreateUserUsecase = None
    get_user_usecase: GetUserUsecase = None

    def get(self, request: Request, user_id: int) -> Response:
        try:
            user_dto = self.get_user_usecase.execute(user_id)
        except (DomainValidationError, ValidationError) as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'unknown error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={'id': user_dto.user_id, 'name': user_dto.name})

    def post(self, request: Request) -> Response:
        try:
            user_dto = self._extract_data(request)
            user_id = self.create_user_usecase.execute(user_dto)
        except (DomainValidationError, ValidationError) as e:
            return Response({'validation error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f'unknown error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'id': user_id}, status=status.HTTP_201_CREATED)

    @log_error
    def _extract_data(self, request: Request) -> UserDTO:
        return UserDTO(
            name=request.data['name'],
        )


class TaskView(APIView):
    create_task_usecase: CreateTaskUsecase = None
    get_task_usecase: GetTaskUsecase = None

    def get(self, request: Request, task_id: int) -> Response:
        # TODO: add error handling (first write tests)
        task_dto = self.get_task_usecase.execute(task_id)
        return Response(
            data={
                'id': task_id,
                'title': task_dto.title,
                'reporter_id': task_dto.reporter_id,
                'description': task_dto.description,
                'comments': [
                    {
                        'id': c.comment_id,
                        'user_id': c.user_id,
                        'text': c.text,
                    }
                    for c in task_dto.comments
                ],
                'related_task_ids': task_dto.related_task_ids,
                'assignee_id': task_dto.assignee_id,
            },
            status=HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        try:
            task_dto = self._extract_data(request)
            task_id = self.create_task_usecase.execute(task_dto)
        except (
                ValidationError, DomainValidationError,
                InvalidReporterID, InvalidAssigneeID,
                InvalidRelatedTaskIDs,
        ) as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        except TitleEmptyError:
            return Response('title must not be empty', status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(f'unknown error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'id': task_id}, status=status.HTTP_201_CREATED)

    @log_error
    def _extract_data(self, request) -> TaskDTO:
        return TaskDTO(
            title=request.data['title'],
            reporter_id=request.data['reporter_id'],
            description=request.data.get('description', ''),
            related_task_ids=request.data.getlist('related_task_ids'),
            assignee_id=request.data.get('assignee_id'),
        )


class CommentView(APIView):
    create_comment_usecase: CreateCommentUsecase = None
    get_comment_usecase: GetCommentUsecase = None

    def post(self, request: Request) -> Response:
        try:
            comment_dto = self._extract_data(request)
            comment_id = self.create_comment_usecase.execute(comment_dto)
        except Exception:
            return Response({'error': 'unknown error'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'id': comment_id}, status=HTTP_201_CREATED)

    @log_error
    def _extract_data(self, request: Request):
        return CommentDTO(
            text=request.data['text'],
            user_id=request.data['user_id'],
            task_id=request.data['task_id'],
        )

    def get(self, request: Request, comment_id: int) -> Response:
        try:
            comment_dto = self.get_comment_usecase.execute(comment_id)
        except Exception:
            raise NotImplementedError()
        else:
            return Response(
                data={'user_id': comment_dto.user_id, 'text': comment_dto.text, 'create_time': comment_dto.create_time_str},
                status=HTTP_200_OK,
            )
