import structlog
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.use_cases.add_task_attachment import AddTaskAttachmentUsecase

logger = structlog.get_logger(__name__)


class TaskAttachmentView(APIView):
    add_task_attachment_usecase: AddTaskAttachmentUsecase = None

    def post(self, request: Request, task_id: str) -> Response:
        try:
            attachment_url = self.add_task_attachment_usecase.execute(
                task_id=int(task_id),
                filename=request.headers['Filename'],
                bytes_stream=request.stream,
            )
        except Exception:
            return Response(f'unknown error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'attachment_url': str(attachment_url)}, status=status.HTTP_201_CREATED)
