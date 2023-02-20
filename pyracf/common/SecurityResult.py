import defusedxml.ElementTree as XMLParser


class SecurityResult:
    def __init__(self, result_xml: str) -> None:
        self.result = XMLParser.fromstring(result_xml)
        self.result_dictionary = {"securityresult": {}}
        self.__extract_results()

    def __extract_results(self) -> None:
        self.definition = self.result[0]
        definition_tag = self.definition.tag.split("}")[-1]
        self.result_dictionary["securityresult"][
            definition_tag
        ] = self.definition.attrib
        self.definition_dictionary = self.result_dictionary["securityresult"][
            definition_tag
        ]
        if self.definition[0].tag.split("}")[-1] == "info":
            self.__extract_info()
        if self.definition[0].tag.split("}")[-1] == "error":
            self.__extract_error()
        else:
            self.__extract_commands()
        return_code = self.result[1]
        self.result_dictionary["securityresult"]["returncode"] = int(return_code.text)
        reason_code = self.result[1]
        self.result_dictionary["securityresult"]["reasoncode"] = int(reason_code.text)

    def __extract_info(self) -> None:
        self.definition_dictionary["info"] = []
        info = self.definition_dictionary["info"]
        while self.definition[0].tag.split("}")[-1] == "info":
            item = self.definition[0]
            if item.tag.split("}")[-1] != "info":
                return
            info.append(item.text)
            self.definition.remove(item)

    def __extract_commands(self) -> None:
        self.definition_dictionary["commands"] = []
        commands = self.definition_dictionary["commands"]
        for command in self.definition:
            command_dictionary = {}
            commands.append(command_dictionary)
            for item in command:
                item_tag = item.tag.split("}")[-1]
                if item_tag == "message":
                    if "messages" not in command_dictionary:
                        command_dictionary["messages"] = []
                    command_dictionary["messages"].append(item.text)
                try:
                    command_dictionary[item_tag] = int(item.text)
                except ValueError:
                    command_dictionary[item_tag] = item.text

    def __extract_error(self) -> None:
        self.definition_dictionary["error"] = {}
        error = self.definition[0]
        for item in error:
            item_tag = item.tag.split("}")[-1]
            try:
                self.definition_dictionary["error"][item_tag] = int(item.text)
            except ValueError:
                self.definition_dictionary["error"][item_tag] = item.text

    def get_result_dictionary(self) -> dict:
        return self.result_dictionary
