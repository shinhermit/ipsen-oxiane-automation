import requests
import datetime
import json

from src import settings


class Service:
    """
    Monitis connection utility.

    api_key, secret_key and agent_key can be obtanined from the Monitis account under the Tools > API menu.
    """
    def __init__(self):
        with open(settings.monitisapi["credentials"]["client_secret_path"], "r") as file:
            secret_credentials = json.loads(file.read())
        self.api_key = secret_credentials["api_key"]
        self.secret_key = secret_credentials["secret_key"]
        self.agent_key = secret_credentials["agent_key"]
        self.user_key = secret_credentials["user_key"]

    def get_auth_token_request_data(self) -> dict:
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

        :return: a dictionary that can be used to create the query string for the
        call to the Monitis API
        """
        return {
            "action": settings.monitisapi["api_actions"]["get_auth_token"],
            "apikey": self.api_key,
            "secretkey": self.secret_key
        }

    def get_add_monitor_request_data(self, auth_token: str,
                                     monitor_name: str,
                                     resource_url: str,
                                     monitor_type: str = settings.monitisapi["monitor"]["monitor_default_type"],
                                     monitor_params: str = settings.monitisapi["monitor"]["monitor_params"],
                                     result_params: str = settings.monitisapi["monitor"]["result_params"],
                                     action: str = settings.monitisapi["api_actions"]["add_rum"],
                                     from_dashboard: bool = True,
                                     record_api_call: bool = False,
                                     version: str = settings.monitisapi["api_version"],
                                     auth_method: str = settings.monitisapi["credentials"]["auth_method"],
                                     tag: str = settings.monitisapi["monitor"]["default_tag"]) -> dict:
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
            "apikey": self.api_key,
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

    def get_token(self) -> str:
        response = requests.get(
            settings.monitisapi["api_url"],
            params=self.get_auth_token_request_data())
        return response.json()["authToken"]

    def add_rum_monitor(self, monitor_name: str, resource_url: str, auth_token: str):
        data = self.get_add_monitor_request_data(
            auth_token=auth_token,
            monitor_name=monitor_name,
            resource_url=resource_url)
        response = requests.post(settings.monitisapi["api_url"], data=data)
        print(response.json())

    def list_monitors(self):
        search_url = settings.monitisapi["search_url"].format(user_key=self.user_key)
        response = requests.get(search_url)
        return response.json()["searchItems"]["monitors"]

service = Service()
