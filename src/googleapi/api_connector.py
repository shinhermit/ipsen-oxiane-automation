# This file contains *modified* copies of source code samples provided by Google for its APIs.
# These code samples are licensed under the Apache 2.0 License:
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import httplib2
import googleapiclient
from typing import List
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from googleapiclient.discovery import build

from src import settings


def create_oauth_flow(client_secrets_path: str, scope: List[str]) -> client.Flow:
    """
    Create an OAuth flow to use to create credentials for authentication (using OAuth)
    """
    return client.flow_from_clientsecrets(client_secrets_path,
                                          scope=scope,
                                          message=tools.message_if_missing(client_secrets_path))


def get_authorized_http_object(api_name: str, flow: client.Flow) -> httplib2.Http:
    """
    Create an OAuth authorized http object.

    :param api_name: name of the api. Will be used as the name of the credentials file
    :param flow: the OAuth flow object to use to create credentials
    :return: authorize http object
    """
    credentials_base_path = settings.googleapi["credentials"]["credentials_base_path"]
    storage = file.Storage(credentials_base_path + api_name + '.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage)
    return credentials.authorize(http=httplib2.Http())


def get_service(api_name: str, api_version: str, scope: List[str], client_secrets_path: str)\
        -> googleapiclient.discovery.Resource:
    """
    Get a service that communicates to a Google API.

    :param api_name: The name of the api to connect to.
    :param api_version: The api version to connect to.
    :param scope: A list of strings representing the auth
    scopes to authorize for the connection.
    :param client_secrets_path: A path to a valid client secrets file.
    :return: A service that is connected to the specified API.
    """
    flow = create_oauth_flow(client_secrets_path, scope)
    http = get_authorized_http_object(api_name, flow)
    return build(api_name, api_version, http=http)
