
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
        self._items_iterator1 = GenericWrappingIterator(self.data.get("ResourceRecords", []), ResourceRecords)

    @property
    def name(self):
        return self.data.get('Name')

    @property
    def region(self):
        return self.data.get('Region')

    @property
    def ttl(self):
        return self.data.get("TTL")

    @property
    def type(self):
        return self.data.get("Type")

    @property
    def geo_location(self):
        if self.data.get('GeoLocation'):
            continent_code = self.data.get('GeoLocation')['ContinentCode']
            keys = self.data.get('GeoLocation').keys()
            if "CountryCode" in keys:
                country_code = self.data.get('GeoLocation')['CountryCode']
            else:
                country_code = None
            if "SubdivisionCode" in keys:
                subdivision_code = self.data.get('GeoLocation')['SubdivisionCode']
            else:
                subdivision_code = None
            return GeoLocation(continent_code, country_code, subdivision_code)
        else:
            return None

    @property
    def resource_records(self):
        if self.data.get('ResourceRecords'):
            return self._items_iterator1
        else:
            return None

    @property
    def alias_target(self):
        if self.data.get('AliasTarget'):
            return AliasTarget(self.data.get('AliasTarget')['HostedZoneId'], self.data.get('AliasTarget')['DNSName'])
        else:
            return None


class ResourceRecords:
    def __init__(self, json_as_dict):
        self.data = json_as_dict

    @property
    def value(self):
        return self.data.get('Value')


class GeoLocation:
    def __init__(self, continent_code, country_code=None, subdivision_code=None):
        self.continent_code = continent_code
        self.country_code = country_code
        self.subdivision_code = subdivision_code

    @property
    def continent_code_get(self):
        return self.continent_code

    @property
    def country_code_get(self):
        return self.country_code

    @property
    def subdivision_code_get(self):
        return self.subdivision_code


class AliasTarget:
    def __init__(self,  hosted_zoned_id, dns_name):
        self.hosted_zone_id = hosted_zoned_id
        self.dns_name = dns_name

    @property
    def dns_name_get(self):
        return self.dns_name

    @property
    def hosted_zone_id_get(self):
        return self.hosted_zone_id


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
