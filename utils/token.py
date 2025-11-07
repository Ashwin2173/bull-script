from utils.tokentype import TokenType, to_string

from lang.exceptions import BullException

class Token:
    def __init__(self, raw, _type, line):
        self.raw = raw
        self._type = _type
        self.line = line

    def get_raw(self):
        return self.raw

    def get_type(self):
        return self._type

    def get_line(self):
        return self.line

    def match(self, *others):
        if self._type not in others:
            others = [to_string(other).lower() for other in others]
            raise BullException(f"Expected {' or '.join(others)}, but got {self.raw}")
        return self

    def contains(self, *items):
        return self._type in items

    def __eq__(self, other):
        if type(other) == TokenType:
            return self._type == other
        elif type(other) == str:
            return self.raw == other
        return False

    def __str__(self):
        return str(list([self.raw, self._type, self.line]))
