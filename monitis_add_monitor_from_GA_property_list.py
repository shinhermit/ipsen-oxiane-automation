"""
This script creates all the monitors for each properties
given in a csv file on the Monitis Application
"""

from webapis.monitisapi import api_connector
import csv
from webapis import utils
from webapis.utils import cli_col


welcome_msg = """
-------------------------------------------------------------------------------------------------
**                                                                                             **
**                                   MONITIS'S MONITORS SYNC                                   **
**                                                                                             **
**  Add monitors in Monitis from a list of properties previously dumped from Google Analytics  **
-------------------------------------------------------------------------------------------------
"""


def main():
    """
    Add monitors in Monitis from a list of properties previously dumped
    from Google Analytics.

    This script expects:
     - a credentials file which contains the Monitis API credentials
     - the path to the input file that contains some previously dumped
     Google Analytics properties.
     The directories of this path must exist.

     The credentials file contains JSON in the form:

    ```
        {
          "api_key": "your api key",
          "secret_key": "your secret key",
          "agent_key": "your agent key",
          "user_key": "your user key"
        }
    ```

    Usage:

    ```
    <python 3 interpreter> monitis_add_monitor_from_GA_property_list.py \
            --credentials etc/credentials/monitisapi/secret_credentials.json \
            --input etc/dump/GA_property_list.csv
    ```
    """
    cli_col.print_header(welcome_msg)
    parser = utils.get_input_arg_parser(description="Add monitors in Monitis from a list of properties "
                                                    "previously dumped from Google Analytics.")
    args = parser.parse_args()

    monitors_dict = load_analytics_properties(args.input_file)
    add_monitors_via_api(monitors_dict, args.credentials)


def load_analytics_properties(csv_file: str) -> dict:
    """
    Loads the Google Analytics properties in a dictionary.

    This dictionary ensures each domain is represented
    only one time (as it is the key of the dictionary),
    avoiding duplicate network accesses for the same monitor.

    :param csv_file: path to the analytics properties CSV file
    to load.
    :return: a dictionary in the form:
    {
        "monitor_name" {
            "url": str,
            "account": str
        }
    }
    """
    monitors_dict = {}
    csv_lines_count = 0
    print("\nLoading Analytics Properties's CSV file...\n")
    with open(csv_file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            csv_lines_count += 1
            url = row.get('Properties')
            monitor_name = get_monitor_name(row.get('Without URL'))
            account = row['Account']
            monitors_dict[monitor_name] = {"url": url, "account": account}
            print("\t**** ", monitor_name, ", ", url, ", ", account)
    cli_col.print_green("\n%d CSV lines loaded\n" % csv_lines_count)
    return monitors_dict


def get_monitor_name(domain_name):
    return domain_name + "_RUM"


def add_monitors_via_api(monitors_dict: dict, api_credentials_file_path):
    service = api_connector.Service(api_credentials_file_path)
    auth_token = service.get_token()

    processed_properties_count = 0
    errors_count = 0
    for monitor_name, monitor_dict in monitors_dict.items():
        url = monitor_dict["url"]
        account = monitor_dict["account"]
        response = service.add_rum_monitor(auth_token=auth_token,
                                           monitor_name=monitor_name,
                                           resource_url=url,
                                           tag='["'+account+'"]')
        json_response = response.json()
        if response.status_code >= 300 or json_response.get("error"):
            errors_count += 1
            cli_col.print_red("\t" + str(json_response))
        else:
            processed_properties_count += 1
            print("\t**** ", monitor_name, ", ", url, ", ", account)
    cli_col.print_green("%d monitors added." % processed_properties_count)
    cli_col.print_red("%d errors." % errors_count)
    cli_col.print_good_bye_message()


if __name__ == "__main__":
    main()
