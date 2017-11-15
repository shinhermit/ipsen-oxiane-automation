import requests

from src import settings
from src.monitisapi import data_model


def get_token() -> str:
    response = requests.get(
        settings.monitisapi["api_url"],
        params=data_model.get_auth_token_request_data())
    return response.json()["authToken"]


def add_rum_monitor(monitor_name: str, resource_url: str, auth_token: str):
    data = data_model.get_add_monitor_request_data(
        auth_token=auth_token,
        monitor_name=monitor_name,
        resource_url=resource_url)
    response = requests.post(settings.monitisapi["api_url"], data=data)
    print(response.json())


def list_monitors():
    return
