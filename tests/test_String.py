import unittest

from pylity.String import String


class TestString(unittest.TestCase):
    def test_is_none_or_empty_give_invalid(self):
        assert String.is_none_or_empty(None)
        assert String.is_none_or_empty("")
        assert String.is_none_or_empty("   ")
        assert String.is_none_or_empty("\t")
        assert String.is_none_or_empty(" \t ")

    def test_is_none_or_empty_give_valid(self):
        assert not String.is_none_or_empty("None")
        assert not String.is_none_or_empty("    not empty   ")


if __name__ == '__main__':
    unittest.main()
