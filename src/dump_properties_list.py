"""
This script creates properties in Google Search Console based on
properties declared in Google Analytics
"""
import csv
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
        wr.writerow(("Properties", "Account"))
        for account in acc_list.items:
            for web_property in account.web_properties:
                wr.writerow((web_property.website_url, account.name))


if __name__ == "__main__":
    main()
