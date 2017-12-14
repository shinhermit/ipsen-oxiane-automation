"""
For the accounts:  https://developers.google.com/tag-manager/api/v2/reference/accounts/get
For the containers : https://developers.google.com/tag-manager/api/v2/reference/accounts/containers/create
"""


import csv

from googleapiclient.http import BatchHttpRequest
from oauth2client import tools

import settings
from webapis import utils
from webapis.googleapi.api_connector import get_service
from webapis.googleapi.tagmanagerapi.data_model import AccountsList
from webapis.utils import Console
from webapis.googleapi.utils import batch_http_request_default_callback

welcome_msg = """
-------------------------------------------------------------------------------------------------
**                                                                                             **
**                            GOOGLE TAG MANAGER SYNC                                          **
**                                                                                             **
**     Synchronize Google Tag Manager containers on Analytics properties from a CSV file       **
-------------------------------------------------------------------------------------------------
"""


def main():
    """
    Dump the list of all Google Analytics properties in a CSV file.

    This script expects:
     - the client_secret.json file which you can download from your
     Google Developer Console, and
     - the path to the input file that contains some previously dumped
     Google Analytics properties.
     The directories of this path must exist.

    Usage:

    ```
    <python 3 interpreter>  google_tagmanager_add_from_analytics_property_list.py \
            --credentials etc/credentials/googleapi/client_secret.json \
            --input etc/dump/GA_property_list.csv
    ```
    """
    Console.print_header(welcome_msg)
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

    print("\nRetrieving Accounts and properties list from csv file...\n")
    analytics_account_properties_dict = get_analytics_account_properties_dict_from_csv(args.input_file)

    processed_accounts = []
    print("\nRetrieving Accounts list from Google Tag Manager...\n")
    tagmanager_account_list = AccountsList(api_tag_manager.accounts().list().execute())

    batch = BatchHttpRequest(callback=batch_http_request_default_callback)

    report_total_accounts_count = 0
    report_total_containers_count = 0

    for account in tagmanager_account_list.account:
        account_name = account.name
        account_id = account.account_id
        report_containers_count = 0
        account_exist = analytics_account_properties_dict.get(account_name)
        print("\nChecking Account existence and state...")
        if account_exist and account_name not in processed_accounts:
            print("\nAccount name: %s , Account Id: %s" % (account_name, account_id))
            for prop in analytics_account_properties_dict[account_name]:
                report_total_containers_count += 1
                report_containers_count += 1
                domain = utils.get_domain_name_from_url(prop)
                print("\tDomain Name: %s, URL: %s\n\t\t ++ \tDone " % (domain, prop))
                body = {
                    "name": domain,
                    "usageContext": ["web"]
                }
                batch.add(api_tag_manager.accounts().containers().create(parent='accounts/' + account_id,
                                                                         body=body),
                          callback=lambda *x: print(account_id, ", ", str(body)))
            print("\n\t****** ", report_containers_count, " tags creation request added "
                                                          "to batch for this account")
            report_total_accounts_count += 1
            processed_accounts.append(account.name)
            analytics_account_properties_dict.pop(account_name)
        else:
            print("\nThe Account %s doesn't exist" % account_name)
    batch.execute()
    Console.print_green("\nProcessed ", report_total_accounts_count,
                        " account(s) and ", report_total_containers_count, " Container(s) in total.")

    for missing_account in analytics_account_properties_dict.keys():
        Console.print_red("\nThe Google Analytics account +", missing_account,
                          "+ is missing as a container in Tag Manger. Please "
                          "create it manually if you want to add some containers to it")
    Console.print_good_bye_message()


def get_analytics_account_properties_dict_from_csv(csv_file_path: str) -> dict:
    account_to_properties = {}
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            account = row["Account"]
            account_property = row["Properties"]
            if account not in account_to_properties and account_property != '':
                account_to_properties[account] = [account_property]
            elif account_property != '':
                account_to_properties[account].append(account_property)
    return account_to_properties


if __name__ == "__main__":
    main()


