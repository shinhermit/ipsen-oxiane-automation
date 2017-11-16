from src.monitisapi import api_connector
from src.monitisapi import data_model
from src import settings


def main():
    res = api_connector.list_monitors()
    with open(settings.monitisapi['monitor']['dump_file'], "w+") as file:
        for monitor in data_model.MonitorWrappingIterable(res):
            csv_line = '"{domain}","{url}",{id}\r\n'.format(
                domain=monitor.params.domain,
                url=monitor.params.domain,
                id=monitor.id)
            file.write(csv_line)


if __name__ == "__main__":
    main()
