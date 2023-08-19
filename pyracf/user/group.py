from datetime import datetime


class UserGroup:
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
