from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.domain.exceptions import DomainValidationError, UserNotExists
from tasks.domain.use_cases.create_user import CreateUserUsecase
from tasks.domain.use_cases.get_user import GetUserUsecase
from tasks.domain.users.dto import UserDTO
from utils import log_error


class UserView(APIView):
    create_user_usecase: CreateUserUsecase = None
    get_user_usecase: GetUserUsecase = None

    def get(self, request: Request, user_id: str) -> Response:
        try:
            user_dto = UserDTO(user_id=user_id)
            user_dto = self.get_user_usecase.execute(user_dto.user_id)
        except (DomainValidationError, ValidationError) as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)
        except UserNotExists as e:
            return Response({'error': str(e)}, status.HTTP_404_NOT_FOUND)
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
            return Response({'error': 'unknown error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'id': user_id}, status=status.HTTP_201_CREATED)

    @log_error
    def _extract_data(self, request: Request) -> UserDTO:
        return UserDTO(
            name=request.data['name'],
        )
