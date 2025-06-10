import structlog
from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.domain.exceptions import (
    DomainValidationError,
)
from tasks.domain.use_cases.create_user import CreateUserUsecase
from tasks.domain.use_cases.get_user import GetUserUsecase
from tasks.domain.users.dto import UserDTO
from utils import log_error

logger = structlog.get_logger(__name__)


class UserView(APIView):
    create_user_usecase: CreateUserUsecase = None
    get_user_usecase: GetUserUsecase = None

    # TODO: I could merge the try-except blocks to make the code more concise (otherwise, I need to to add except Exception for the first block)
    def post(self, request: Request) -> Response:
        try:
            user_dto = self._extract_data(request)
        except ValidationError as e:
            return Response({'validation error': e.errors()}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = self.create_user_usecase.execute(user_dto)
        except DomainValidationError as e:
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

    def get(self, request: Request, user_id: int) -> Response:
        try:
            user_dto = self.get_user_usecase.execute(user_id)
        except (DomainValidationError, ValidationError) as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': 'unknown error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={'id': user_dto.user_id, 'name': user_dto.name})
