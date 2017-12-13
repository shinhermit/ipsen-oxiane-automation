"""
This script creates properties in Google Search Console based on
properties declared in Google Analytics
"""
import csv

from googleapiclient.http import BatchHttpRequest
from oauth2client import tools

import settings
from webapis import utils
from webapis.googleapi.api_connector import get_service


def main():
    parser = utils.get_input_arg_parser(description="Add sites in google search console base on a "
                                                    "list of google analytics properties from a CSV file.",
                                        parents=[tools.argparser])
    args = parser.parse_args()

    search_console_settings = settings.googleapi["search_console"]
    api_search_console = get_service(api_name=search_console_settings["api_name"],
                                     api_version=search_console_settings['api_version'],
                                     client_secrets_path=args.credentials,
                                     scope=search_console_settings['scopes'],
                                     flags=args)

    batch = BatchHttpRequest()
    with open(args.input_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            website_url = row["Properties"]
            account = row["Account"]
            print("Currently in the %s Account, adding %s to Google Search Console" % (account, website_url))
            batch.add(api_search_console.sites().add(siteUrl=website_url))
    batch.execute()


if __name__ == "__main__":
    main()
