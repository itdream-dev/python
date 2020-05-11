import types


class Registry(dict):
    """ A lockable dictionary, intended to be used to store
        references to external resources """
    def __init__(self, *args, **kwargs):
        self._locked = False
        dict.__init__(self, *args, **kwargs)

    def lock(self):
        self._locked = True

    def is_locked(self):
        return self._locked

    def __setitem__(self, key, val):
        assert not self._locked
        dict.__setitem__(self, key, val)

    def update(self, *args, **kwargs):
        assert not self._locked
        dict.update(self, *args, **kwargs)

    def __getitem__(self, key):
        result = dict.__getitem__(self, key)
        if isinstance(result, types.FunctionType):
            result = result()
            dict.__setitem__(self, key, result)
        return result


THE_REGISTRY = Registry()


def get_registry():
    return THE_REGISTRY
