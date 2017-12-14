"""
http://boto3.readthedocs.io/en/latest/reference/services/route53.html#Route53.Client.list_hosted_zones
"""
from typing import List
import boto3
import yaml
from webapis.awsapi.data_model import ResourceRecordSetList
from webapis import utils
from webapis.utils import Console

welcome_msg = """
-------------------------------------------------------------------------------------------------
**                                                                                             **
**                         AMAZON WEB SERVICES ROUTE 53 BACKUP FILES                           **
**                                                                                             **
**                         Create templates of Route 53 Hosted Zones                           **
-------------------------------------------------------------------------------------------------
"""


def main():
    Console.print_header(welcome_msg)
    parser = utils.get_output_arg_parser(description="Create a YAML backup for AWS route53",
                                         require_credentials=False)
    args = parser.parse_args()

    client = boto3.client('route53')
    print("\nRetrieving Route53 Hosted Zones...\n")
    request_result = client.list_hosted_zones()

    report_total_hosted_zones = 0

    while request_result is not None:
        for hosted_zone in request_result['HostedZones']:
            report_total_hosted_zones += 1
            zone_id = hosted_zone["Id"].split('/')[2]
            zone_name = hosted_zone["Name"]
            print("Creating template for %s zone" % zone_name)
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
                        "DependsOn": "Zone",
                        "Type": "AWS::Route53::RecordSetGroup",
                        "Properties": {
                            "HostedZoneName": zone_name,
                            "Comment": "Zone record for " + zone_name + " HostedZoneId is " + zone_id,
                            "RecordSets": get_resource_record_set_cloud_formation_dict_list(
                                zone_details, client, zone_id)
                        }
                    }
                }
            }
            with open(args.dump_file + zone_name + 'yml', 'w+') as outfile:
                yaml.dump(cloud_formation_template_dict, outfile, explicit_start=True, width=1000,
                          default_flow_style=False)
            print("\t\t ++ \tDone")
        next_marker = request_result.get('NextMarker')
        if next_marker is not None:
            print("\nRetrieving Route 53 next Hosted Zones\n")
            request_result = client.list_hosted_zones(Marker=next_marker)
        else:
            request_result = None
    Console.print_green("%s templates have been created" % report_total_hosted_zones)
    Console.print_good_bye_message()


def get_resource_record_set_cloud_formation_dict_list(hosted_zone: ResourceRecordSetList, client,
                                                      zone_id: str) -> List[dict]:
    """
    Provide a dict representation of a resource record set that can
    be used to dump a cloud formation formatted YAML file.

    :return: a dict in the form:
        {
            "Name": str,
            "Type": str,
            "TTL": str,
            "ResourceRecord": [str],
            "AliasTarget": {
                "DNSName": str,
                "HostedZoneId": str
            }
        }
    """
    results_are_not_truncated = not hosted_zone.is_truncated
    next_record_name = hosted_zone.next_record_name
    hosted_zone_has_next_record = next_record_name is not None or results_are_not_truncated

    resource_record_set_cloud_formation_dict_list = []
    while hosted_zone_has_next_record:
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
                resource_record_set_cloud_formation_dict['ResourceRecords'] = resource_record_values
            if resource_record_set.alias_target:
                resource_record_set_cloud_formation_dict['AliasTarget'] = {
                    "DNSName": resource_record_set.alias_target.dns_name,
                    "HostedZoneId": resource_record_set.alias_target.hosted_zone_id
                }

            resource_record_set_cloud_formation_dict_list.append(resource_record_set_cloud_formation_dict)
        if results_are_not_truncated:
            hosted_zone_has_next_record = False
        else:
            hosted_zone = ResourceRecordSetList(client.list_resource_record_sets(HostedZoneId=zone_id,
                                                                                 StartRecordName=next_record_name))
            next_record_name = hosted_zone.next_record_name
            hosted_zone_has_next_record = next_record_name is not None
    return resource_record_set_cloud_formation_dict_list


if __name__ == "__main__":
    main()
