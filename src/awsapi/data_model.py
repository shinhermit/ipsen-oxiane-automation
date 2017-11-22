
class HostedZone:

    def __init__(self, response_data):
        self.data = response_data
        self._items_iterator = GenericWrappingIterator(self.data.get("ResourceRecordSets", []), ResourceRecordSets)

    @property
    def is_truncated(self):
        return self.data.get("IsTruncated")

    @property
    def max_items(self):
        return self.data.get("MaxItems")

    @property
    def resource_record_sets(self):
        return self._items_iterator


class ResourceRecordSets:
    def __init__(self, json_as_dict):
        self.data = json_as_dict
        self._items_iterator = GenericWrappingIterator((self.data.get('ResourceRecords'), []), ResourceRecords)

    @property
    def name(self):
        return self.data.get('Name')

    @property
    def ttl(self):
        return self.data.get("TTL")

    @property
    def type(self):
        return self.data.get("Type")

    @property
    def resource_records(self):
        return self._items_iterator


class ResourceRecords:
    def __init__(self, json_as_dict):
        self.data = json_as_dict

    # c'est une liste
    # @property
    # def value(self):
    #     return self.data.get('value')


class GenericWrappingIterator:
    """
    Iterate over wrapped dict items from a list in an API response.

    This iterator allows to iterate over wrapped representation of entities contained
    in the API response.
    """
    def __init__(self, items, wrapper_class):
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

    def __next__(self):
        """Used in for..in loops to get the next item."""
        return self._wrapper_class(next(self._items_iterator))

    def __getitem__(self, key: int):
        """[] operator"""
        return self._wrapper_class(self._items[key])

    def __len__(self):
        """Used by the builtin len() function."""
        return len(self._items)