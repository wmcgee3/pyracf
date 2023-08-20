from datetime import datetime

from ._utils import _get_message_value, _get_messages

__all__ = ["RacfUser"]


class RacfUser:
    __slots__ = ["_name", "_omvs", "_tso"]

    def __init__(self, name: str):
        self._name = name
        self._omvs = None
        self._tso = None

    @property
    def attributes(self):
        return _get_messages("user", self._name)[2][11:]

    @property
    def category_authorization(self):
        return _get_messages("user", self._name)[-2]

    @property
    def class_authorizations(self):
        return _get_messages("user", self._name)[5][21:]

    @property
    def created(self):
        return datetime.strptime(
            _get_messages("user", self._name)[0][65:], "%y.%j"
        ).date()

    @property
    def default_group(self):
        return _get_messages("user", self._name)[1][14:23].strip()

    @property
    def groups(self):
        group_messages = _get_messages("user", self._name)[11:-12]
        return [
            _UserGroup(group_messages[i : i + 4])
            for i in range(0, len(group_messages), 4)
        ]

    @property
    def installation_data(self):
        return _get_messages("user", self._name)[6][18:]

    @property
    def last_access(self):
        return _get_messages("user", self._name)[4][12:]

    @property
    def logon_allowed_days(self):
        return _get_messages("user", self._name)[10][:32].strip()

    @property
    def logon_allowed_time(self):
        return _get_messages("user", self._name)[10][32:]

    @property
    def model_name(self):
        return _get_messages("user", self._name)[7]

    @property
    def name(self):
        return _get_messages("user", self._name)[0][19:41].strip()

    @property
    def omvs(self):
        if self._omvs is None:
            self._omvs = _Omvs(self._name)
        return self._omvs

    @property
    def owner(self):
        return _get_messages("user", self._name)[0][47:57].strip()

    @property
    def passphrase_date(self):
        try:
            return datetime.strptime(
                _get_messages("user", self._name)[1][68:], "%y.%j"
            ).date()
        except ValueError:
            return None

    @property
    def password_date(self):
        try:
            return datetime.strptime(
                _get_messages("user", self._name)[1][32:38], "%y.%j"
            ).date()
        except ValueError:
            return None

    @property
    def password_interval(self):
        try:
            return int(_get_messages("user", self._name)[1][53:57].strip())
        except ValueError:
            return None

    @property
    def resume_date(self):
        return _get_messages("user", self._name)[3][31:]

    @property
    def revoke_date(self):
        return _get_messages("user", self._name)[3][12:19].strip()

    @property
    def security_label(self):
        return _get_messages("user", self._name)[-1][15:]

    @property
    def security_level(self):
        return _get_messages("user", self._name)[-4][15:]

    @property
    def tso(self):
        if self._tso is None:
            self._tso = _Tso(self._name)
        return self._tso

    @property
    def user(self):
        return _get_messages("user", self._name)[0][5:14].strip()


class _UserGroup:
    __slots__ = [
        "auth",
        "connect_attributes",
        "connect_date",
        "connect_owner",
        "connects",
        "last_connect",
        "name",
        "resume_date",
        "revoke_date",
        "uacc",
    ]

    def __init__(self, messages: list[str]):
        line_1, line_2, line_3, line_4 = messages

        self.name = line_1[6:16].strip()
        self.auth = line_1[21:30].strip()
        self.connect_owner = line_1[44:54].strip()
        self.connect_date = datetime.strptime(line_1[67:].strip(), "%y.%j").date()

        self.connects = line_2[9:17].strip()
        self.uacc = line_2[22:31].strip()
        self.last_connect = line_2[44:].strip()

        self.connect_attributes = line_3[19:].strip()

        self.revoke_date = line_4[12:19].strip()
        self.resume_date = line_4[31:].strip()


class _Omvs:
    __slots__ = ["_name"]

    def __init__(self, name: str):
        self._name = name

    @property
    def home(self):
        return _get_message_value("user", self._name, "omvs", "HOME")

    @property
    def max_address_space_size(self):
        return self._get_max_value("ASSIZEMAX")

    @property
    def max_cpu_time(self):
        return self._get_max_value("CPUTIMEMAX")

    @property
    def max_mmap_area(self):
        return self._get_max_value("MMAPAREAMAX")

    @property
    def max_process_files(self):
        return self._get_max_value("FILEPROCMAX")

    @property
    def max_processes(self):
        return self._get_max_value("PROCUSERMAX")

    @property
    def max_threads(self):
        return self._get_max_value("THREADSMAX")

    @property
    def program(self):
        return _get_message_value("user", self._name, "omvs", "PROGRAM")

    @property
    def uid(self):
        return int(_get_message_value("user", self._name, "omvs", "UID"))

    def _get_max_value(self, key: str):
        value = _get_message_value("user", self._name, "omvs", key)
        return None if value == "NONE" else int(value)


class _Tso:
    __slots__ = ["_name"]

    def __init__(self, name: str):
        self._name = name

    @property
    def account_number(self):
        return _get_message_value("user", self._name, "tso", "ACCTNUM")

    @property
    def command(self):
        return _get_message_value("user", self._name, "tso", "COMMAND")

    @property
    def max_size(self):
        return int(_get_message_value("user", self._name, "tso", "MAXSIZE"))

    @property
    def proc(self):
        return _get_message_value("user", self._name, "tso", "PROC")

    @property
    def size(self):
        return int(_get_message_value("user", self._name, "tso", "SIZE"))

    @property
    def unit(self):
        return _get_message_value("user", self._name, "tso", "UNIT")

    @property
    def user_data(self):
        return _get_message_value("user", self._name, "tso", "USERDATA")
