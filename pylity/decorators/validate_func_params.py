import inspect
from typing import Any, Callable, Dict, Optional

from on_rails import Result, ValidationError, def_result, try_func
from schema import Schema, SchemaError


def validate_func_params(schema: Optional[Schema] = None, raise_exception: bool = False):
    """
    Decorator function that validates function parameters based on a given schema and can optionally raise
    exceptions or manage exceptions with on_rails package.

    :param schema: An optional parameter of type Schema that specifies the schema to be used for validating the function
    parameters. If not provided, no validation will be performed
    :type schema: Optional[Schema]

    :param raise_exception: A boolean parameter that determines whether or not to raise an exception if the validation
    fails. If set to True, an exception will be raised. If set to False, the validation result will be returned as
    Result object, defaults to False
    :type raise_exception: bool (optional)

    :return: By default, when raise_exception is false, returns result as Result object, Otherwise returns output
    of function or raise exception.
    """

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            # Validation
            validation_result = _get_args(func, *args, **kwargs) \
                .on_success(lambda arg_dict: _validate_args(schema, arg_dict, func))

            if validation_result.success:
                if raise_exception:
                    # Execute the function without catch exceptions
                    return func(*args, **kwargs)
                # Execute the function with catch exceptions
                return try_func(lambda: func(*args, **kwargs))

            if not raise_exception:
                return validation_result

            if validation_result.detail and validation_result.detail.is_instance_of(ValidationError):
                raise ValueError(validation_result.detail.message)

            validation_result.on_fail_raise_exception()  # pragma: no cover
            raise Exception("Somethings is not correct. This code should not be executed!")  # pragma: no cover

        return wrapper

    return decorator


def _has_exception(result: Result):
    return result and result.detail and result.detail.exception


def _is_exception_type(result: Result, exception_type):
    return _has_exception(result) and isinstance(result.detail.exception, exception_type)


@def_result()
def _get_args(func: Callable, *args, **kwargs) -> Result[Dict[str, Any]]:
    """
    This function takes a function and its arguments and returns a dictionary of argument names and values, including any
    default values.

    :param func: The function for which we want to get the arguments and their values.
    :type func: Callable
    """

    # Get the function signature
    sig = inspect.signature(func)

    # Create a dictionary of argument names and values
    bound_args = try_func(lambda: sig.bind(*args, **kwargs)) \
        .on_fail_operate_when(lambda res: _is_exception_type(res, TypeError),
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


@def_result()
def _validate_args(schema: Optional[Schema], arg_dict: Dict[str, Any], func: Callable) -> Result:
    """
    This function validates arguments using a schema and returns a result, handling any validation errors.

    :param schema: An optional parameter of type Schema, which is used to validate the arguments passed to the function
    :type schema: Optional[Schema]

    :param arg_dict: arg_dict is a dictionary containing the arguments passed to a function. The keys of the dictionary are
    the argument names and the values are the argument values
    :type arg_dict: Dict[str, Any]

    :param func: Represents the function that needs to be validated. The function's annotations are
    used to determine the expected types of the arguments
    :type func: Callable
    """

    func_schema = schema if schema is not None else Schema(
        {key: value for key, value in arg_dict.items() if key in func.__annotations__})
    if 'self' in arg_dict and 'self' not in func_schema.schema:
        arg_dict.pop('self', None)

    return try_func(lambda: func_schema.validate(arg_dict)) \
        .on_fail_operate_when(lambda res: _is_exception_type(res, SchemaError),
                              lambda res: Result.fail(ValidationError(message=str(res.detail.exception))))
