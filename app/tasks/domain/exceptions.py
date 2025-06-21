from typing import Sequence


class ApplicationError(Exception):
    ...


class TitleEmptyError(ApplicationError):
    ...


class InvalidReporterID(ApplicationError):
    def __init__(self, reporter_id: int) -> None:
        super().__init__(f'invalid reporter ID: {reporter_id}')
        self.reporter_id = reporter_id


class InvalidAssigneeID(ApplicationError):
    def __init__(self, assignee_id: int) -> None:
        super().__init__(f'invalid assignee ID: {assignee_id}')
        self.assignee_id = assignee_id


class InvalidTaskID(ApplicationError):
    def __init__(self, task_id: int) -> None:
        super().__init__(f'invalid task ID: {task_id}')
        self.task_id = task_id


class InvalidRelatedTaskIDs(ApplicationError):
    def __init__(self, task_ids: Sequence[int]) -> None:
        """ Some or all of the related_task_ids are invalid """
        super().__init__(f'some (or all) of the following related task IDs are invalid: {task_ids}')
        self.invalid_bunch_of_related_task_ids = task_ids


class DomainValidationError(ApplicationError):
    ...
