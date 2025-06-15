from typing import Sequence


class ApplicationError(Exception):
    ...


class TitleEmptyError(ApplicationError):
    ...


class InvalidReporterID(ApplicationError):
    def __init__(self, reporter_id: int, message: str = '') -> None:
        super().__init__(message)
        self.reporter_id = reporter_id


class InvalidAssigneeID(ApplicationError):
    def __init__(self, assignee_id: int, message: str = '') -> None:
        super().__init__(message)
        self.assignee_id = assignee_id


class InvalidRelatedTaskIDs(ApplicationError):
    def __init__(self, comment_ids: Sequence[int], message: str = '') -> None:
        """ Some or all of the related_task_ids are invalid """
        super().__init__(message)
        self.invalid_bunch_of_related_task_ids = comment_ids


class DomainValidationError(ApplicationError):
    ...
