class String:
    """ A collection of utility functions for string  """

    @staticmethod
    def is_none_or_empty(string: str) -> bool:
        """
        The function checks if a given string is None or empty (contains only whitespace characters)

        :param string: A string variable that we want to check if it is None or empty
        :type string: str

        :return: Returns a boolean value.
        """
        return string is None or string.strip() == ''
