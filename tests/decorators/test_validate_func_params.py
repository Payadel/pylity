import unittest
from typing import Any, Dict, List, Optional

from on_rails import (ErrorDetail, Result, ValidationError,
                      assert_error_detail, assert_result,
                      assert_result_with_type, try_func)
from schema import And, Or, Schema, Use

from pylity.decorators.validate_func_params import validate_func_params

SCHEMA = Schema({
    'p1': And(Use(int), lambda n: n > 0, error='The p1 must be greater than zero'),
    'p2': And(str, str.strip, lambda s: len(s) > 0, error='The p2 must be string and can not be empty or whitespace.'),
    'p3': And(list, lambda lst: len(lst) > 0, [str], error='The p3 must be list of strings and can not be empty.'),
    'p4': Or(str, None, error='The p4 must be string or None.'),
    'p5': And(str, str.strip, lambda s: len(s) > 0, error='The p5 must be string and can not be empty or whitespace.')
})


def fake_func(p1: int, p2: str, p3: List[str], p4: Optional[str], p5: Optional[str] = "default"):
    return {'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4, 'p5': p5}


class ClassWithDefaultSchema:
    _private_variable: str

    @validate_func_params(raise_exception=True)
    def __init__(self, p1: int, p2: str, p3: List[str], p4: Optional[str], p5: Optional[str] = "default"):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self._private_variable = "fake"


class ClassWithCustomSchema:
    _private_variable: str

    @validate_func_params(raise_exception=True, schema=SCHEMA)
    def __init__(self, p1: int, p2: str, p3: List[str], p4: Optional[str], p5: Optional[str] = "default"):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self._private_variable = "fake"


class TestValidateFuncParameters(unittest.TestCase):
    def test_ok_raise_false(self):
        # default schema
        result = validate_func_params(raise_exception=False)(fake_func)(1, '1', ['a', 'b'], None, 'p5')
        assert_result(self, result, expected_success=True,
                      expected_value={'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'p5'})

        # custom schema
        result = validate_func_params(raise_exception=False, schema=SCHEMA)(fake_func)(1, '1',
                                                                                       ['a', 'b'], None,
                                                                                       'p5')
        assert_result(self, result, expected_success=True,
                      expected_value={'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'p5'})

    def test_ok_raise_true(self):
        # default schema
        result = validate_func_params(raise_exception=True)(fake_func)(1, '1', ['a', 'b'], None, 'p5')
        assert result == {'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'p5'}

        # custom schema
        result = validate_func_params(raise_exception=True, schema=SCHEMA)(fake_func)(1, '1', ['a', 'b'],
                                                                                      None, 'p5')
        assert result == {'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'p5'}

    def test_default_value_raise_false(self):
        # default schema
        result = validate_func_params(raise_exception=False)(fake_func)(1, '1', ['a', 'b'], None)
        assert_result(self, result, expected_success=True,
                      expected_value={'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'default'})

        # custom schema
        result = validate_func_params(raise_exception=False, schema=SCHEMA)(fake_func)(1, '1',
                                                                                       ['a', 'b'], None)
        assert_result(self, result, expected_success=True,
                      expected_value={'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'default'})

    def test_default_value_raise_true(self):
        # default schema
        result = validate_func_params(raise_exception=True)(fake_func)(1, '1', ['a', 'b'], None)
        assert result == {'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'default'}

        # custom schema
        result = validate_func_params(raise_exception=True, schema=SCHEMA)(fake_func)(1, '1', ['a', 'b'],
                                                                                      None)
        assert result == {'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'default'}

    def test_missing_required_params_raise_false(self):
        # default schema
        result = validate_func_params(raise_exception=False)(fake_func)(1, '1', ['a', 'b'])
        self.assert_validation_error(result, "missing a required argument: 'p4'")

        result = validate_func_params(raise_exception=False)(fake_func)(1, '1', p4='p4')
        self.assert_validation_error(result, "missing a required argument: 'p3'")

        # custom schema
        result = validate_func_params(raise_exception=False, schema=SCHEMA)(fake_func)(1, '1',
                                                                                       ['a', 'b'])
        self.assert_validation_error(result, "missing a required argument: 'p4'")

        result = validate_func_params(raise_exception=False, schema=SCHEMA)(fake_func)(1, '1', p4='p4')
        self.assert_validation_error(result, "missing a required argument: 'p3'")

    def test_missing_required_params_raise_true(self):
        # default schema
        result = try_func(
            lambda: validate_func_params(raise_exception=True)(fake_func)(1, '1', ['a', 'b']))
        self.assert_result_exception(result, "missing a required argument: 'p4'")

        result = try_func(lambda: validate_func_params(raise_exception=True)(fake_func)(1, '1', p4='p4'))
        self.assert_result_exception(result, "missing a required argument: 'p3'")

        # custom schema
        result = try_func(
            lambda: validate_func_params(raise_exception=True, schema=SCHEMA)(fake_func)(1, '1', ['a', 'b']))
        self.assert_result_exception(result, "missing a required argument: 'p4'")

        result = try_func(lambda: validate_func_params(raise_exception=True, schema=SCHEMA)(fake_func)(1, '1', p4='p4'))
        self.assert_result_exception(result, "missing a required argument: 'p3'")

    def test_invalid_inputs_raise_false(self):
        # default schema
        result = validate_func_params(raise_exception=False)(fake_func)(1, 2, ['a', 3, 'c'], '')
        assert_result(self, result, expected_success=True,
                      expected_value={'p1': 1, 'p2': 2, 'p3': ['a', 3, 'c'], 'p4': '', 'p5': 'default'})

        # custom schema
        result = validate_func_params(raise_exception=False, schema=SCHEMA)(fake_func)(0, '2', ['a', '3', 'c'], '')
        self.assert_validation_error(result, "The p1 must be greater than zero")

        result = validate_func_params(raise_exception=False, schema=SCHEMA)(fake_func)(1, 2, ['a', '3', 'c'], '')
        self.assert_validation_error(result, "The p2 must be string and can not be empty or whitespace.")

        result = validate_func_params(raise_exception=False, schema=SCHEMA)(fake_func)(1, '2', ['a', '3', 'c'], '', '')
        self.assert_validation_error(result, "The p5 must be string and can not be empty or whitespace.")

    def test_invalid_inputs_raise_true(self):
        # default schema
        result = validate_func_params(raise_exception=True)(fake_func)(1, 2, ['a', 3, 'c'], '')
        assert result == {'p1': 1, 'p2': 2, 'p3': ['a', 3, 'c'], 'p4': '', 'p5': 'default'}

        # custom schema
        result = try_func(
            lambda: validate_func_params(raise_exception=True, schema=SCHEMA)(fake_func)(0, '2', ['a', '3', 'c'], ''))
        self.assert_result_exception(result, "The p1 must be greater than zero")

        result = try_func(
            lambda: validate_func_params(raise_exception=True, schema=SCHEMA)(fake_func)(1, 2, ['a', '3', 'c'], ''))
        self.assert_result_exception(result, "The p2 must be string and can not be empty or whitespace.")

        result = try_func(
            lambda: validate_func_params(raise_exception=True, schema=SCHEMA)(fake_func)(1, '2', ['a', '3', 'c'], '',
                                                                                         ''))
        self.assert_result_exception(result, "The p5 must be string and can not be empty or whitespace.")

    def test_on_init_ok(self):
        # default schema
        obj = ClassWithDefaultSchema(1, '1', ['a', 'b'], None, 'p5')
        self.assert_class_object(obj, ClassWithDefaultSchema,
                                 {'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'p5'})

        # custom schema
        obj = ClassWithCustomSchema(1, '1', ['a', 'b'], None, 'p5')
        self.assert_class_object(obj, ClassWithCustomSchema,
                                 {'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'p5'})

    def test_on_init_default_value(self):
        # default schema
        obj = ClassWithDefaultSchema(1, '1', ['a', 'b'], None)
        self.assert_class_object(obj, ClassWithDefaultSchema,
                                 {'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'default'})

        # custom schema
        obj = ClassWithCustomSchema(1, '1', ['a', 'b'],None)
        self.assert_class_object(obj, ClassWithCustomSchema,
                                 {'p1': 1, 'p2': '1', 'p3': ['a', 'b'], 'p4': None, 'p5': 'default'})

    def test_on_init_missing_required_params(self):
        # default schema
        result = try_func(lambda: ClassWithDefaultSchema(1, '1', ['a', 'b']))
        self.assert_result_exception(result, "missing a required argument: 'p4'")

        result = try_func(lambda: ClassWithDefaultSchema(1, '1', p4='p4'))
        self.assert_result_exception(result, "missing a required argument: 'p3'")

        # custom schema
        result = try_func(lambda: ClassWithCustomSchema(1, '1', ['a', 'b']))
        self.assert_result_exception(result, "missing a required argument: 'p4'")

        result = try_func(lambda: ClassWithCustomSchema(1, '1', p4='p4'))
        self.assert_result_exception(result, "missing a required argument: 'p3'")

    def test_on_init_invalid_inputs(self):
        # default schema
        obj = ClassWithDefaultSchema(1, 2, ['a', 3, 'c'], '')
        self.assert_class_object(obj, ClassWithDefaultSchema,
                                 {'p1': 1, 'p2': 2, 'p3': ['a', 3, 'c'], 'p4': '', 'p5': 'default'})

        # custom schema
        result = try_func(lambda: ClassWithCustomSchema(0, '2', ['a', '3', 'c'], ''))
        self.assert_result_exception(result, "The p1 must be greater than zero")

        result = try_func(lambda: ClassWithCustomSchema(1, 2, ['a', '3', 'c'], ''))
        self.assert_result_exception(result, "The p2 must be string and can not be empty or whitespace.")

        result = try_func(lambda: ClassWithCustomSchema(1, '2', ['a', '3', 'c'], '',''))
        self.assert_result_exception(result, "The p5 must be string and can not be empty or whitespace.")

    # region Helpers

    def assert_validation_error(self, target_result: Result, expected_message: str):
        assert_result_with_type(self, target_result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, target_result.detail, expected_title="One or more validation errors occurred",
                            expected_message=expected_message,
                            expected_code=400)

    def assert_result_exception(self, target_result: Result, expected_message: str):
        assert_result_with_type(self, target_result, expected_success=False, expected_detail_type=ErrorDetail)
        self.assertIsNotNone(target_result.detail.exception)
        self.assertIsInstance(target_result.detail.exception, ValueError)
        self.assertEqual(expected_message, str(target_result.detail.exception))

    def assert_class_object(self, target_obj, expected_class_type, expected_field: Dict[str, Any]):
        self.assertIsInstance(target_obj, expected_class_type)

        class_fields = {key: value for key, value in vars(target_obj).items() if not key.startswith('_')}
        self.assertEqual(expected_field, class_fields)

    # endregion


if __name__ == '__main__':
    unittest.main()
