class Generator:
    def __init__(self, _list):
        self.pointer = 0
        self._list = _list

    def has_next(self):
        return self.pointer + 1 <= len(self._list)

    def next(self, offset=1):
        if self.has_next():
            self.pointer += offset
        return self.get()

    def get(self, offset=0):
        if 0 <= self.pointer + offset < len(self._list):
            return self._list[self.pointer + offset]
