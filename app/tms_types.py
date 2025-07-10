from typing import TypeAlias, Generator, TypeVar, Protocol

from django.contrib.auth import get_user_model

UserModel: TypeAlias = get_user_model()

T = TypeVar('T')
Generator_: TypeAlias = Generator[T, None, None]


class BytesStream(Protocol):
    def read(self, size: int) -> bytes:
        ...
