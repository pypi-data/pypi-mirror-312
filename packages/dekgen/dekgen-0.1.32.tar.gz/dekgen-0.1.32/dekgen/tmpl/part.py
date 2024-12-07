import functools


class Cache:
    def __init__(self, master):
        self.master = master
        self.caches = {}

    def __getitem__(self, method):
        return functools.partial(self.__run, method)

    def __getattr__(self, method):
        return self[method]

    def __run(self, method):
        if method not in self.caches:
            self.caches[method] = getattr(self.master, method)()
        return self.caches[method]


class Repr:
    def __init__(self, value, delay=False):
        self.value = value
        self.delay = delay

    def final_value(self):
        return self.value

    def __repr__(self):
        value = self.final_value()
        return f'lambda: {value}' if self.delay else value

    def __copy__(self):
        return self.__class__(self.value, self.delay)

    def __deepcopy__(self, memo):
        return self.__class__(self.value, self.delay)


class ReprTuple(Repr):
    def __init__(self, value, delay=False):
        super().__init__(list(value), delay)

    def final_value(self):
        return repr(tuple(self.value))

    def __getattr__(self, item):
        return getattr(self.value, item)
