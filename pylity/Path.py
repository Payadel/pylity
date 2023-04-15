import os
from enum import Enum
from typing import List

from on_rails import Result, ValidationError, def_result

from pylity.Collection import Collection
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
        if not isinstance(path, str):
            return Result.fail(ValidationError(
                message=f"The input is not valid. Expected get a string but got {type(path)}"))

        if String.is_none_or_empty(path):
            return Result.ok(value=PathType.INVALID)

        if os.path.isfile(path):
            return Result.ok(value=PathType.FILE)
        if os.path.isdir(path):
            return Result.ok(value=PathType.DIRECTORY)
        return Result.ok(value=PathType.INVALID)

    @staticmethod
    @def_result()
    def collect_files(files_and_directories: List[str]) -> Result[List[str]]:
        """
        The function collects all files from a list of directories and files and returns a list of the file paths.

        :param files_and_directories: A list of strings representing file paths and/or directory paths
        :type files_and_directories: List[str]

        :return: The function `collect_files` returns a `Result` object that contains a list of strings representing the
        collected files and directories.
        """

        files_and_directories = files_and_directories or []
        if not Collection.is_list(files_and_directories, str):
            return Result.fail(ValidationError(message="Input is not valid. It must be a list of strings."))

        files = set()

        for file_or_dir in files_and_directories:
            result = Path.get_path_type(file_or_dir) \
                .on_fail_break_function() \
                .on_success_fail_when(lambda path: path is PathType.INVALID,
                                      ValidationError(title="File or directory is not valid.",
                                                      message=f"The ({file_or_dir}) is not valid.")) \
                .on_fail_break_function()
            if result.value is PathType.FILE:
                files.add(file_or_dir)
            else:
                Path.collect_files_from_dir(file_or_dir).on_fail_break_function() \
                    .on_success(lambda dir_files: files.update(dir_files)).on_fail_break_function()
        return Result.ok(value=list(files))

    @staticmethod
    @def_result()
    def collect_files_from_dir(directory: str) -> Result[List[str]]:
        """
        This function collects all files from a given directory and returns them as a list.

        :param directory: The directory parameter is a string that represents the path to a directory from
        which we want to collect files
        :type directory: str
        """

        return Path.get_path_type(directory) \
            .on_success_fail_when(lambda path: path is not PathType.DIRECTORY,
                                  ValidationError(title="Directory is not valid.",
                                                  message=f"The ({directory}) is not valid.")) \
            .on_success(lambda: Path.__collect_files_from_dir(directory))

    @staticmethod
    @def_result()
    def __collect_files_from_dir(directory: str) -> Result[List[str]]:
        files = []
        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)
            if os.path.isfile(full_path):
                files.append(full_path)
        return Result.ok(files)
