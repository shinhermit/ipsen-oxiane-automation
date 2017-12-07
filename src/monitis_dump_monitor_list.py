from src.monitisapi import api_connector
from src.monitisapi import data_model
from src import utils


def main():
    parser = utils.get_output_arg_parser(description='Dump the list of monitor in Monitis into a CSV file.')
    args = parser.parse_args()

    service = api_connector.Service(args.credentials)
    res = service.list_monitors()
    with open(args.dump_file, "w+") as file:
        file.write("Domain,URL,Monitor ID\n")
        for monitor in data_model.MonitorWrappingIterable(res):
            csv_line = '"{domain}","{url}",{id}\r\n'.format(
                domain=monitor.params.domain,
                url=monitor.params.domain,
                id=monitor.id)
            file.write(csv_line)


if __name__ == "__main__":
    main()
