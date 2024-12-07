from dektools.dict import is_list


class Collection:
    def __init__(self, entry):
        self.entry = entry

    def append(self, name, data):
        raise NotImplementedError

    def set_data(self, data):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError


class CollectionGeneric(Collection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {}

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data


class DictCollection(CollectionGeneric):
    def append(self, name, data):
        self.data.update(data)


class NamedCollection(CollectionGeneric):
    def append(self, name, data):
        self.data[name] = data


class NamedListCollection(NamedCollection):
    def append(self, name, data):
        if is_list(data):
            super().append(name, data)
        else:
            self.data.update(data)
