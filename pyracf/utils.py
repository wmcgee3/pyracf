import platform

import xmltodict

from .models import _Response

if platform.system() == "OS/390":
    from cpyracf import call_irrsmo00
else:
    # Ignore import of extension on non-z/OS platforms to allow for unit testing off platform.
    def call_irrsmo00(*, xml_str, xml_len, opts):
        _ = xml_str, xml_len, opts
        return b""


def get_message_value(name: str, segment: str, key: str):
    messages = get_messages(name, segment)
    return next(
        (
            line[len(key) + 2 :]
            for line in reversed(messages)
            if line is not None and line.startswith(f"{key}=")
        )
    )


def get_messages(name: str, segment: str | None = None):
    request_xml = (
        "<?xml version='1.0' encoding='cp1047'?>"
        + "<securityrequest xmlns='http://www.ibm.com/systems/zos/saf' xmlns:racf='http://www.ibm.com/systems/zos/racf'>"
        + f"<user name='{name}' operation='listdata' requestid='UserRequest'>"
        + (f"<{segment} />" if segment is not None else "")
        + "</user>"
        + "</securityrequest>"
    ).encode("cp1047")
    response_text = call_irrsmo00(
        xml_str=request_xml,
        xml_len=len(request_xml),
        opts=1,
    ).decode("cp1047")
    return _Response(
        **xmltodict.parse(response_text)
    ).security_result.user.command.message
