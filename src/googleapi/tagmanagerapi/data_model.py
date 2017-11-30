
class AccountsList:

    def __init__(self, json_as_dict):
        self.data = json_as_dict
        self._accounts_iterator = GenericWrappingIterator(self.data.get("account", []), Account)

    @property
    def account(self):
        return self._accounts_iterator


class Account:

    def __init__(self, json_as_dict):
        self.data = json_as_dict

    @property
    def path(self):
        return self.data.get('path')

    @property
    def account_id(self):
        return self.data.get('accountId')

    @property
    def name(self):
        return self.data.get('name')


class ContainersList:

    def __init__(self, json_as_dict):
        self.data = json_as_dict
        self._containers_iterator = GenericWrappingIterator(self.data.get("container", []), Container)

    @property
    def container(self):
        return self._containers_iterator


class Container:

    def __init__(self, json_as_dict):
        self.data = json_as_dict

    @property
    def path(self):
        return self.data.get('path')

    @property
    def account_id(self):
        return self.data.get('accountId')

    @property
    def container_id(self):
        return self.data.get('containerId')

    @property
    def name(self):
        return self.data.get('name')


class GenericWrappingIterator:

    def __init__(self, items, wrapper_class):
        self._items = items
        self._wrapper_class = wrapper_class
        self._items_iterator = iter(items)

    def __iter__(self):
        return self

    def __next__(self):
        return self._wrapper_class(next(self._items_iterator))

    def __getitem__(self, key):
        return self._wrapper_class(self._items['key'])

    def __len__(self):
        return len(self._items)

