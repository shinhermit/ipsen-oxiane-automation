"""
This script creates properties in Google Search Console based on
properties declared in Google Analytics
"""
import csv

from googleapiclient.http import BatchHttpRequest
from oauth2client import tools

import settings
from webapis import utils
from webapis.utils import Console
from webapis.googleapi.api_connector import get_service
from webapis.googleapi.utils import batch_http_request_default_callback


welcome_msg = """
-------------------------------------------------------------------------------------------------
**                                                                                             **
**                            GOOGLE SEARCH CONSOLE SYNC                                       **
**                                                                                             **
**    Synchronize Google Search Console sites on Analytics properties from a CSV file          **
-------------------------------------------------------------------------------------------------
"""


def main():
    """
    Synchronize Google Search Console sites on Analytics properties
    from a CSV file.

    This script expects:
     - the client_secret.json file which you can download from your
     Google Developer Console, and
     - the path to the input file that contains some previously dumped
     Google Analytics properties.
     The directories of this path must exist.

    Usage:

    ```
    <python 3 interpreter> google_search_console_add_from_analytics_property_list.py \
            --credentials etc/credentials/googleapi/client_secret.json \
            --input etc/dump/GA_property_list.csv
    ```
    """
    Console.print_header(welcome_msg)
    parser = utils.get_input_arg_parser(description="Add sites in google search console base on a "
                                                    "list of google analytics properties from a CSV file.",
                                        parents=(tools.argparser,))
    args = parser.parse_args()

    search_console_settings = settings.googleapi["search_console"]
    api_search_console = get_service(api_name=search_console_settings["api_name"],
                                     api_version=search_console_settings['api_version'],
                                     client_secrets_path=args.credentials,
                                     scope=search_console_settings['scopes'],
                                     flags=args)

    batch = BatchHttpRequest(callback=batch_http_request_default_callback)
    with open(args.input_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        print("Preparing batch request:")
        sites_count = 0
        for row in reader:
            website_url = row["Properties"]
            batch.add(api_search_console.sites().add(siteUrl=website_url),
                      callback=(lambda *x: print(website_url)))
            sites_count += 1
            print("\t** Analytics account: %s, Site URL: %s" % (row["Account"], website_url))
    Console.print_green("\n", sites_count, " sites added to batch request")
    batch.execute()
    Console.print_good_bye_message()


if __name__ == "__main__":
    main()
