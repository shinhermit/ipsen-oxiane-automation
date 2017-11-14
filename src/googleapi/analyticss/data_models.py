"""
The classes in this module represent the data model of Google Analytics API.

They are basically wrapper over dicts parsed from JSON returned by the API. These models
allow a better understanding of the data used in the scripts.

API reference page: https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/
"""


class AccountSummaryList:
    """
    This class represent the result of a call to the accountSummaries/list endpoint
    of the Google Analytics API.

    Each of this class' properties exactly maps to one of the JSON from the API response.

    API reference page:
    https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/accountSummaries/list

    The JSON reponse has the foolowing structure:

    {
      "kind": "analytics#accountSummaries",
      "username": string,
      "totalResults": integer,
      "startIndex": integer,
      "itemsPerPage": integer,
      "previousLink": string,
      "nextLink": string,
      "items": [
        {
          "id": string,
          "kind": "analytics#accountSummary",
          "name": string,
          "starred": boolean,
          "webProperties": [
            {
              "kind": "analytics#webPropertySummary",
              "id": string,
              "name": string,
              "internalWebPropertyId": string,
              "level": string,
              "websiteUrl": string,
              "starred": boolean,
              "profiles": [
                {
                  "kind": "analytics#profileSummary",
                  "id": string,
                  "name": string,
                  "type": string,
                  "starred": boolean
                }
              ]
            }
          ]
        }
      ]
    }
    """
    def __init__(self, json_as_dict: dict):
        """
        :param json_as_dict: a dictionary that represent the JSON response from the Google API
        :type json_as_dict: dict
        """
        self.data = json_as_dict
        self._items_iterator = GenericWrappingIterator(self.data.get("items", []), AccountSummary)

    @property
    def kind(self):
        return self.data.get("kind")

    @property
    def username(self):
        return self.data.get("username")

    @property
    def total_results(self):
        return self.data.get("totalResults")

    @property
    def start_index(self):
        return self.data.get("startIndex")

    @property
    def items_per_page(self):
        return self.data.get("itemsPerPage")

    @property
    def previous_link(self):
        return self.data.get("previousLink")

    @property
    def next_link(self):
        return self.data.get("nextLink")

    @property
    def items(self):
        return self._items_iterator


class AccountSummary:
    """
    This class represent an AccountSummary item from the items section of the result of a call to the
    /management/accountSummaries endpoint of the Google Analytics API.

    Each of this class' properties exactly maps to one of the JSON from the API response.

    API reference page:
    https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/accountSummaries
    """
    def __init__(self, json_as_dict):
        self.data = json_as_dict
        self._items_iterator = GenericWrappingIterator(self.data.get("webProperties", []), WebProperty)

    @property
    def id(self):
        return self.data.get("id")

    @property
    def kind(self):
        return self.data.get("kind")

    @property
    def name(self):
        return self.data.get("name")

    @property
    def web_properties(self):
        return self._items_iterator


class WebProperty:
    """
        This class represent a WebProperty  from the webProperties section in an AccountSummary item

        Each of this class' properties exactly maps to one of the JSON from the API response.

        API reference page:
        https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/accountSummaries
        """
    def __init__(self, json_as_dict):
        self.data = json_as_dict
        self._profile_iterator = GenericWrappingIterator(self.data.get("profiles", []), Profile)

    @property
    def kind(self):
        return self.data.get("kind")

    @property
    def id(self):
        return self.data.get("id")

    @property
    def name(self):
        return self.data.get("name")

    @property
    def internal_web_property_id(self):
        return self.data.get("internalWebPropertyId")

    @property
    def level(self):
        return self.data.get("level")

    @property
    def website_url(self):
        return self.data.get("websiteUrl")

    @property
    def profiles(self):
        return self._profile_iterator


class Profile:
    """
        This class represent a Profile from the profiles section in a WebProperty item

        Each of this class' properties exactly maps to one of the JSON from the API response.

        API reference page:
        https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/accountSummaries
    """
    def __init__(self, json_as_dict):
        self.data = json_as_dict

    @property
    def kind(self):
        return self.data.get("kind")

    @property
    def id(self):
        return self.data.get("id")

    @property
    def name(self):
        return self.data.get("name")

    @property
    def type(self):
        return self.data.get("type")


class GenericWrappingIterator:
    """
    Iterate over wrapped dict items from a list in an API response.

    This iterator allows to iterate over wrapped representation of entities contained
    in the API response.
    """
    def __init__(self, items, wrapper_class):
        self._wrapper_class = wrapper_class
        self._items = items
        self._items_iterator = iter(items)

    def __iter__(self):
        return self

    def __next__(self):
        return self._wrapper_class(next(self._items_iterator))

    def __getitem__(self, key):
        return self._wrapper_class(self._items[key])

    def __len__(self):
        return len(self._items)
