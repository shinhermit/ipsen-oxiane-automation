from collections import OrderedDict

import boto3
import pprint
import yaml
import datetime
from src import settings
from src.awsapi.data_model import HostedZone


def append_dict(record_set):
        returned_list = []
        # for record in record_set.resource_record_sets:
        for record in record_set['ResourceRecordSets']:
            temp = []
            # dictionary = {"Name": record.name,
            #               "Type": record.type,
            #               "TTL": record.ttl}
            dictionary = {"Name": record['Name'],
                          "Type": record['Type']}
            # for resource in record.resource_records:
            if "ResourceRecords" in record.keys():
                dictionary['TTL'] = record['TTL']
                for resource in record['ResourceRecords']:
                    temp.append(resource['Value'])
                    dictionary['ResourceRecord'] = temp

            elif "AliasTarget" in record.keys():
                    dictionary['AliasTarget'] = {"DNSName": record['AliasTarget']['DNSName'],
                                                 "HostedZoneId": record['AliasTarget']['HostedZoneId']}
            returned_list.append(dictionary)
        return returned_list


pp = pprint.PrettyPrinter()
hosted_zone_list = []
client = boto3.client('route53')
result = client.list_hosted_zones()

for hosted_zone in result['HostedZones']:
    hosted_zone_list.append({"id": hosted_zone["Id"].split('/')[2], "name": hosted_zone["Name"]})

for zone in hosted_zone_list:
    result = client.list_resource_record_sets(HostedZoneId=zone["id"])
    # pp.pprint(result)
    # data = HostedZone(client.list_resource_record_sets(HostedZoneId=zone["id"]))
    yaml_dump = {"AWSTemplateFormatVersion": str(datetime.datetime.now().strftime('%Y-%m-%d')),
                 "Description": "Backup definition for the "+zone['name']+" zone",
                 "Resources": {"Zone": {"Type": "AWS::Route53::HostedZone",
                                        "Properties": {"Name": zone["name"]}},
                               "records": {"Type": "AWS::Route53::RecordSetGroup",
                                           "Properties": {"HostedZoneId": zone["id"],
                                                          "comment": "Zone record for "+zone['name'],
                                                          "RecordSets": append_dict(result)}}}}
    # append_dict(data)
    pp.pprint(yaml_dump)
    with open(settings.awsapi['route53']['dump_file_path']+zone["name"]+'yml', 'w') as outfile:
        yaml.dump(yaml_dump, outfile, default_flow_style=False)
    print("Iteration .................................")





