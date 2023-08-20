from ._utils import _get_messages

__all__ = ["RacfResource"]


class RacfResource:
    __slots__ = ["_name"]

    def __init__(self, name: str):
        self._name = name

    @property
    def application_data(self):
        return _get_messages("resource", self._name)[14]

    @property
    def auditing(self):
        return _get_messages("resource", self._name)[18]

    @property
    def class_(self):
        return _get_messages("resource", self._name)[2].split()[0]

    @property
    def installation_data(self):
        return _get_messages("resource", self._name)[10]

    @property
    def level(self):
        return _get_messages("resource", self._name)[6].split()[0]

    @property
    def name(self):
        return _get_messages("resource", self._name)[2].split()[1]

    @property
    def notify(self):
        return _get_messages("resource", self._name)[22]

    @property
    def owner(self):
        return _get_messages("resource", self._name)[6].split()[1]

    @property
    def universal_access(self):
        return _get_messages("resource", self._name)[6].split()[2]

    @property
    def warning(self):
        return _get_messages("resource", self._name)[6].split()[4]

    @property
    def your_access(self):
        return _get_messages("resource", self._name)[6].split()[3]
