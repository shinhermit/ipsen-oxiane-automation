from src.common.data_model import GenericWrappingIterator


class HostedZone:
    """
    This class represents the result of a call to the route53/list_hosted_zones endpoint
    of boto3, the API for AWS.

    Each of this class' properties exactly maps to one of the JSON from the API response.

     API reference page:
     http://boto3.readthedocs.io/en/latest/reference/services/route53.html#Route53.Client.list_hosted_zones

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
        """The value of max items that you have give in parameters when you call the API"""
        return self.data.get("MaxItems")

    @property
    def resource_record_sets(self):
        """"""
        return self._items_iterator

    @property
    def maker(self):
        return self.data.get("Marker")

    @property
    def next_marker(self):
        return self.data.get("NextMarker")


class ResourceRecordSets:
    """
    This class represent a hosted zone from the list in the ResourceRecordSets section
     of the result of a call to the route53/list_hosted_zones endpoint of the AWS API.

    Each of this class' properties exactly maps to one of the JSON from the API response.

    API reference page:
    http://boto3.readthedocs.io/en/latest/reference/services/route53.html#Route53.Client.list_hosted_zones
    """
    def __init__(self, json_as_dict):
        self.data = json_as_dict
        self._items_iterator = GenericWrappingIterator(self.data.get("ResourceRecords", []), ResourceRecords)

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
        return None

    @property
    def resource_records(self):
        if self.data.get('ResourceRecords'):
            return self._items_iterator
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
