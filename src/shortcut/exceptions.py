from fastapi import status, HTTPException

SHORTCUT_NOT_FOUND_MSG = 'Shortcut not found'
SHORTCUT_DISABLED_MSG = 'Shortcut disabled'
SHORTCUT_TAKEN = 'Shortcut already taken'


class ShortcutNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, SHORTCUT_NOT_FOUND_MSG)


class ShortcutDisabled(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, SHORTCUT_DISABLED_MSG)


class ShortcutTaken(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, SHORTCUT_DISABLED_MSG)
