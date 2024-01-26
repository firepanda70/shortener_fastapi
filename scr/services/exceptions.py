from fastapi import status

from scr.core.exceptions import ValidationException

SHORTCUT_NOT_FOUND_MSG = 'Shortcut {0} not found'
SHORTCUT_DISABLED_MSG = 'Shortcut {0} currently disabled'
SHORTCUT_TAKEN = 'Shortcut {0} already in use'


class ShortcutNotFound(ValidationException):
    def __init__(
        self, reason: str, status_code: int = status.HTTP_404_NOT_FOUND
    ) -> None:
        super().__init__(SHORTCUT_NOT_FOUND_MSG.format(reason), status_code)


class ShortcutDisabled(ValidationException):
    def __init__(
        self, reason: str, status_code: int = status.HTTP_423_LOCKED
    ) -> None:
        super().__init__(SHORTCUT_DISABLED_MSG.format(reason), status_code)


class ShortcutTaken(ValidationException):
    def __init__(
        self, reason: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> None:
        super().__init__(SHORTCUT_TAKEN.format(reason), status_code)
