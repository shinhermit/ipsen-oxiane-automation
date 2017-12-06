"""
http://boto3.readthedocs.io/en/latest/reference/services/route53.html#Route53.Client.list_hosted_zones
"""


import boto3
import yaml
import datetime
from src import settings
from src.awsapi.data_model import ResourceRecordSetsList


def main():

    hosted_zone_list = []
    client = boto3.client('route53')
    request_result = client.list_hosted_zones()

    for hosted_zone in request_result['HostedZones']:
        hosted_zone_list.append({"id": hosted_zone["Id"].split('/')[2], "name": hosted_zone["Name"]})

    for zone in hosted_zone_list:
        zone_details = ResourceRecordSetsList(client.list_resource_record_sets(HostedZoneId=zone["id"]))
        print(client.list_resource_record_sets(HostedZoneId=zone["id"]))
        yaml_dump = {#"AWSTemplateFormatVersion": str(datetime.datetime.now().strftime('%Y-%m-%d')),
                     "AWSTemplateFormatVersion": '2010-09-09',
                     "Description": "Backup definition for the "+zone['name']+" zone",
                     "Resources": {"Zone": {"Type": "AWS::Route53::HostedZone",
                                            "Properties": {"Name": zone["name"]}},
                                   "records": {"Type": "AWS::Route53::RecordSetGroup",
                                               "Properties": {"HostedZoneId": zone["id"],
                                                              "comment": "Zone record for "+zone['name'],
                                                              "RecordSets": append_dict(zone_details)}}}}
        with open(settings.awsapi['route53']['dump_file_path']+zone["name"]+'yml', 'w') as outfile:
            yaml.dump(yaml_dump, outfile, explicit_start=True, width=1000, default_flow_style=False)


def append_dict(hosted_zone):
    returned_list = []
    for resource_record_sets in hosted_zone.resource_record_sets:
        temp = []
        dictionary = {"Name": resource_record_sets.name,
                      "Type": resource_record_sets.type}
        if resource_record_sets.resource_records:
            for resource_records in resource_record_sets.resource_records:
                dictionary['TTL'] = resource_record_sets.ttl
                temp.append(resource_records.value)
                dictionary['ResourceRecord'] = temp
        elif resource_record_sets.alias_target:
            dictionary['AliasTarget'] = {"DNSName": resource_record_sets.alias_target.dns_name_get,
                                         "HostedZoneId": resource_record_sets.alias_target.hosted_zone_id_get}

        returned_list.append(dictionary)
    return returned_list


if __name__ == "__main__":
    main()
