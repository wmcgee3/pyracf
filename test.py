import json

import xmltodict

text = """<?xml version="1.0" encoding="IBM-1047"?>
<securityresult xmlns="http://www.ibm.com/systems/zos/saf/IRRSMO00Result1">
  <resource name="TESTING" class="ELIJTEST" operation="listdata" requestid="ResourceRequest">
    <command>
      <safreturncode>0</safreturncode>
      <returncode>0</returncode>
      <reasoncode>0</reasoncode>
      <image>RLIST   ELIJTEST             (TESTING) </image>
      <message>CLASS      NAME</message>
      <message>-----      ----</message>
      <message>ELIJTEST   TESTING</message>
      <message> </message>
      <message>LEVEL  OWNER      UNIVERSAL ACCESS  YOUR ACCESS  WARNING</message>
      <message>-----  --------   ----------------  -----------  -------</message>
      <message> 00    ESWIFT          READ               READ    NO</message>
      <message> </message>
      <message>INSTALLATION DATA</message>
      <message>-----------------</message>
      <message>NONE</message>
      <message> </message>
      <message>APPLICATION DATA</message>
      <message>----------------</message>
      <message>NONE</message>
      <message> </message>
      <message>AUDITING</message>
      <message>--------</message>
      <message>FAILURES(READ)</message>
      <message> </message>
      <message>NOTIFY</message>
      <message>------</message>
      <message>NO USER TO BE NOTIFIED</message>
    </command>
  </resource>
  <returncode>0</returncode>
  <reasoncode>0</reasoncode>
</securityresult>
"""

print(json.dumps(xmltodict.parse(text), indent=4))
