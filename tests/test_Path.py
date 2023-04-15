import os
import tempfile
import unittest

from on_rails import (ErrorDetail, ValidationError, assert_error_detail,
                      assert_result, assert_result_with_type)

from pylity.Path import Path, PathType


class TestPath(unittest.TestCase):
    # region basename

    def test_basename_give_none_or_empty(self):
        result = Path.basename(None)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input file path is not valid. It can not be None or empty.",
                            expected_code=400)

        result = Path.basename("")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input file path is not valid. It can not be None or empty.",
                            expected_code=400)

        result = Path.basename("     ")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input file path is not valid. It can not be None or empty.",
                            expected_code=400)

    def test_basename_give_valid_path(self):
        # create a temporary directory and a file in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file = os.path.join(tmp_dir_name, "file.py")
            with open(file, "w") as f:
                f.write("print('file1')")

            result = Path.basename(file)
            assert_result(self, result, expected_success=True, expected_value="file.py")

    # endregion

    # region get_path_type

    def test_get_path_type_give_invalid(self):
        result = Path.get_path_type(None)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title='One or more validation errors occurred',
                            expected_message='The input is not valid. Expected get a string but got <class \'NoneType\'>',
                            expected_code=400)

        result = Path.get_path_type("")
        assert_result(self, result, expected_success=True, expected_value=PathType.INVALID)

        result = Path.get_path_type("   ")
        assert_result(self, result, expected_success=True, expected_value=PathType.INVALID)

        result = Path.get_path_type("Invalid/path")
        assert_result(self, result, expected_success=True, expected_value=PathType.INVALID)

    def test_get_path_type_give_valid_path(self):
        # create a temporary directory and some files in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            dir1 = os.path.join(tmp_dir_name, "dir1")
            os.makedirs(dir1)
            file1 = os.path.join(tmp_dir_name, "file1.py")
            with open(file1, "w") as f:
                f.write("print('file1')")

            result = Path.get_path_type(tmp_dir_name)
            assert_result(self, result, expected_success=True, expected_value=PathType.DIRECTORY)

            result = Path.get_path_type(file1)
            assert_result(self, result, expected_success=True, expected_value=PathType.FILE)

            result = Path.get_path_type(dir1)
            assert_result(self, result, expected_success=True, expected_value=PathType.DIRECTORY)

    # endregion

    # region collect_files_from_dir

    def test_collect_files_from_dir_give_invalid_dir(self):
        result = Path.collect_files_from_dir(None)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title='One or more validation errors occurred',
                            expected_message="The input is not valid. Expected get a string but got <class 'NoneType'>", expected_code=400)

        result = Path.collect_files_from_dir("")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title='Directory is not valid.',
                            expected_message='The () is not valid.', expected_code=400)

        result = Path.collect_files_from_dir("Invalid directory")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title='Directory is not valid.',
                            expected_message='The (Invalid directory) is not valid.', expected_code=400)

    def test_collect_files_from_dir_give_file(self):
        # create a temporary directory and some files in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file = os.path.join(tmp_dir_name, "file.py")
            with open(file, "w") as f:
                f.write("print('file')")

            result = Path.collect_files_from_dir(file)
            assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
            assert_error_detail(self, result.detail, expected_title='Directory is not valid.',
                                expected_message=f'The ({file}) is not valid.', expected_code=400)

    def test_collect_files_from_dir_give_dir(self):
        # create a temporary directory and some files in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file1 = os.path.join(tmp_dir_name, "file1.py")
            with open(file1, "w") as f:
                f.write("print('file1')")
            file2 = os.path.join(tmp_dir_name, "file2.py")
            with open(file2, "w") as f:
                f.write("print('file2')")

            result = Path.collect_files_from_dir(tmp_dir_name)
            assert_result(self, result, expected_success=True,
                          expected_value=[f"{tmp_dir_name}/file1.py", f"{tmp_dir_name}/file2.py"])

    # endregion

    # region collect_files

    def test_collect_files_give_none_or_empty_list(self):
        result = Path.collect_files(None)
        assert_result(self, result, expected_success=True, expected_value=[])

        result = Path.collect_files([])
        assert_result(self, result, expected_success=True, expected_value=[])

    def test_collect_files_give_invalid_path(self):
        result = Path.collect_files(["Invalid path"])
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title='File or directory is not valid.',
                            expected_message='The (Invalid path) is not valid.', expected_code=400)

        result = Path.collect_files([None])
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title='One or more validation errors occurred',
                            expected_message='Input is not valid. It must be a list of strings.', expected_code=400)

        result = Path.collect_files("non list")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title='One or more validation errors occurred',
                            expected_message='Input is not valid. It must be a list of strings.', expected_code=400)

    def test_collect_files_ok(self):
        # create a temporary directory and some files in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            dir1 = os.path.join(tmp_dir_name, "dir1")
            os.makedirs(dir1)
            file1 = os.path.join(tmp_dir_name, "file1.py")
            with open(file1, "w") as f:
                f.write("print('file1')")
            file2 = os.path.join(tmp_dir_name, "file2.py")
            with open(file2, "w") as f:
                f.write("print('file2')")
            file3 = os.path.join(dir1, "file3.py")
            with open(file3, "w") as f:
                f.write("print('file3')")
            file4 = os.path.join(dir1, "file4.py")
            with open(file4, "w") as f:
                f.write("print('file4')")

            result = Path.collect_files([tmp_dir_name, dir1, file4])
            assert result.success
            assert set(result.value) == set([file1, file2, file3, file4])

    # endregion


if __name__ == '__main__':
    unittest.main()
