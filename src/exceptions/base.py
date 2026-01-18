from dataclasses import dataclass
from http import HTTPStatus


@dataclass
class ApplicationError(Exception):
    @property
    def message(self, ) -> str:
        return "Internal error"

    @property
    def status_code(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR
