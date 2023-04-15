import unittest

from pylity.Collection import Collection


class TestCollection(unittest.TestCase):
    def test_is_list_give_non_list(self):
        assert not Collection.is_list(None)
        assert not Collection.is_list(" ")
        assert not Collection.is_list(set())

    def test_is_list_give_list_invalid_items(self):
        assert not Collection.is_list([None], str)
        assert not Collection.is_list(['', None, ' '], str)

    def test_is_list_give_list_valid_items(self):
        assert Collection.is_list(['None'], str)
        assert Collection.is_list(['', 'None', ' '], str)


if __name__ == '__main__':
    unittest.main()
