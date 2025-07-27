from http import HTTPStatus

from fastapi import HTTPException


class InvalidAddress(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.BAD_REQUEST, message)