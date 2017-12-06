import csv
import sys
import re
from src import settings
from src.googleapi.api_connector import get_service
from googleapiclient.http import BatchHttpRequest
from src.googleapi.tagmanagerapi.data_model import AccountsList

client_secrets_path = settings.googleapi["credentials"]['client_secret_path']
tag_manager_settings = settings.googleapi["tag_manager"]
api_tag_manager = get_service(api_name=tag_manager_settings["api_name"],
                              api_version=tag_manager_settings['api_version'],
                              client_secrets_path=client_secrets_path,
                              scope=tag_manager_settings['scopes'])

account_to_properties = {}


with open(sys.argv[1], "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not row["Account"] in account_to_properties:
            account_to_properties[row["Account"]] = [row["Properties"]]
        else:
            account_to_properties[row["Account"]].append(row["Properties"])

account_name_list = []
key_done = []
account_list = AccountsList(api_tag_manager.accounts().list().execute())
batch = BatchHttpRequest()

for account in account_list.account:
    for key in account_to_properties.keys():
        if key == account.name and key not in key_done:
            for prop in account_to_properties[key]:
                prop = re.sub(r'.*://', '', prop)
                if re.search(r'/', prop):
                    print("%s can't be add due to the /" % prop)
                else:
                    print(prop)
                    body = {
                        "name": prop,
                        "usageContext": ["web"]
                    }
                    batch.add(api_tag_manager
                              .accounts()
                              .containers()
                              .create(parent='accounts/' + account.account_id, body=body))
            key_done.append(key)
batch.execute()

for key in key_done:
    account_to_properties.pop(key)

for ma in account_to_properties.keys():
    print("The account %s is missing, please create it manually if you want to add some containers to it" % ma)


