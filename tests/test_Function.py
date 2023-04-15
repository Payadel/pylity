import unittest

from on_rails import (ErrorDetail, ValidationError, assert_error_detail,
                      assert_result, assert_result_with_type)

from pylity.Function import Function


async def async_func():
    return "Hello, World!"


EXCEPTION_FAKE = Exception("fake")


async def raise_exception_async():
    raise EXCEPTION_FAKE


class TestFunction(unittest.TestCase):

    # region is_func_valid

    def test_is_func_valid_give_invalid_func(self):
        assert not Function.is_func_valid(None)
        assert not Function.is_func_valid("Not callable")
        assert not Function.is_func_valid(" ")

    def test_is_func_valid_give_valid_func(self):
        assert Function.is_func_valid(lambda: None)
        assert Function.is_func_valid(lambda x: x)
        assert Function.is_func_valid(print)
        assert Function.is_func_valid(sum)

    # endregion

    # region get_num_of_params

    def test_get_num_of_params_give_none(self):
        result = Function.get_num_of_params(None)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input function is not valid.",
                            expected_code=400)

        result = Function.get_num_of_params("is not callable")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input function is not valid.",
                            expected_code=400)

    def test_get_num_of_params(self):
        result = Function.get_num_of_params(lambda x: x)
        assert_result(self, target_result=result, expected_success=True, expected_value=1)

        result = Function.get_num_of_params(lambda x, y: x)
        assert_result(self, target_result=result, expected_success=True, expected_value=2)

    def test_get_num_of_params_builtin_functions(self):
        # Works for some builtin functions not all
        result = Function.get_num_of_params(sum)
        assert_result(self, target_result=result, expected_success=True, expected_value=2)

        result = Function.get_num_of_params(print)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="Parameter Number Detection Error",
                            expected_message=f"Can not determine the number of parameters of the "
                                             "print() function. You can use python function"
                                             "like lambda to fix this issue.", expected_code=400)

    # endregion

    # region is_async

    def test_is_async_give_invalid_func(self):
        result = Function.is_async(None)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input function is not valid.",
                            expected_code=400)

        result = Function.is_async("Not callable")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input function is not valid.",
                            expected_code=400)

    def test_is_async(self):
        assert_result(self, Function.is_async(lambda x: x), expected_success=True, expected_value=False)

        assert_result(self, Function.is_async(async_func), expected_success=True, expected_value=True)

    # endregion

    # region await_func

    def test_await_func_give_invalid_func(self):
        result = Function.await_func(None)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input function is not valid.",
                            expected_code=400)

        result = Function.await_func("Not callable")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input function is not valid.",
                            expected_code=400)

    def test_await_func_ok(self):
        result = Function.await_func(async_func)
        assert_result(self, result, expected_success=True, expected_value="Hello, World!")

        result = Function.await_func(lambda: 5)
        assert_result(self, result, expected_success=True, expected_value=5)

    def test_await_func_give_func_raise_exception(self):
        result = Function.await_func(raise_exception_async)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_error_detail(self, result.detail, expected_title="An error occurred",
                            expected_message='Operation failed with 1 attempts. The details of the 1 errors are '
                                             'stored in the more_data field. At least one of the errors was an '
                                             'exception type, the first exception being stored in the '
                                             'exception field.', expected_code=500,
                            expected_exception=EXCEPTION_FAKE, expected_more_data=[EXCEPTION_FAKE])

    # endregion


if __name__ == '__main__':
    unittest.main()
