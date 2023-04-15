import asyncio
import inspect
from typing import Callable, Coroutine

from on_rails import Result, ValidationError, def_result

from pylity.Async import Async


class Function:
    """ A collection of utility functions for functions  """

    @staticmethod
    def is_func_valid(func) -> bool:
        """
        Checks if a given input is a valid callable function or not.

        :param func: The parameter `func` is expected to be a function object. This function checks if the `func`
        parameter is not `None` and is callable (i.e., it can be called as a function).
        If both conditions are true, it returns `True`

        :return: Returns a boolean value. It returns `True` if the input `func` is not `None` and
        is callable (i.e. can be called as a function), and `False` otherwise.
        """
        return func is not None and callable(func)

    @staticmethod
    @def_result()
    def get_num_of_params(func: Callable) -> Result[int]:
        """
        The function takes a callable object and returns the number of parameters it accepts.
        The number of parameters of some builtin functions cannot be recognized and
        returns ErrorDetail for these functions.

        :param func: The input function for which we want to determine the number of parameters.
        It is expected to be a callable object
        :type func: Callable

        :return: Returns a `Result` object that contains either the number of parameters of the input function
        as an integer if the function is valid, or a `ValidationError` message if the input function is not valid.
        """

        if not Function.is_func_valid(func):
            return Result.fail(ValidationError(message="The input function is not valid."))

        try:
            return Result.ok(len(inspect.signature(func).parameters))
        except ValueError:
            try:
                return Result.ok(func.__code__.co_argcount)
            except Exception:
                return Result.fail(ValidationError(title="Parameter Number Detection Error",
                                                   message=f"Can not determine the number of parameters of the "
                                                           f"{func.__name__}() function. You can use python function"
                                                           f"like lambda to fix this issue."))

    @staticmethod
    @def_result()
    def is_async(func: Callable) -> Result[bool]:
        """
        The function checks if a given function is asynchronous or not.

        :param func: The parameter `func` is a function that is being checked for whether it is an asynchronous
        function or not. The function is expected to be a valid Python function that can be called.
        :type func: Callable

        :return: Returns a boolean value indicating whether the input function is an asynchronous coroutine
        function or not. If the input function is not valid, it returns a `Result` object with a validation error.
        message.
        """

        if not Function.is_func_valid(func):
            return Result.fail(ValidationError(message="The input function is not valid."))

        return Result.ok(value=asyncio.iscoroutinefunction(func))

    @staticmethod
    @def_result()
    def await_func(func: callable) -> Result:
        """
        The function takes in a callable function, checks if it's valid, and runs it either synchronously and
        returns result as Result object.

        :param func: The parameter `func` is a callable object, which means it can be a function, method, or any other
        object that can be called like a function
        :type func: callable

        :return: Returns an instance of the `Result` class. If the input function is not valid, it returns
        a failed `Result` object with a `ValidationError` message. If the input function returns a coroutine, it
        uses the `run_until_complete` method of the event loop to wait for the coroutine to complete and returns
        the result as a `Result` object.
        """

        if not Function.is_func_valid(func):
            return Result.fail(ValidationError(message="The input function is not valid."))

        result = func()
        if isinstance(result, Coroutine):
            return Async.get_loop() \
                .on_success(lambda loop: loop.run_until_complete(result)) \
                .on_fail_break_function()

        return Result.convert_to_result(result)
