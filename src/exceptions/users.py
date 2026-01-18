from dataclasses import dataclass
from http import HTTPStatus

from src.exceptions.base import ApplicationError


@dataclass
class UserNotFoundError(ApplicationError):
    user_id: str

    @property
    def message(self) -> str:
        return f"User with id: {self.user_id} not found!"

    @property
    def status_code(self) -> int:
        return HTTPStatus.NOT_FOUND
