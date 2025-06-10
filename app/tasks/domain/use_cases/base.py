from abc import ABC, abstractmethod
from typing import Any

import icontract

from utils import log_error

_METHOD_NAME_FOR_EXECUTION = (
    # NOTE (SemenK): added this constant to make sure that
    # name of this constant should stay "_METHOD_NAME_FOR_EXECUTION"
    'execute'
)


class Usecase(ABC):
    @icontract.require(
        lambda cls: hasattr(cls, _METHOD_NAME_FOR_EXECUTION),
        description=(f"To change '.{_METHOD_NAME_FOR_EXECUTION}' method's name, "
                     f"first change _METHOD_NAME_FOR_EXECUTION value.")
    )
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        ...

    def __getattribute__(self, item):
        attr = super().__getattribute__(item)

        if item == _METHOD_NAME_FOR_EXECUTION:
            assert callable(attr)
            return log_error(attr)
        else:
            return attr
