import datetime
import typing

from src import settings


def get_auth_token_request_data(
        api_key: str = settings.monitisapi["credentials"]["api_key"],
        secret_key: str = settings.monitisapi["credentials"]["secret_key"]) -> dict:
    """
    Obtain an auth token.

    Usage example:
    ``
    auth_token = api_connector.get_token()
    api_connector.add_monitor(
        auth_token=auth_token,
        monitor_name="ipsen-oxiane.blogspot.fr_RUM",
        resource_url="ipsen-oxiane.blogspot.fr")
    ``

    API reference: http://www.monitis.com/api/customApiActions.html#getAuthToken

    :param api_key: API access key. Can be obtain via the Monitis account
    under the Tools > API menu.
    :param secret_key:API access secret key. Can be obtain via the Monitis account
    under the Tools > API menu.
    :return: a dictionary that can be used to create the query string for the
    call to the Monitis API
    """
    return {
        "action": settings.monitisapi["api_actions"]["get_auth_token"],
        "apikey": api_key,
        "secretkey": secret_key
    }


def get_add_monitor_request_data(auth_token: str,
                                 monitor_name: str,
                                 resource_url: str,
                                 tag: str or settings.monitisapi["monitor"]["default_tag"],
                                 monitor_type: str = settings.monitisapi["monitor"]["monitor_default_type"],
                                 monitor_params: str = settings.monitisapi["monitor"]["monitor_params"],
                                 result_params: str = settings.monitisapi["monitor"]["result_params"],
                                 action: str = settings.monitisapi["api_actions"]["add_rum"],
                                 from_dashboard: bool = True,
                                 record_api_call: bool = False,
                                 version: str = settings.monitisapi["api_version"],
                                 auth_method: str = settings.monitisapi["credentials"]["auth_method"]) -> dict:
                                 # tag: str = settings.monitisapi["monitor"]["default_tag"]) -> dict:
    """
    Provides a dictionary that can be used to create a monitor in Monitis.

    Usage example:
    ``
    auth_token = api_connector.get_token()
    api_connector.add_monitor(
        auth_token=auth_token,
        monitor_name="ipsen-oxiane.blogspot.fr_RUM",
        resource_url="ipsen-oxiane.blogspot.fr")
    ``

    API reference: http://www.monitis.com/api/api.html

    :param auth_method: how credentials are validated. For example, token
    :param auth_token: auth token for authentication.
    :param action: the action to take. For example, addMonitor to add a monitor.
    :param monitor_name: the name to assign to the monitor
    :param monitor_type: the type of monitor, for example RUM
    :param resource_url: the resource to monitor
    :param monitor_params: Parameters of the monitor in the following format:
    name1:displayName1:value1:dataType1:isHidden1[;name2:displayName2:value2:dataType2:isHidden2...].
    :param result_params: Result parameters in the following format:
    name1:displayName1:uom1:dataType1:hasFixedValues1:groups1:aggFunction1[;name2:displayName2:uom2:\
    dataType2:hasFixedValues1:groups1:aggFunction1...
    :param from_dashboard: tells whether of not the request comes from the dashboard.
    :param record_api_call: ??
    :param version: the version of API to invoke
    :param tag: the group name or list of the groups the monitor will belong to: E.g. ["dev", "ops"]
    """
    monitor_param_domain = "domain:Domain:{domain}:1:false:false".format(domain=resource_url)
    return{
        "apikey": settings.monitisapi["credentials"]["api_key"],
        "validation": auth_method,
        "authToken": auth_token,
        "action": action,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": monitor_name,
        "type": monitor_type,
        "url": resource_url,
        "monitorParams": monitor_params + ";" + monitor_param_domain,
        "resultParams": result_params,
        "tag": tag,
        "version": version,
        "output": "json",
        "recordApiCall": record_api_call,
        "fromDashboard": from_dashboard
    }


class MonitorWrappingIterable:
    """
    This iterable allows to iterate over a list of dict
    representation of monitor entities. For each monitor,
    it provides a wrapped version to work with.
    """
    def __init__(self, response_data: list):
        self._data = response_data
        self._iterator = iter(response_data)

    def __iter__(self) -> 'MonitorWrappingIterable':
        return self

    def __next__(self) -> 'Monitor':
        return Monitor(next(self._iterator))

    def __getitem__(self, key) -> 'Monitor':
        return self._data[key]

    def __len__(self) -> int:
        return len(self._data)


class Monitor:
    """
    Represents a monitor as return by Monitis when requesting the
    list pf all monitors.
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
    def __init__(self, response_data: dict):
        self._data = response_data

    @property
    def domain(self) -> str:
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
