import csv
import re
from src import settings
from src.googleapi.api_connector import get_service
from googleapiclient.http import BatchHttpRequest
from src.googleapi.tagmanagerapi.data_model import AccountsList, ContainersList
from src import utils


parser = utils.get_input_arg_parser(description="Add tags in google tag manager base on a "
                                                "list of google analytics properties from a CSV file.")
args = parser.parse_args()

tag_manager_settings = settings.googleapi["tag_manager"]
api_tag_manager = get_service(api_name=tag_manager_settings["api_name"],
                              api_version=tag_manager_settings['api_version'],
                              client_secrets_path=args.credentials,
                              scope=tag_manager_settings['scopes'])

account_list = AccountsList(api_tag_manager.accounts().list().execute())

for account in account_list.account:
    test = ContainersList(api_tag_manager.accounts().containers().list(parent='accounts/' + account.account_id).execute())

for oui in test.container:
    print(oui.container_id)