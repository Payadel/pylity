import asyncio
import unittest

from on_rails import assert_result

from pylity.Async import Async


class TestAsync(unittest.TestCase):
    def test_get_loop(self):
        """
        This test case creates two event loops using the get_loop function and checks that they are both instances of
        the AbstractEventLoop class and that they are the same object. This tests that the function correctly returns
        the current event loop if one exists, or creates a new event loop if one doesn't exist, and sets it as the
        current event loop for the thread.
        """

        loop1_result = Async.get_loop()
        assert_result(self, loop1_result, expected_success=True, expected_value=loop1_result.value)

        loop2_result = Async.get_loop()
        assert_result(self, loop2_result, expected_success=True, expected_value=loop1_result.value)

        assert isinstance(loop1_result.value, asyncio.AbstractEventLoop)
        assert isinstance(loop2_result.value, asyncio.AbstractEventLoop)


if __name__ == '__main__':
    unittest.main()
