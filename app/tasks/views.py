from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.domain.exceptions import (
    InvalidReporterID,
    InvalidAssigneeID,
    InvalidRelatedTaskIDs,
    TitleEmptyError,
)
from tasks.domain.tasks.dto import TaskDTO
from tasks.domain.use_cases.create_task import CreateTaskUsecase


# TODO: (for the future) think about logging
# Create your views here.
class TaskView(APIView):
    # TODO: use dicts instead of str for response data
    create_task_use_case: CreateTaskUsecase = None

    def post(self, request: Request) -> Response:
        try:
            task_dto = self._extract_data(request)
        except ValidationError as e:
            return Response({'errors': e.errors()}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f'unknown error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            self.create_task_use_case.execute(task_dto)
        except InvalidReporterID as e:
            return Response(f'invalid reporter ID: {e.reporter_id}', status=status.HTTP_400_BAD_REQUEST)
        except InvalidAssigneeID as e:
            return Response(f'invalid assignee ID: {e.assignee_id}', status=status.HTTP_400_BAD_REQUEST)
        except InvalidRelatedTaskIDs as e:
            return Response(
                f'some (or all) of the following related task IDs are invalid {e.invalid_bunch_of_related_task_ids}',
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TitleEmptyError:  # TODO: should I explicitly handle all possible domain errors?
            # TODO: Looks like it's better to group those errors into DomainError and catch it here
            # TODO: those errors could be specified in the icontract require decorator
            return Response('title must not be empty', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f'unknown error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response('ok', status=status.HTTP_201_CREATED)

    def _extract_data(self, request) -> TaskDTO:
        return TaskDTO(
            title=request.data['title'],
            reporter_id=request.data['reporter_id'],
            description=request.data['description'],
            related_task_ids=request.data.getlist('related_task_ids'),
            assignee_id=request.data['assignee_id'],
        )
