"""DoHome protocol exceptions"""

import json

from dohome.types.common import DoDict

from .base import DoHomeException


class CommandCodeInvalid(DoHomeException):
    """Invalid command code exception"""

    def __init__(self, got: int, expected: int, expected_title: str):
        super().__init__(
            f"Invalid command code: {got}, expected: {expected} ({expected_title})"
        )


class CommandCodeNotFound(DoHomeException):
    """Command not found exception"""

    def __init__(self, res: DoDict, code: int, title: str):
        super().__init__(
            f"Command code not found: {title} ({code}) at response: {json.dumps(res)}"
        )


class ResponseCodeInvalid(DoHomeException):
    """Invalid response code exception"""

    def __init__(self, code: int, title: str):
        super().__init__(f"Invalid response code: {code} ({title})")


class ResponseCodeNotFound(DoHomeException):
    """Response code not found exception"""

    def __init__(self, res: DoDict):
        super().__init__(f"Response code not found at response: {json.dumps(res)}")
