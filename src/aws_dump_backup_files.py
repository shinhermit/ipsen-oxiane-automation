"""
http://boto3.readthedocs.io/en/latest/reference/services/route53.html#Route53.Client.list_hosted_zones
"""


import boto3
import yaml
from src.awsapi.data_model import ResourceRecordSetList
from src import utils


def main():
    parser = utils.get_output_arg_parser(description="Create a YAML backup for AWS route53",)
    args = parser.parse_args()

    client = boto3.client('route53')
    request_result = client.list_hosted_zones()

    for hosted_zone in request_result['HostedZones']:
        zone_id = hosted_zone["Id"].split('/')[2]
        zone_name = hosted_zone["Name"]
        zone_details = ResourceRecordSetList(client.list_resource_record_sets(HostedZoneId=zone_id))
        cloud_formation_template_dict = {
            "AWSTemplateFormatVersion": '2010-09-09',
            "Description": "Backup definition for the " + zone_name + " zone",
            "Resources": {
                "Zone": {
                    "Type": "AWS::Route53::HostedZone",
                    "Properties": {
                        "Name": zone_name
                    }
                },
                "records": {
                    "Type": "AWS::Route53::RecordSetGroup",
                    "Properties": {
                        "HostedZoneId": zone_id,
                        "comment": "Zone record for " + zone_name,
                        "RecordSets": get_resource_record_set_cloud_formation_dict_list(zone_details)
                    }
                }
            }
        }
        with open(args.dump_file + zone_name + 'yml', 'w+') as outfile:
            yaml.dump(cloud_formation_template_dict, outfile, explicit_start=True, width=1000, default_flow_style=False)


def get_resource_record_set_cloud_formation_dict_list(hosted_zone):
    resource_record_set_cloud_formation_dict_list = []
    for resource_record_set in hosted_zone.resource_record_sets:
        resource_record_values = [resource_record.value
                                  for resource_record in resource_record_set.resource_records]

        resource_record_set_cloud_formation_dict = {
            "Name": resource_record_set.name,
            "Type": resource_record_set.type
        }

        if resource_record_set.ttl:
            resource_record_set_cloud_formation_dict['TTL'] = resource_record_set.ttl
        if resource_record_values:
            resource_record_set_cloud_formation_dict['ResourceRecord'] = resource_record_values
        if resource_record_set.alias_target:
            resource_record_set_cloud_formation_dict['AliasTarget'] = {
                "DNSName": resource_record_set.alias_target.dns_name,
                "HostedZoneId": resource_record_set.alias_target.hosted_zone_id
            }

        resource_record_set_cloud_formation_dict_list.append(resource_record_set_cloud_formation_dict)
    return resource_record_set_cloud_formation_dict_list


if __name__ == "__main__":
    main()
