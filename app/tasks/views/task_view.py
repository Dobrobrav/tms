from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from tasks.domain.tasks.dto import TaskDTO
from tasks.exceptions import (
    DomainValidationError,
    InvalidTaskID,
    InvalidReporterID,
    InvalidAssigneeID,
    InvalidRelatedTaskIDs,
    TitleEmptyError,
)
from tasks.use_cases.create_task import CreateTaskUsecase
from tasks.use_cases.get_task import GetTaskUsecase
from utils import log_error


class TaskView(APIView):
    create_task_usecase: CreateTaskUsecase = None
    get_task_usecase: GetTaskUsecase = None

    def get(self, request: Request, task_id: int) -> Response:
        # TODO: add error handling (first write tests). Should I remove this todo?
        try:
            task_dto = self.get_task_usecase.execute(task_id)
        except InvalidTaskID as e:
            return Response({'validation error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(f'unknown error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return self._form_get_response(task_dto, task_id)

    def _form_get_response(self, task_dto: TaskDTO, task_id: int) -> Response:
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
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except TitleEmptyError:
            return Response('title must not be empty', status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(f'unknown error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'id': task_id}, status=status.HTTP_201_CREATED)

    @log_error
    def _extract_data(self, request: Request) -> TaskDTO:
        return TaskDTO(
            title=request.data['title'],
            reporter_id=request.data['reporter_id'],
            description=request.data.get('description') or '',
            related_task_ids=request.data.get('related_task_ids'),
            assignee_id=request.data.get('assignee_id'),
        )
