"""
Module flysystem
"""

from typing import final

from typing_extensions import Self


class FileValidatorException(Exception):
    """
    Base exception class for FileValidatorException package
    """


class UnableToOperateToFile(FileValidatorException):
    """
    Unable to check to file exception
    """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self._location = ""
        self._reason = ""

    @final
    def location(self) -> str:
        return self._location

    @final
    def reason(self) -> str:
        return self._reason


@final
class UnableToCloseFile(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to close file from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._location = location
        this._reason = reason
        return this


@final
class UnableToReadFile(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to read file from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._location = location
        this._reason = reason
        return this


@final
class UnableToWriteFile(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to write file from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._location = location
        this._reason = reason
        return this


@final
class UnableToUpdateFile(UnableToOperateToFile):
    @classmethod
    def with_location(cls, location: str, reason: str = "") -> Self:
        msg = f"Unable to update file from location: {location}. {reason}".rstrip()
        this = cls(msg)
        this._location = location
        this._reason = reason
        return this
