from ..utils import get_message_value


class Omvs:
    __slots__ = ["_name"]

    def __init__(self, name: str):
        self._name = name

    @property
    def home(self):
        return get_message_value(self._name, "omvs", "HOME")

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
        return get_message_value(self._name, "omvs", "PROGRAM")

    @property
    def uid(self):
        return int(get_message_value(self._name, "omvs", "UID"))

    def _get_max_value(self, key: str):
        value = get_message_value(self._name, "omvs", key)
        return None if value == "NONE" else int(value)
