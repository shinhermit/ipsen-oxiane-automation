"""
This script creates a list of all the properties (and the corresponding account)
from a given Google Analytics Account
"""
import csv
import re

from oauth2client import tools

import settings
from webapis import utils
from webapis.googleapi.analyticss.data_model import AccountSummaryList
from webapis.googleapi.api_connector import get_service


def main():
    parser = utils.get_output_arg_parser(description="Dump the list of all Google Analytics properties.",
                                         parents=[tools.argparser])
    args = parser.parse_args()

    analytics_settings = settings.googleapi["analytics"]
    api_analytics = get_service(api_name=analytics_settings["api_name"],
                                api_version=analytics_settings['api_version'],
                                client_secrets_path=args.credentials,
                                scope=analytics_settings['scopes'],
                                flags=args)

    account_summaries = api_analytics.management().accountSummaries().list().execute(num_retries=10)
    acc_list = AccountSummaryList(account_summaries)

    with open(args.dump_file, 'w+', newline='') as csv_file:
        wr = csv.writer(csv_file)
        wr.writerow(("Account Id", "Account", "Properties Id", "Properties", "Without URL"))
        for account in acc_list.items:
            for web_property in account.web_properties:
                wo_url = re.sub(r'(.*//www.|.*//)', '', web_property.website_url)
                wo_url = re.sub(r'/.*', '', wo_url)
                print("Currently in \"%s\" Account, in the \"%s\" Property" % (account.name, web_property.name))
                if web_property.website_url:
                    wr.writerow((account.id, account.name, web_property.id, web_property.website_url, wo_url))


if __name__ == "__main__":
    main()
