from webapis.common.data_model import GenericWrappingIterator
from typing import NamedTuple


class ResourceRecordSetList:
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

    def __init__(self, json_as_dict: dict):
        """
        :param json_as_dict: a dictionary that represent the JSON response from the boto3 API
        """
        self.data = json_as_dict
        self._items_iterator = GenericWrappingIterator(self.data.get("ResourceRecordSets", []), ResourceRecordSet)

    @property
    def is_truncated(self) -> bool:
        """Indicate if there is more items to display. If so, you can display them by indicating the next marker"""
        return self.data.get("IsTruncated")

    @property
    def max_items(self) -> str:
        """The value of max items that you have give in parameters when you call the API. Default value is 100"""
        return self.data.get("MaxItems")

    @property
    def next_record_name(self) -> str:
        """Indicate the name of the next Record"""
        return self.data.get('NextRecordName')

    @property
    def next_record_type(self) -> str:
        """Indicate the type of the next Record"""
        return self.data.get('NextRecordType')

    @property
    def next_record_identifier(self) -> str:
        """Indicate the ID of the next Record"""
        return self.data.get('NextRecordIdentifier')

    @property
    def resource_record_sets(self) -> GenericWrappingIterator:
        """"""
        return self._items_iterator


class ResourceRecordSet:
    """
    Wrapper other an AWS Route53 resource record set.

    The JSON data has the form:

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
    }

     API reference page:
     http://boto3.readthedocs.io/en/latest/reference/services/route53.html#Route53.Client.list_resource_record_sets
    """
    def __init__(self, json_as_dict: dict):
        self.data = json_as_dict
        self._items_iterator = GenericWrappingIterator(self.data.get("ResourceRecords", []), ResourceRecord)

    @property
    def name(self) -> str:
        """Indicate the name of the domain on which you want t perform actions"""
        return self.data.get('Name')

    @property
    def type(self) -> str:
        """Indicate the type of the DNS record"""
        return self.data.get("Type")

    @property
    def set_identifier(self) -> str:
        """ An identifier that differentiates among multiple resource record sets
         that have the same combination of DNS name and type"""
        return self.data.get('SetIdentifier')

    @property
    def weight(self) -> int:
        return self.data.get('Weight')

    @property
    def region(self) -> str:
        """Indicate the region in which is set the actual resource record set"""
        return self.data.get('Region')

    @property
    def failover(self) -> str:
        return self.data.get('Failover')

    @property
    def multi_value_answer(self) -> bool:
        return self.data.get('MultiValueAnswer')

    @property
    def ttl(self) -> int:
        """Indicate the lifetime of the Resource Record Cache"""
        return self.data.get("TTL")

    @property
    def resource_records(self) -> GenericWrappingIterator:
        """
        Iterator to iterate over ResourceRecords items of this ResourceRecordSet.

        :rtype: GenericWrappingIterator of ResourceRecord
        """
        return self._items_iterator

    @property
    def health_check_id(self) -> str:
        """Indicate if you want to check the integrity of a resource record set"""
        return self.data.get('HealthCheckId')

    @property
    def traffic_policy_instance_id(self) -> str:
        """Indicate the ID of the traffic policy instance record"""
        return self.data.get('TrafficPolicyInstanceId')

    @property
    def geo_location(self) -> NamedTuple:
        """An object that gives information about the location of queries"""
        geo_location = self.data.get('GeoLocation')
        if geo_location:
            geo_location = NamedTuple("GeoLocation", [("continent_code", str), ("country_code", str),
                                                      ("subdivision_code", str)])(
                continent_code=geo_location.get('ContinentCode'),
                country_code=geo_location.get('CountryCode'),
                subdivision_code=geo_location.get('SubdivisionCode'))
        return geo_location

    @property
    def alias_target(self) -> NamedTuple:
        """An object that gives information about an alias target"""
        alias_target = self.data.get('AliasTarget')
        if alias_target:
            alias_target = NamedTuple("GeoLocation", [("hosted_zone_id", str), ("dns_name", str)])(
                hosted_zone_id=alias_target['HostedZoneId'],
                dns_name=alias_target['DNSName'])
        return alias_target


class ResourceRecord:
    """
    Wrapper other an AWS Route53 resource record.

    The JSON data has the form:

    {
        'Value': 'string'
    }

     API reference page:
     http://boto3.readthedocs.io/en/latest/reference/services/route53.html#Route53.Client.list_resource_record_sets
    """
    def __init__(self, json_as_dict):
        self.data = json_as_dict

    @property
    def value(self) -> str:
        """Give the value of the Resource Record"""
        return self.data.get('Value')
