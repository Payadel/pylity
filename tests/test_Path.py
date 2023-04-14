import os
import tempfile
import unittest

from on_rails import (ErrorDetail, ValidationError, assert_error_detail,
                      assert_result, assert_result_with_type)

from pylity.Path import Path, PathType


class TestPath(unittest.TestCase):
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

    def test_get_path_type_give_none_or_empty(self):
        result = Path.get_path_type(None)
        assert_result(self, result, expected_success=True, expected_value=PathType.INVALID)

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


if __name__ == '__main__':
    unittest.main()
