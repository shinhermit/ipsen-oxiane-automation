"""
http://boto3.readthedocs.io/en/latest/reference/services/route53.html#Route53.Client.list_hosted_zones
"""
from typing import List
import boto3
import botocore.client
import yaml
from webapis.awsapi.data_model import ResourceRecordSetList
from webapis import utils
from webapis.utils import Console
from webapis.awsapi.utils import update_type_counter_aws_resource_record_set

welcome_msg = """
-------------------------------------------------------------------------------------------------
**                                                                                             **
**                         AMAZON WEB SERVICES ROUTE 53 BACKUP FILES                           **
**                                                                                             **
**                         Create templates of Route 53 Hosted Zones                           **
-------------------------------------------------------------------------------------------------
"""


def main():
    """
    Create a template for each Hosted Zones in AWS Route 53

    This script expects:
     - the path to the output file, where the template will be create.
     The directories of this path must exist.

    Usage:

    ```
    <python 3 interpreter> aws_dump_backup_files.py \
            --output etc/dump/AWS_backup_files/
    ```
    """

    Console.print_header(welcome_msg)
    parser = utils.get_output_arg_parser(description="Create a YAML backup for AWS route53",
                                         require_credentials=False)
    args = parser.parse_args()

    client = boto3.client('route53')
    print("\nRetrieving Route53 Hosted Zones...\n")
    request_result = client.list_hosted_zones()

    report_total_hosted_zones = 0

    while request_result is not None:
        for hosted_zone in request_result.get('HostedZones', ()):
            if dump_hosted_zone(hosted_zone, args.with_soa, args.dump_file, client):
                report_total_hosted_zones += 1
        next_marker = request_result.get('NextMarker')
        if next_marker:
            print("\nRetrieving Route 53 next Hosted Zones\n")
            request_result = client.list_hosted_zones(Marker=next_marker)
        else:
            request_result = None
    Console.print_green("%s templates have been created" % report_total_hosted_zones)
    Console.print_good_bye_message()


def dump_hosted_zone(hosted_zone: dict, with_soa: bool, output_file_path: str, boto3_client: botocore.client.BaseClient):
    zone_id = hosted_zone["Id"].split('/')[2]
    zone_name = hosted_zone["Name"]
    zone_details = ResourceRecordSetList(boto3_client.list_resource_record_sets(HostedZoneId=zone_id))
    type_counter_aws_resource_record_set = {}
    cloud_formation_template_dict = {
        "AWSTemplateFormatVersion": '2010-09-09',
        "Description": "Backup definition for the " + zone_name + " zone",
        "Resources": {
            "zone": {
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
                        zone_details, with_soa, boto3_client, zone_id, type_counter_aws_resource_record_set)
                }
            }
        }
    }
    file_name = output_file_path + zone_name + 'yml'
    set_record_list = cloud_formation_template_dict.get("Resources").get("records").get('Properties').get('RecordSets')
    if len(set_record_list) != 0:
        print("Creating template for %s zone" % zone_name)
        with open(file_name, 'w+') as outfile:
            yaml.dump(cloud_formation_template_dict, outfile,
                      explicit_start=True, width=1000, default_flow_style=False)
        print("\t\t File: ", file_name)
        print("\t\t Total Records: ", sum(type_counter_aws_resource_record_set.values()))
        print("\t\t Records types: ", str(type_counter_aws_resource_record_set))
        print("\t\t ++ \tDone\n")
        return True
    Console.print_red("Can't create %s zone template, recordSets is empty\n" % zone_name)
    return False


def get_resource_record_set_cloud_formation_dict_list(hosted_zone: ResourceRecordSetList,
                                                      with_soa: str,
                                                      client: botocore.client.BaseClient, zone_id: str,
                                                      type_counter_aws_resource_record_set: dict) -> List[dict]:
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
    resource_record_set_cloud_formation_dict_list = []
    while hosted_zone is not None:
        for resource_record_set in hosted_zone.resource_record_sets:
            resource_record_values = [resource_record.value
                                      for resource_record in resource_record_set.resource_records]
            if((resource_record_set.type != "SOA" and resource_record_set.type != "NS")
               or (with_soa and (resource_record_set.type == "SOA" or resource_record_set.type == "NS"))):
                resource_record_set_cloud_formation_dict = {
                    "Name": resource_record_set.name,
                    "Type": resource_record_set.type
                }
                update_type_counter_aws_resource_record_set(type_counter_aws_resource_record_set,
                                                            resource_record_set.type)

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
        next_record_name = hosted_zone.next_record_name
        if next_record_name:
            hosted_zone = ResourceRecordSetList(client.list_resource_record_sets(HostedZoneId=zone_id,
                                                                                 StartRecordName=next_record_name))
        else:
            hosted_zone = None
    return resource_record_set_cloud_formation_dict_list


if __name__ == "__main__":
    main()
