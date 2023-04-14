import os
from enum import Enum

from on_rails import Result, ValidationError, def_result

from pylity.String import String


class PathType(Enum):
    """
    Defines an enumeration of three path types: file, directory, and invalid.
    """
    FILE = 1
    DIRECTORY = 2
    INVALID = 3


class Path:
    """ A collection of utility functions for paths  """

    @staticmethod
    @def_result()
    def basename(path: str) -> Result[str]:
        """
        Takes a path as input and returns the name as a Result object, with an error message if the
        input is invalid.

        :param path: A string representing the path of file, directory, etc.
        :type path: str

        :return: Returns a `Result` object that contains either a string
        representing the name or a `ValidationError` object if the input path is not valid.
        """

        if String.is_none_or_empty(path):
            return Result.fail(ValidationError(
                message="The input file path is not valid. It can not be None or empty."))
        return Result.ok(os.path.basename(path))

    @staticmethod
    @def_result()
    def get_path_type(path: str) -> Result[PathType]:
        """
        The function checks the type of given path and returns a result indicating whether it is a
        file, directory, or invalid.

        :param path: A string representing a file path or directory path
        :type path: str

        :return: a `Result` object that contains a `PathType` value.
        """

        if String.is_none_or_empty(path):
            return Result.ok(value=PathType.INVALID)

        if os.path.isfile(path):
            return Result.ok(value=PathType.FILE)
        if os.path.isdir(path):
            return Result.ok(value=PathType.DIRECTORY)
        return Result.ok(value=PathType.INVALID)
