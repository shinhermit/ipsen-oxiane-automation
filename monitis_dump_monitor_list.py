from webapis.monitisapi import api_connector
from webapis.monitisapi.data_model import Monitor
from webapis.common.data_model import GenericWrappingIterator
from webapis import utils


def main():
    """
    Dum the list of all Monitis' monitors in a CSV file.

    This script expects:
     - a credentials file which contains the Monitis API credentials
     - the path to the output file, where the data will be written.
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
    <python 3 interpreter>  monitis_dump_monitor_list.py \
            --credentials etc/credentials/monitisapi/secret_credentials.json \
            --output etc/dump/monitis_rum_monitors.csv
    ```
    """
    parser = utils.get_output_arg_parser(description='Dump the list of monitor in Monitis into a CSV file.')
    args = parser.parse_args()

    service = api_connector.Service(args.credentials)
    res = service.list_monitors()
    with open(args.dump_file, "w+") as file:
        file.write("Domain,URL,Monitor ID\n")
        for monitor in GenericWrappingIterator(res, Monitor):
            csv_line = '"{domain}","{url}",{id}\r\n'.format(
                domain=monitor.params.domain,
                url=monitor.params.url,
                id=monitor.id)
            file.write(csv_line)


if __name__ == "__main__":
    main()
