"""
This script creates a list of all the properties (and the corresponding account)
from a given Google Analytics Account
"""
import csv
import logging
import re
from src import settings
from src.googleapi.api_connector import get_service
from src.googleapi.analyticss.data_model import AccountSummaryList


def main():
    client_secrets_path = settings.googleapi["credentials"]['client_secret_path']

    analytics_settings = settings.googleapi["analytics"]
    api_analytics = get_service(api_name=analytics_settings["api_name"],
                                api_version=analytics_settings['api_version'],
                                client_secrets_path=client_secrets_path,
                                scope=analytics_settings['scopes'])

    account_summaries = api_analytics.management().accountSummaries().list().execute(num_retries=10)
    acc_list = AccountSummaryList(account_summaries)

    with open(settings.googleapi['analytics']['dump_file'], 'w+', newline='') as csvfile:
        wr = csv.writer(csvfile)
        wr.writerow(("Account Id", "Account", "Properties Id", "Properties", "Without URL"))
        for account in acc_list.items:

            print(account.data)
            for web_property in account.web_properties:
                wo_url = re.sub(r'(.*//www.|.*//)', '', web_property.website_url)
                wr.writerow((account.id, account.name, web_property.id, web_property.website_url, wo_url))


if __name__ == "__main__":
    main()
