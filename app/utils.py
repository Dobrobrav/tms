from functools import wraps
from typing import Callable

import structlog

logger = structlog.get_logger(__name__)


def log_error[T](callable_: Callable[..., T]) -> Callable[..., T]:
    @wraps(callable_)
    def wrapper(*args, **kwargs) -> T:
        try:
            return callable_(*args, **kwargs)
        except Exception as e:
            # TODO: potentially add if-statement to avoid logging errors which are not supposed to be logged
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
            raise e

    return wrapper
