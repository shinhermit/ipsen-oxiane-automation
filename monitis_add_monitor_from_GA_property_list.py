"""
This script creates all the monitors for each properties
given in a csv file on the Monitis Application
"""

from webapis.monitisapi import api_connector
import csv
from webapis import utils


def main():
    parser = utils.get_input_arg_parser(description="Dump the list of all Google Analytics properties.")
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


def set_values(resource_url):
    if resource_url[-1] == "/":
        resource_url = resource_url[:-1]
    monitor_name = resource_url+"_RUM"
    return monitor_name


if __name__ == "__main__":
    main()
