import datetime

from src import settings


def get_auth_token_request_data(
        api_key: str = settings.monitisapi["credentials"]["api_key"],
        secret_key: str = settings.monitisapi["credentials"]["secret_key"]) -> dict:
    """
    Obtain an auth token.

    API reference: http://www.monitis.com/api/customApiActions.html#getAuthToken

    :param api_key: API access key. Can be obtain via the Monitis account
    under the Tools > API menu.
    :param secret_key:API access secret key. Can be obtain via the Monitis account
    under the Tools > API menu.
    :return: a dictionary that can be used to create the query string for the
    call to the Monitis API
    """
    return {
        "action": settings.monitisapi["actions"]["get_auth_token"],
        "apikey": api_key,
        "secretkey": secret_key
    }


def get_add_monitor_request_data(auth_token: str,
                                 monitor_name: str,
                                 resource_url: str,
                                 monitor_type: str = settings.monitisapi["monitor"]["monitor_type"],
                                 monitor_params: str = settings.monitisapi["monitor"]["monitor_params"],
                                 result_params: str = settings.monitisapi["monitor"]["result_params"],
                                 action: str = settings.monitisapi["actions"]["add_rum"],
                                 from_dashboard: bool = True,
                                 record_api_call: bool = False,
                                 version: str = settings.monitisapi["version"],
                                 auth_method: str = settings.monitisapi["credentials"]["auth_method"],
                                 tag: str = settings.monitisapi["monitor"]["default_tag"]) -> dict:
    """
    Provides a dictionary that can be used to create a monitor in Monitis.

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
