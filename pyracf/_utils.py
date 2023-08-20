import platform
from typing import Optional

import xmltodict

from ._models import _Response

if platform.system() == "OS/390":
    from cpyracf import call_irrsmo00
else:
    # Ignore import of extension on non-z/OS platforms to allow for unit testing off platform.
    def call_irrsmo00(*, xml_str: bytes, xml_len: int, opts: int) -> bytes:
        _ = xml_str, xml_len, opts
        return "".encode()


def _get_message_value(resource: str, name: str, segment: str, key: str):
    messages = _get_messages(resource, name, segment)
    return next(
        (
            line[len(key) + 2 :]
            for line in reversed(messages)
            if line is not None and line.startswith(f"{key}=")
        )
    )


def _get_messages(resource: str, name: str, segment: Optional[str] = None):
    request_xml = (
        "<?xml version='1.0' encoding='cp1047'?>"
        + "<securityrequest xmlns='http://www.ibm.com/systems/zos/saf' xmlns:racf='http://www.ibm.com/systems/zos/racf'>"
        + f"<{resource} name='{name}' operation='listdata' requestid='{resource.capitalize()}Request'>"
        + (f"<{segment} />" if segment is not None else "")
        + f"</{resource}>"
        + "</securityrequest>"
    ).encode("cp1047")
    response_text = call_irrsmo00(
        xml_str=request_xml,
        xml_len=len(request_xml),
        opts=1,
    ).decode("cp1047")
    response = _Response(**xmltodict.parse(response_text))
    return response.security_result.user.command.messages
