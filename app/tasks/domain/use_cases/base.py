from abc import ABC, abstractmethod
from typing import Any

import icontract

from utils import log_error

_METHOD_NAME_FOR_EXECUTION = (
    # NOTE (SemenK): name of this constant should stay "_METHOD_NAME_FOR_EXECUTION"
    'execute'
)


class Usecase(ABC):
    @icontract.require(
        # NOTE: we need to make sure that the execution method's name
        # changes synchronously with '_METHOD_NAME_FOR_EXECUTION' value.
        # '_METHOD_NAME_FOR_EXECUTION' is used to dynamically wrap execution method with logging decorator
        # Alternatives would be:
        #   1. to explicitly wrap the method for each subclass. In this case we would have to remember to do it with each usecase
        #   2. to make execution method here non-abstract, wrap it with the decorator and make it call ._execute()
        #       method from subclasses. In this case we lose the method's arguments' and their types' hints,
        #       we would only see *args, **kwargs as hints when calling the execution method and would have to go
        #       to usecase's definition to see what parameters its execution method takes
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
