import inspect
from typing import Any, Callable, Dict, Optional

from on_rails import Result, ValidationError, def_result, try_func
from schema import Schema, SchemaError


def validate_func_params(schema: Optional[Schema] = None):
    """
    A Python decorator function that validates function parameters based on a given schema.

    :param schema: The `schema` parameter is an optional argument of type `Schema`. It is used to specify the expected
    schema for the function parameters. If provided, the function parameters will be validated against this schema.
    If not provided, no validation will be performed
    :type schema: Optional[Schema]
    """
    def decorator(func: Callable):
        @def_result()
        def wrapper(*args, **kwargs) -> Result:
            return _get_args(func, *args, **kwargs) \
                .on_success(lambda arg_dict: _validate_args(schema, arg_dict, func)) \
                .on_success(lambda: func(*args, **kwargs))

        return wrapper

    return decorator


def _is_exception_type(result: Result, exception_type):
    return result and result.detail and result.detail.exception and isinstance(result.detail.exception, exception_type)


@def_result()
def _get_args(func: Callable, *args, **kwargs) -> Result[Dict[str, Any]]:
    # Get the function signature
    sig = inspect.signature(func)

    # Create a dictionary of argument names and values
    bound_args = try_func(lambda: sig.bind(*args, **kwargs)) \
        .on_fail_operate_when(
        lambda res: _is_exception_type(res, TypeError),
        lambda res: Result.fail(ValidationError(message=str(res.detail.exception)))) \
        .on_fail_break_function() \
        .value

    arg_dict = {}
    for name, value in bound_args.arguments.items():
        arg_dict[name] = value

    # Add any additional keyword arguments to the argument dictionary
    arg_dict.update(kwargs)

    for param in sig.parameters.values():
        # If parameter is not in arg_dict and has default value, add it to the arg_dict
        if param.name not in arg_dict and param.default is not inspect.Parameter.empty:
            arg_dict[param.name] = param.default

    return Result.ok(value=arg_dict)


def _validate_args(schema: Optional[Schema], arg_dict: Dict[str, Any], func: Callable) -> Result:
    # Validate the arguments using the schema
    func_schema = schema if schema is not None else Schema(
        {key: value for key, value in arg_dict.items() if key in func.__annotations__})

    return try_func(lambda: func_schema.validate(arg_dict)) \
        .on_fail_operate_when(
        lambda res: _is_exception_type(res, SchemaError),
        lambda res: Result.fail(ValidationError(message=str(res.detail.exception))))
