from src.common.data_model import GenericWrappingIterator
from collections import namedtuple


class ResourceRecordSetsList:
    """
    This class represents the result of a call to the route53/list_hosted_zones endpoint
    of boto3 , the API for AWS.

    Each of this class' properties exactly maps to one of the JSON from the API response.

     API reference page:
     http://boto3.readthedocs.io/en/latest/reference/services/route53.html#Route53.Client.list_resource_record_sets

     The JSON response has the following structure:

    {
        'ResourceRecordSets': [
            {
                'Name': 'string',
                'Type': 'SOA'|'A'|'TXT'|'NS'|'CNAME'|'MX'|'NAPTR'|'PTR'|'SRV'|'SPF'|'AAAA'|'CAA',
                'SetIdentifier': 'string',
                'Weight': 123,
                'Region': 'us-east-1'|'us-east-2'|'us-west-1'|'us-west-2'|'ca-central-1'|'eu-west-1'|'eu-west-2'|'eu-central-1'|'ap-southeast-1'|'ap-southeast-2'|'ap-northeast-1'|'ap-northeast-2'|'sa-east-1'|'cn-north-1'|'ap-south-1',
                'GeoLocation': {
                    'ContinentCode': 'string',
                    'CountryCode': 'string',
                    'SubdivisionCode': 'string'
                },
                'Failover': 'PRIMARY'|'SECONDARY',
                'MultiValueAnswer': True|False,
                'TTL': 123,
                'ResourceRecords': [
                    {
                        'Value': 'string'
                    },
                ],
                'AliasTarget': {
                    'HostedZoneId': 'string',
                    'DNSName': 'string',
                    'EvaluateTargetHealth': True|False
                },
                'HealthCheckId': 'string',
                'TrafficPolicyInstanceId': 'string'
            },
        ],
        'IsTruncated': True|False,
        'NextRecordName': 'string',
        'NextRecordType': 'SOA'|'A'|'TXT'|'NS'|'CNAME'|'MX'|'NAPTR'|'PTR'|'SRV'|'SPF'|'AAAA'|'CAA',
        'NextRecordIdentifier': 'string',
        'MaxItems': 'string'
    }
    """

    def __init__(self, json_as_dict):
        """
        :param json_as_dict: a dictionary that represent the JSON response from the boto3 API
        """
        self.data = json_as_dict
        self._items_iterator = GenericWrappingIterator(self.data.get("ResourceRecordSets", []), ResourceRecordSets)

    @property
    def is_truncated(self):
        """Indicate if there is more items to display. If so, you can display them by indicating the next marker"""
        return self.data.get("IsTruncated")

    @property
    def max_items(self):
        """The value of max items that you have give in parameters when you call the API. Default value is 100"""
        return self.data.get("MaxItems")

    @property
    def next_record_name(self):
        """Indicate the name of the next Record"""
        return self.data.get('NextRecordName')

    @property
    def next_record_type(self):
        """Indicate the type of the next Record"""
        return self.data.get('NextRecordType')

    @property
    def next_record_identifier(self):
        """Indicate the ID of the next Record"""
        return self.data.get('NextRecordIdentifier')

    @property
    def resource_record_sets(self):
        """"""
        return self._items_iterator


class ResourceRecordSets:
    def __init__(self, json_as_dict):
        self.data = json_as_dict
        self._items_iterator1 = GenericWrappingIterator(self.data.get("ResourceRecords", []), ResourceRecords)

    @property
    def name(self):
        """Indicate the name of the domain on which you want t perform actions"""
        return self.data.get('Name')

    @property
    def type(self):
        """Indicate the type of the DNS record"""
        return self.data.get("Type")

    @property
    def set_identifier(self):
        """ An identifier that differentiates among multiple resource record sets
         that have the same combination of DNS name and type"""
        return self.data.get('SetIdentifier')

    @property
    def weight(self):
        return self.data.get('Weight')

    @property
    def region(self):
        """Indicate the region in which is set the actual resource record set"""
        return self.data.get('Region')

    @property
    def geo_location(self):
        """An object that gives information about the location of queries"""
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
            return namedtuple("GeoLocation", "continent_code, country_code, subdivision_code")(
                              continent_code=continent_code, country_code=country_code,
                              subdivision_code=subdivision_code)
        return None

    @property
    def failover(self):
        return self.data.get('Failover')

    @property
    def multi_value_answer(self):
        return self.data.get('MultiValueAnswer')

    @property
    def ttl(self):
        """Indicate the lifetime of the Resource Record Cache"""
        return self.data.get("TTL")

    @property
    def resource_records(self) -> 'GenericWrappingIterator':
        """
        Iterator to iterate over ResourceRecords items of this ResourceRecordSets.

        :rtype: GenericWrappingIterator of ResourceRecords
        """
        if self.data.get('ResourceRecords'):
            return self._items_iterator1

    @property
    def alias_target(self):
        """An object that gives information about an alias target"""
        if self.data.get('AliasTarget'):
            return AliasTarget(self.data.get('AliasTarget')['HostedZoneId'], self.data.get('AliasTarget')['DNSName'])
        else:
            return None

    @property
    def health_check_id(self):
        """Indicate if you want to check the integrity of a resource record set"""
        return self.data.get('HealthCheckId')

    @property
    def traffic_policy_instance_id(self):
        """Indicate the ID of the traffic policy instance record"""
        return self.data.get('TrafficPolicyInstanceId')


class ResourceRecords:
    def __init__(self, json_as_dict):
        self.data = json_as_dict

    @property
    def value(self):
        """Give the value of the Resource Record"""
        return self.data.get('Value')


class GeoLocation:
    def __init__(self, continent_code, country_code=None, subdivision_code=None):
        self._continent_code = continent_code
        self._country_code = country_code
        self._subdivision_code = subdivision_code

    @property
    def continent_code_get(self):
        """Give the continent code"""
        return self._continent_code

    @property
    def country_code_get(self):
        """Give the country code code"""
        return self._country_code

    @property
    def subdivision_code_get(self):
        """Give the subdivision code code"""
        return self._subdivision_code


class AliasTarget:
    def __init__(self,  hosted_zoned_id, dns_name):
        self._hosted_zone_id = hosted_zoned_id
        self._dns_name = dns_name

    @property
    def dns_name_get(self):
        """Give the dns name of the Alias target"""
        return self._dns_name

    @property
    def hosted_zone_id_get(self):
        """Give the ID of the Hosted Zone of the Alias target"""
        return self._hosted_zone_id
