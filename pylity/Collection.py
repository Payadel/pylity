from typing import Optional, Type


class Collection:
    """
    A collection of utility functions for Collections like list, set, dict, etc.
    """

    @staticmethod
    def is_list(target, item_types: Optional[Type] = None) -> bool:
        """
        This function checks if a given target is a list and optionally checks if all its items are of a specified type.

        :param target: The variable or object that is being checked to see if it is a list

        :param item_types: The parameter `item_types` is an optional argument that specifies the type of
        items that should be present in the list. If `item_types` is provided, the function checks if all
        the items in the list are of the specified type. If `item_types` is not provided, the function only
        checks if target is list or not.
        :type item_types: Optional[Type]
        """

        if item_types:
            return isinstance(target, list) and all(isinstance(item, str) for item in target)
        return isinstance(target, list)
