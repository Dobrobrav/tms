from pydantic import ValidationError
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView

from tasks.domain.comments.dto import CommentDTO
from tasks.exceptions import DomainValidationError, CommentNotExists
from tasks.use_cases.create_comment import CreateCommentUsecase
from tasks.use_cases.get_comment import GetCommentUsecase
from utils import log_error


@parser_classes([JSONParser])
class CommentView(APIView):
    create_comment_usecase: CreateCommentUsecase = None
    get_comment_usecase: GetCommentUsecase = None

    def post(self, request: Request) -> Response:
        try:
            comment_dto, task_id = self._extract_data(request)
            comment_id = self.create_comment_usecase.execute(comment_dto, task_id)
        except (DomainValidationError, ValidationError) as e:
            return Response({'validation error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'unknown error'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'id': comment_id}, status=HTTP_201_CREATED)

    @log_error
    def _extract_data(self, request: Request) -> tuple[CommentDTO, int]:
        return (
            CommentDTO(text=request.data['text'], user_id=request.data['user_id']),
            request.data['task_id'],
        )

    def get(self, request: Request, comment_id: str) -> Response:
        try:
            comment_id = CommentDTO(comment_id=comment_id).comment_id
            comment_dto, task_id = self.get_comment_usecase.execute(comment_id)
        except ValidationError as e:
            return Response({'validation error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except CommentNotExists as e:
            return Response({'error': str(e)}, status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'unknown error'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            data={
                'user_id': comment_dto.user_id, 'text': comment_dto.text,
                'create_time': comment_dto.create_time_str,
                'task_id': task_id,
            },
            status=HTTP_200_OK,
        )
