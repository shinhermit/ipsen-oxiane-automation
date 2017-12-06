"""
The classes in this module represent the data model of Google Analytics API.

They are basically wrapper over dicts parsed from JSON returned by the API. These models
allow a better understanding of the data used in the scripts.

API reference page: https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/
"""
from typing import TypeVar, List, Dict


T = TypeVar("T")
"""Used to type hint the GenericWrappingIterator class' methods"""


class GenericWrappingIterator:
    """
    Iterate over wrapped dict items from a list in an API response.

    This iterator allows to iterate over wrapped representation of entities contained
    in the API response.
    """
    def __init__(self, items: List[Dict], wrapper_class):
        """
        :param items: the (dict) items over which we want to iterate
        :param wrapper_class: each item returned while iterating using this iterator will
        be wrapped using the class provided by wrapper_class
        """
        self._wrapper_class = wrapper_class
        self._items = items
        self._items_iterator = iter(items)

    def __iter__(self) -> 'GenericWrappingIterator':
        """Used in for..in loops to get the iterator."""
        return self

    def __next__(self) -> T:
        """Used in for..in loops to get the next item."""
        return self._wrapper_class(next(self._items_iterator))

    def __getitem__(self, key: int) -> T:
        """[] operator"""
        return self._wrapper_class(self._items[key])

    def __len__(self) -> int:
        """Used by the builtin len() function."""
        return len(self._items)
