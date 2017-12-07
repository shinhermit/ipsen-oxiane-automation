import typing
from src import utils


class Monitor:
    """
    Represents a monitor as return by Monitis when requesting the
    list of all monitors.

    The wrapped data has the form:

    {
        "name": "ipsen.co.uk_RUM",
        "categoryId": 8,
        "category": "RUM",
        "type": "RUM",
        "id": 124115,
        "tag": "External Communication",
        "groups": ["External Communication"],
        "enabled": 1,
        "dataTypeId": 25,
        "params": {
            "ignoreQueryParams": "true",
            "domain": "www.ipsen.co.uk/",
            "aggType": "median"
        },
        "monitorTypeId": 71
    }
    """
    def __init__(self, response_data: dict):
        self._data = response_data

    @property
    def id(self) -> int:
        """ID of the monitor"""
        return self._data.get("id")

    @property
    def name(self) -> str:
        """Name of the monitor"""
        return self._data.get("name")

    @property
    def params(self) -> 'MonitorParams':
        """Key-value parameters of the monitor"""
        return MonitorParams(self._data.get("params", {}))

    @property
    def type(self) -> str:
        """The type of this Monitor, for example RUM"""
        return self._data.get("type")

    @property
    def category(self) -> str:
        """The monitor category to which this type of monitor belongs"""
        return self._data.get("category")

    @property
    def groups(self) -> typing.List[str]:
        """Groups to wich this monitor belong"""
        return self._data.get("groups")

    @property
    def tag(self) -> str:
        """Tags associated with this monitor"""
        return self._data.get("tag")

    @property
    def enabled(self) -> int:
        """Tell whether or not this monitor is enabled"""
        return self._data.get("enabled")

    @property
    def data_type_id(self) -> int:
        return self._data.get("dataTypeId")

    @property
    def category_id(self) -> str:
        return self._data.get("categoryId")

    @property
    def monitor_type_id(self) -> int:
        return self._data.get("monitorTypeId")


class MonitorParams:
    """
    Wrap over Monitis' monitor params.

    The wrapped data has the form:

    {
        "ignoreQueryParams": "true",
        "domain": "www.ipsen.co.uk/",
        "aggType": "median"
    }
    """
    def __init__(self, response_data: dict):
        self._data = response_data

    @property
    def domain(self) -> str:
        """The monitored domain"""
        return utils.substring_after(utils.substring_before(self._data.get("domain"), "/"), "www.")

    @property
    def url(self) -> str:
        """The monitored domain"""
        return self._data.get("domain")

    @property
    def ignore_query_params(self) -> bool:
        """
        If True, query params are taken into account to
        differentiate URIs. Otherwise query params are ignored.
        In the latter case, example.com?d=1 is the same resource as
        example.com and example.com?x=1&y=2
        """
        return self._data.get("ignoreQueryParams")

    @property
    def agg_type(self) -> str:
        return self._data.get("aggType")
