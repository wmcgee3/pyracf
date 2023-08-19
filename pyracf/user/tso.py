from ..utils import get_message_value


class Tso:
    __slots__ = ["_name"]

    def __init__(self, name: str):
        self._name = name

    @property
    def account_number(self):
        return get_message_value(self._name, "tso", "ACCTNUM")

    @property
    def command(self):
        return get_message_value(self._name, "tso", "COMMAND")

    @property
    def max_size(self):
        return int(get_message_value(self._name, "tso", "MAXSIZE"))

    @property
    def proc(self):
        return get_message_value(self._name, "tso", "PROC")

    @property
    def size(self):
        return int(get_message_value(self._name, "tso", "SIZE"))

    @property
    def unit(self):
        return get_message_value(self._name, "tso", "UNIT")

    @property
    def user_data(self):
        return get_message_value(self._name, "tso", "USERDATA")
