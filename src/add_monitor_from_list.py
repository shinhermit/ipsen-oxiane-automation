"""
This script creates all the monitors for each properties
given in a csv file on the Monitis Application
"""

from src.monitisapi import api_connector
import csv
import sys


def main():
    auth_token = api_connector.get_token()
    cpt = 0
    if len(sys.argv) > 1 and sys.argv[1].endswith('csv'):
        with open(sys.argv[1], "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cpt += 1
                resource_url, monitor_name = set_values(row['Properties'].split('//')[1])
                api_connector.add_rum_monitor(auth_token=auth_token,
                                              monitor_name=monitor_name,
                                              resource_url=resource_url,
                                              tag='["'+row['Account']+'"]')
    elif len(sys.argv) == 1:
        print("Please give a file to the script")
    else:
        print("Please give a csv file to the script")


def set_values(resource_url):
    if resource_url[-1] == "/":
        resource_url = resource_url[:-1]
    if resource_url[0:3] == "www.":
        monitor_name = resource_url[3:]+"_RUM"
    else:
        monitor_name = resource_url+"_RUM"
    return resource_url, monitor_name


if __name__ == "__main__":
    main()
