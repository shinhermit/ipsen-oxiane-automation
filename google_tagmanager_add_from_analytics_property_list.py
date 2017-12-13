"""
For the accounts:  https://developers.google.com/tag-manager/api/v2/reference/accounts/get
For the containers : https://developers.google.com/tag-manager/api/v2/reference/accounts/containers/create
"""


import csv
import re

from googleapiclient.http import BatchHttpRequest
from oauth2client import tools

import settings
from webapis import utils
from webapis.googleapi.api_connector import get_service
from webapis.googleapi.tagmanagerapi.data_model import AccountsList

parser = utils.get_input_arg_parser(description="Add tags in google tag manager base on a "
                                                "list of google analytics properties from a CSV file.",
                                    parents=[tools.argparser])
args = parser.parse_args()

tag_manager_settings = settings.googleapi["tag_manager"]
api_tag_manager = get_service(api_name=tag_manager_settings["api_name"],
                              api_version=tag_manager_settings['api_version'],
                              client_secrets_path=args.credentials,
                              scope=tag_manager_settings['scopes'],
                              flags=args)

account_to_properties = {}


with open(args.input_file, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        if not row["Account"] in account_to_properties and row["Properties"] != '':
            account_to_properties[row["Account"]] = [row["Properties"]]
        elif row["Properties"] != '':
            account_to_properties[row["Account"]].append(row["Properties"])

key_done = []
account_list = AccountsList(api_tag_manager.accounts().list().execute())

batch = BatchHttpRequest()

# for account in account_list.account:
#     for key in account_to_properties.keys():
#         if key == account.name and key not in key_done:
#             for prop in account_to_properties[key]:
#                 prop = re.sub(r'.*://', '', prop)
#                 if re.search(r'/', prop):
#                     print("%s can't be add due to the /" % prop)
#                 else:
#                     print(prop)
#                     body = {
#                         "name": prop,
#                         "usageContext": ["web"]
#                     }
#                     batch.add(api_tag_manager
#                               .accounts()
#                               .containers()
#                               .create(parent='accounts/' + account.account_id, body=body))
#             key_done.append(key)
# batch.execute()

for account in account_list.account:
    account_exist = account_to_properties.get(account.name)
    if account_exist and account.name not in key_done:
        for prop in account_to_properties[account.name]:
            prop = re.sub(r'(.*://)(www.)?', '', prop)
            if re.search('/.*', prop):
                prop = re.sub(r'/.*', '', prop)
            body = {
                "name": prop,
                "usageContext": ["web"]
            }
            batch.add(api_tag_manager
                      .accounts()
                      .containers()
                      .create(parent='accounts/' + account.account_id, body=body))
        key_done.append(account.name)
batch.execute()

for key in key_done:
    account_to_properties.pop(key)

for ma in account_to_properties.keys():
    print("The account %s is missing, please create it manually if you want to add some containers to it" % ma)


