"""
This script creates properties in Google Search Console based on
properties declared in Google Analytics
"""

from src import settings
from src.googleapi.api_connector import get_service
from src.googleapi.analyticss.data_models import AccountSummaryList
from googleapiclient.http import BatchHttpRequest


def main():
    client_secrets_path = settings.googleapi["credentials"]['client_secret_path']

    analytics_settings = settings.googleapi["analytics"]
    api_analytics = get_service(api_name=analytics_settings["api_name"],
                                api_version=analytics_settings['api_version'],
                                client_secrets_path=client_secrets_path,
                                scope=analytics_settings['scopes'])

    search_console_settings = settings.googleapi["search_console"]
    api_search_console = get_service(api_name=search_console_settings["api_name"],
                                     api_version=search_console_settings['api_version'],
                                     client_secrets_path=client_secrets_path,
                                     scope=search_console_settings['scopes'])

    account_summaries = api_analytics.management().accountSummaries().list().execute(num_retries=10)
    acc_list = AccountSummaryList(account_summaries)

    batch = BatchHttpRequest()
    print("accounts: ", len(acc_list.items))
    nb_web_properties = 0
    for account in acc_list.items:
        nb_web_properties += len(account.web_properties)
        for web_property in account.web_properties:
            batch.add(api_search_console.sites().add(siteUrl=web_property.website_url))
    print("web properties", nb_web_properties)
    batch.execute()


if __name__ == "__main__":
    main()
