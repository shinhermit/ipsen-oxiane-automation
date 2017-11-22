import boto3
import pprint
import yaml
import datetime
from src import settings


def append_dict(record_set):
        returned_list = []
        for data in record_set['ResourceRecordSets']:
            temp = []
            dictionary = {"Name": data['Name'],
                          "Type": data["Type"],
                          "TTL": data['TTL']}
            for oui in data['ResourceRecords']:
                temp.append(oui['Value'])
                dictionary['ResourceRecord'] = temp
            returned_list.append(dictionary)
        return returned_list


pp = pprint.PrettyPrinter()
liste_hosted_zone = []
client = boto3.client('route53')
result = client.list_hosted_zones()

for zone in result['HostedZones']:
    liste_hosted_zone.append({"id": zone["Id"].split('/')[2], "name": zone["Name"]})

for test in liste_hosted_zone:
    result = client.list_resource_record_sets(HostedZoneId=test["id"])
    pp.pprint(result)
    yaml_dump = {"AWSTemplateFormatVersion": str(datetime.datetime.now().strftime('%Y-%m-%d')),
                 "Description": "Backup definition for the "+test['name']+" zone",
                 "Resources": {"Zone": {"Type": "AWS::Route53::HostedZone",
                                        "Properties": {"Name": test["name"]}},
                               "records": {"Type": "AWS::Route53::RecordSetGroup",
                                           "Properties": {"HostedZoneId": test["id"],
                                                          "comment": "Zone record for "+test['name'],
                                                          "RecordSets": append_dict(result)}}}}
    with open(settings.awsapi['route53']['dump_file_path']+test["name"]+'yml', 'w') as outfile:
        yaml.dump(yaml_dump, outfile, default_flow_style=False)
    print("Iteration .................................")





