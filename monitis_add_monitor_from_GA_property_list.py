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

    service = api_connector.Service(args.credentials)
    auth_token = service.get_token()
    monitors_dict = {}
    with open(args.input_file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            props = row.get('Properties')
            dns = row.get('Without URL')
            if props:
                if dns.find('/'):
                    dns = dns.split('/')[0]
                parts = props.split('//')
                if len(parts) > 1:
                    monitor_name = set_values(dns)
                    monitors_dict[monitor_name] = {"url": parts[1], "account": row['Account']}
            else:
                print("Warning, this property can't be monitored.It might be an application")
    for monitor_name, monitor in monitors_dict.items():
        service.add_rum_monitor(auth_token=auth_token,
                                monitor_name=monitor_name,
                                resource_url=monitor.get('url'),
                                tag='["'+monitor.get('account')+'"]')
    cli_col.print_good_bye_message()


def set_values(resource_url):
    if resource_url[-1] == "/":
        resource_url = resource_url[:-1]
    monitor_name = resource_url+"_RUM"
    return monitor_name


if __name__ == "__main__":
    main()
