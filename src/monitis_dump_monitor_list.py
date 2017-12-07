from src import settings
from src.monitisapi import api_connector
from src.monitisapi import data_model
import utils


def main():
    parser = utils.get_output_arg_parser(
        description='Dump the list of monitor in Monitis into a CSV file.',
        default_credentials=settings.monitisapi["credentials"]["client_secret_path"],
        default_input_file=settings.monitisapi["monitor"]["dump_file"])
    args = parser.parse_args()
    service = api_connector.Service(args.credentials)
    res = service.list_monitors()
    with open(args.dump_file, "w+") as file:
        for monitor in data_model.MonitorWrappingIterable(res):
            csv_line = '"{domain}","{url}",{id}\r\n'.format(
                domain=monitor.params.domain,
                url=monitor.params.domain,
                id=monitor.id)
            file.write(csv_line)


if __name__ == "__main__":
    main()
