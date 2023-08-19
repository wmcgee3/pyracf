from datetime import datetime

from ..utils import get_messages
from .group import UserGroup
from .omvs import Omvs
from .tso import Tso


class RacfUser:
    __slots__ = ["_name", "_omvs", "_tso"]

    def __init__(self, name: str):
        self._name = name
        self._omvs = None
        self._tso = None

    @property
    def attributes(self):
        return get_messages(self._name)[2][11:]

    @property
    def category_authorization(self):
        return get_messages(self._name)[-2]

    @property
    def class_authorizations(self):
        return get_messages(self._name)[5][21:]

    @property
    def created(self):
        return datetime.strptime(get_messages(self._name)[0][65:], "%y.%j").date()

    @property
    def default_group(self):
        return get_messages(self._name)[1][14:23].strip()

    @property
    def groups(self):
        group_messages = get_messages(self._name)[11:-12]
        return [
            UserGroup(group_messages[i : i + 4])
            for i in range(0, len(group_messages), 4)
        ]

    @property
    def installation_data(self):
        return get_messages(self._name)[6][18:]

    @property
    def last_access(self):
        return get_messages(self._name)[4][12:]

    @property
    def logon_allowed_days(self):
        return get_messages(self._name)[10][:32].strip()

    @property
    def logon_allowed_time(self):
        return get_messages(self._name)[10][32:]

    @property
    def model_name(self):
        return get_messages(self._name)[7]

    @property
    def name(self):
        return get_messages(self._name)[0][19:41].strip()

    @property
    def omvs(self):
        if self._omvs is None:
            self._omvs = Omvs(self._name)
        return self._omvs

    @property
    def owner(self):
        return get_messages(self._name)[0][47:57].strip()

    @property
    def passphrase_date(self):
        try:
            return datetime.strptime(get_messages(self._name)[1][68:], "%y.%j").date()
        except ValueError:
            return None

    @property
    def password_date(self):
        try:
            return datetime.strptime(get_messages(self._name)[1][32:38], "%y.%j").date()
        except ValueError:
            return None

    @property
    def password_interval(self):
        try:
            return int(get_messages(self._name)[1][53:57].strip())
        except ValueError:
            return None

    @property
    def resume_date(self):
        return get_messages(self._name)[3][31:]

    @property
    def revoke_date(self):
        return get_messages(self._name)[3][12:19].strip()

    @property
    def security_label(self):
        return get_messages(self._name)[-1][15:]

    @property
    def security_level(self):
        return get_messages(self._name)[-4][15:]

    @property
    def tso(self):
        if self._tso is None:
            self._tso = Tso(self._name)
        return self._tso

    @property
    def user(self):
        return get_messages(self._name)[0][5:14].strip()
