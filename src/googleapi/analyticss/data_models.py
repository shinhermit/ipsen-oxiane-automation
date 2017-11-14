
class AccountSummaryList:
    def __init__(self, json_as_dict):
        self.data = json_as_dict
        self._items_iterator = AccountSummaryList.AccountSummaryIterator(iter(self.data.get("items", [])))

    class AccountSummaryIterator:
        def __init__(self, items_iterator):
            self._items_iterator = items_iterator

        def __iter__(self):
            return self

        def __next__(self):
            return AccountSummary(next(self._items_iterator))

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
    def __init__(self, json_as_dict):
        self.data = json_as_dict
        self._properties_iterator = iter(self.data.get("webProperties", []))

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
    def starred(self):
        return self.data.get("starred")

    @property
    def web_properties(self):
        yield Property(next(self._properties_iterator))


class Property:
    def __init__(self, json_as_dict):
        self.data = json_as_dict


class Profile:
    def __init__(self, json_as_dict):
        self.data = json_as_dict
