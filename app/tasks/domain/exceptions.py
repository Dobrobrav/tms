class ApplicationError(Exception):
    ...


class TitleEmptyError(ApplicationError):
    ...


class InvalidReporterID(ApplicationError):
    ...


class InvalidAssigneeID(ApplicationError):
    ...


class InvalidCommentIDs(ApplicationError):
    ...


class InvalidRelatedTaskIDs(ApplicationError):
    ...
