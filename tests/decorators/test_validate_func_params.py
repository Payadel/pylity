import unittest
from typing import List, Optional

from on_rails import (ValidationError, assert_error_detail, assert_result,
                      assert_result_with_type)
from schema import And, Or, Schema, Use

from pylity.decorators.validate_func_params import validate_func_params


@validate_func_params()
def func_with_default_schema(p1: int, p2: str, p3: List[str], p4: Optional[str], p5: Optional[str] = "default"):
    return {'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4, 'p5': p5}


@validate_func_params(Schema({
    'p1': And(Use(int), lambda n: n > 0, error='The p1 must be greater than zero'),
    'p2': And(str, str.strip, lambda s: len(s) > 0, error='The p2 must be string and can not be empty or whitespace.'),
    'p3': And(list, lambda lst: len(lst) > 0, [str], error='The p3 must be list of strings and can not be empty.'),
    'p4': Or(str, None, error='The p4 must be string or None.'),
    'p5': And(str, str.strip, lambda s: len(s) > 0, error='The p5 must be string and can not be empty or whitespace.')
}))
def func_with_custom_schema(p1: int, p2: str, p3: List[str], p4: Optional[str], p5: Optional[str] = "default"):
    return {'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4, 'p5': p5}


class TestValidateFuncParameters(unittest.TestCase):
    def test_ok(self):
        result = func_with_default_schema(1, '1', ['a', 'b'], None, 'p5')
        assert_result(self, result, expected_success=True,
                      expected_value={'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'p5'})

        result = func_with_custom_schema(1, '1', ['a', 'b'], None, 'p5')
        assert_result(self, result, expected_success=True,
                      expected_value={'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'p5'})

    def test_default_value(self):
        result = func_with_default_schema(1, '1', ['a', 'b'], None)
        assert_result(self, result, expected_success=True,
                      expected_value={'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'default'})

        result = func_with_custom_schema(1, '1', ['a', 'b'], None)
        assert_result(self, result, expected_success=True,
                      expected_value={'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'default'})

    def test_missing_required_params(self):
        # func_with_default_schema
        result = func_with_default_schema(1, '1', ['a', 'b'])
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="missing a required argument: 'p4'", expected_code=400)

        result = func_with_default_schema(1, '1', p4='p4')
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="missing a required argument: 'p3'", expected_code=400)

        # func_with_custom_schema
        result = func_with_custom_schema(1, '1', ['a', 'b'])
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="missing a required argument: 'p4'", expected_code=400)

        result = func_with_custom_schema(1, '1', p4='p4')
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="missing a required argument: 'p3'", expected_code=400)

    def test_invalid_inputs(self):
        # func_with_default_schema not validate params
        result = func_with_default_schema(1, 2, ['a', 3, 'c'], '')
        assert_result(self, result, expected_success=True,
                      expected_value={'p1': 1, 'p2': 2, 'p3': ['a', 3, 'c'], 'p4': '', 'p5': 'default'})

        # func_with_custom_schema
        result = func_with_custom_schema(0, '2', ['a', '3', 'c'], '')
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The p1 must be greater than zero",
                            expected_code=400)

        result = func_with_custom_schema(1, 2, ['a', '3', 'c'], '')
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The p2 must be string and can not be empty or whitespace.",
                            expected_code=400)

        result = func_with_custom_schema(1, '2', ['a', '3', 'c'], '', '')
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The p5 must be string and can not be empty or whitespace.",
                            expected_code=400)


if __name__ == '__main__':
    unittest.main()
