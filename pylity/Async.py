import asyncio
from asyncio import AbstractEventLoop

from on_rails import Result, def_result


class Async:
    """ A collection of utility functions for asynchronously  """

    @staticmethod
    @def_result()
    def get_loop() -> Result[AbstractEventLoop]:
        """
        The function returns the current event loop or creates a new one if none exists.

        :return: Returns a `Result` object that contains either an `AbstractEventLoop` instance or
        an error message.
        """
        try:
            return Result.ok(value=asyncio.get_event_loop())
        except RuntimeError as e:  # pragma: no cover
            if str(e).startswith('There is no current event loop in thread'):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return Result.ok(value=loop)
            raise  # pragma: no cover
