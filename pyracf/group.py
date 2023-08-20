from datetime import datetime

from ._utils import _get_messages

__all__ = ["RacfGroup"]


class RacfGroup:
    __slots__ = ["_name"]

    def __init__(self, name: str):
        self._name = name

    @property
    def created(self):
        return datetime.strptime(
            _get_messages("group", self._name)[1][29:],
            "%y.%j",
        ).date()

    @property
    def installation_data(self):
        value = _get_messages("group", self._name)[2]
        return None if value == "NO INSTALLATION DATA" else value

    @property
    def model_data_set(self):
        value = _get_messages("group", self._name)[3]
        return None if value == "NO MODEL DATA SET" else value

    @property
    def name(self):
        return _get_messages("group", self._name)[0][22:]

    @property
    def owner(self):
        return _get_messages("group", self._name)[1][34:46].strip()

    @property
    def subgroups(self):
        value = _get_messages("group", self._name)[-2]
        return None if value == "NO SUBGROUPS" else value

    @property
    def superior_group(self):
        return _get_messages("group", self._name)[1][15:28].strip()

    @property
    def users(self):
        value = _get_messages("group", self._name)[-1]
        return None if value == "NO USERS" else value


class _Omvs:
    __slots__ = ["_name"]

    def __init__(self, name: str):
        self._name = name

    @property
    def gid(self):
        return int(_get_messages("group", self._name, "omvs")[-1][5:])


class _Tso:
    pass
