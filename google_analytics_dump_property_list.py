"""
This script creates a list of all the properties (and the corresponding account)
from a given Google Analytics Account
"""
import csv

from oauth2client import tools

import settings
from webapis import utils
from webapis.googleapi.analyticss.data_model import AccountSummaryList
from webapis.googleapi.api_connector import get_service
from webapis.utils import cli_col


welcome_msg = """
-------------------------------------------------------------------------------------------------
**                                                                                             **
**                            GOOGLE ANALYTICS PROPERTIES DUMP                                 **
**                                                                                             **
**             Dump the list of all Google Analytics properties in a CSV file                  **
-------------------------------------------------------------------------------------------------
"""

goodbye_msg = """
-------------------------------------------------------------------------------------------------
**                                                                                             **
**                                      Good bye                                               **
**                                                                                             **
-------------------------------------------------------------------------------------------------
"""


def main():
    print(welcome_msg)
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
    print("\nRetrieving Accounts and properties list...\n")
    acc_list = AccountSummaryList(account_summaries)

    with open(args.dump_file, 'w+', newline='') as csv_file:
        wr = csv.writer(csv_file)
        wr.writerow(("Account Id", "Account", "Properties Id", "Properties", "Without URL"))
        report_total_accounts_count = 0
        report_total_properties_count = 0
        for account in acc_list.items:
            print("\n****** Account Name: %s , Account ID: %s" % (account.name, account.id))
            report_properties_count = 0
            for web_property in account.web_properties:
                url = web_property.website_url
                if url:
                    wo_url = utils.get_domain_name_from_url(url)
                    wr.writerow((account.id, account.name, web_property.id, url, wo_url))
                    report_properties_count += 1
                    report_total_properties_count += 1
                    print("\tProperty Name: %s, URL: %s\n\t\t ++ \tDone" % (web_property.name, url))
                else:
                    print(("\tProperty Name: %s, URL: %s\n\t\t ++ \t" +
                          cli_col.YELLOW+"Skipped"+cli_col.END_COL) % (web_property.name, url))
            print("\n\t****** Processed %d propertie(s) for this account" % report_properties_count)
            report_total_accounts_count += 1
    print("\nProcessed %d account(s) and %d propertie(s) in total." % (report_total_accounts_count,
                                                                       report_total_properties_count))
    print(goodbye_msg)


if __name__ == "__main__":
    main()
