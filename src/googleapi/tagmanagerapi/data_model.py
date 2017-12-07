from typing import List

from src.common.data_model import GenericWrappingIterator


class AccountsList:
    """
    This class represent the result of a call to the accounts/list endpoint
    of the Google Tag Manager API.

    Each of this class' properties exactly maps to one of the JSON from the API response.

    API reference page:
    https://developers.google.com/tag-manager/api/v2/reference/accounts/list

    The JSON response has the following structure:

    {
        "account": [
            {
              "path": string,
              "accountId": string,
              "name": string,
              "shareData": boolean,
              "fingerprint": string,
              "tagManagerUrl": string
            }
            ],
        "nextPageToken": string
    }
    """

    def __init__(self, json_as_dict):
        """

        :param json_as_dict: a dictionary that represent the JSON response from the Tag Manager API
        """
        self.data = json_as_dict
        self._accounts_iterator = GenericWrappingIterator(self.data.get("account", []), Account)

    @property
    def account(self) -> GenericWrappingIterator:
        """
        Iterator to iterate over Account items of this AccountList.

        :rtype: GenericWrappingIterator of Account
        """
        return self._accounts_iterator

    @property
    def next_page_token(self) -> str:
        """Give the token to fetch the remaining accounts on the next page"""
        return self.data.get('nextPageToken')


class Account:
    """
    This class represent an Account item from the items section of the result of a call to the
    tagmanager/v2/accounts endpoint of the Google Tag Manager API.

    Each of this class' properties exactly maps to one of the JSON from the API response.

    API reference page:
    https://developers.google.com/tag-manager/api/v2/reference/accounts#resource
    """

    def __init__(self, json_as_dict):
        self.data = json_as_dict

    @property
    def path(self):
        """Give the relative path of the Google Tag Manager Account"""
        return self.data.get('path')

    @property
    def account_id(self):
        """Give the unique ID of the Google Tag Manager Account"""
        return self.data.get('accountId')

    @property
    def name(self):
        """Give the name of Google Tag Manager Account"""
        return self.data.get('name')

    @property
    def share_data(self):
        """Indicate if the Google Tag Manager Account share data anonymously with Google and others"""
        return self.data.get('shareData')

    @property
    def finger_print(self):
        """The fingerprint of the GTM Account as computed at storage time."""
        return self.data.get('fingerprint')

    @property
    def tag_manager_url(self):
        """Give an url to the Google Tag Manager UI"""
        return self.data.get('tagManagerUrl')


class ContainersList:
    """
    This class represent the result of a call to the containers/list endpoint
    of the Google Tag Manager API.

    Each of this class' properties exactly maps to one of the JSON from the API response.

    API reference page:
    https://developers.google.com/tag-manager/api/v2/reference/accounts/containers/list

    The JSON response has the following structure:

    {
      "container": [
        {
          "path": string,
          "accountId": string,
          "containerId": string,
          "name": string,
          "domainName": [
            string
          ],
          "publicId": string,
          "notes": string,
          "usageContext": [
            string
          ],
          "fingerprint": string,
          "tagManagerUrl": string
        }
      ],
      "nextPageToken": string
    }
    """

    def __init__(self, json_as_dict):
        self.data = json_as_dict
        self._containers_iterator = GenericWrappingIterator(self.data.get("container", []), Container)

    @property
    def container(self):
        return self._containers_iterator

    @property
    def next_page_token(self) -> str:
        """Give the token to fetch the remaining containers on the next page"""
        return self.data.get('nextPageToken')


class Container:
    """
    This class represent an Account item from the items section of the result of a call to the
    tagmanager/v2/containers endpoint of the Google Tag Manager API.

    Each of this class' properties exactly maps to one of the JSON from the API response.

    API reference page:
    https://developers.google.com/tag-manager/api/v2/reference/accounts/containers#resource
    """

    def __init__(self, json_as_dict):
        self.data = json_as_dict

    @property
    def path(self) -> str:
        """Give the relative path of the Google Tag Manager Container"""
        return self.data.get('path')

    @property
    def account_id(self) -> str:
        """Give the ID of the Container's Account"""
        return self.data.get('accountId')

    @property
    def container_id(self) -> str:
        """Give the Container ID"""
        return self.data.get('containerId')

    @property
    def name(self) -> str:
        """Give the name of the Container"""
        return self.data.get('name')

    @property
    def notes(self) -> str:
        """The notes written about a Container"""
        return self.data.get('notes')

    @property
    def public_id(self) -> str:
        return self.data.get('publicId')

    @property
    def finger_print(self) -> str:
        """The fingerprint of the GTM Account as computed at storage time."""
        return self.data.get('fingerprint')

    @property
    def tag_manager_url(self) -> str:
        """Give an url to the Google Tag Manager UI"""
        return self.data.get('tagManagerUrl')

    @property
    def domain_name(self) -> List[str]:
        """List all the domain names associate with the Container"""
        return self.data.get('domainName')

    @property
    def usage_context(self) -> List[str]:
        """List the usage context for the Container. Ex : Web, Android or IOS"""
        return self.data.get('usageContext')
