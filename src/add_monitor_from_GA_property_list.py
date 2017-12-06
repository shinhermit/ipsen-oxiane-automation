"""
This script creates all the monitors for each properties
given in a csv file on the Monitis Application
"""

from src.monitisapi import api_connector
import csv
import sys


def main():
    auth_token = api_connector.service.get_token()
    dico = {}
    with open(sys.argv[1], "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            props = row.get('Properties')
            dns = row.get('Sans URL')
            if props:
                if dns.find('/'):
                    dns = dns.split('/')[0]
                parts = props.split('//')
                if len(parts) > 1:
                    monitor_name = set_values(dns)
                    dico[monitor_name] = {"url": parts[1], "account": row['Account']}
            else:
                print("Warning, this property can't be monitored.It might be an application")
    for key in dico.keys():
        api_connector.service.add_rum_monitor(auth_token=auth_token,
                                              monitor_name=key,
                                              resource_url=dico[key].get('url'),
                                              tag='["'+dico[key].get('account')+'"]')


def set_values(resource_url):
    if resource_url[-1] == "/":
        resource_url = resource_url[:-1]
    monitor_name = resource_url+"_RUM"
    return monitor_name


if __name__ == "__main__":
    main()
