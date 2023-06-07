"""Base Class for RACF Administration Interface."""

import json
from typing import List, Tuple, Union

from .irrsmo00 import IRRSMO00
from .logger import Logger
from .security_request import SecurityRequest
from .security_request_error import SecurityRequestError
from .security_result import SecurityResult


class SecurityAdmin:
    """Base Class for RACF Administration Interface."""

    def __init__(
        self,
        profile_type: str,
        debug: bool = False,
        generate_requests_only: bool = False,
    ) -> None:
        self.__irrsmo00 = IRRSMO00()
        self._valid_segment_traits = {}
        self._common_base_traits_dataset_generic = {
            "aclcnt": "racf:aclcnt",
            "aclacnt": "racf:aclacnt",
            "aclacs": "racf:aclacs",
            "aclid": "racf:aclid",
            "acl2cnt": "racf:acl2cnt",
            "acl2acnt": "racf:acl2acnt",
            "acl2acs": "racf:acl2acs",
            "acl2cond": "racf:acl2cond",
            "acl2ent": "racf:acl2ent",
            "acl2id": "racf:acl2id",
            "acsaltr": "racf:acsaltr",
            "acscntl": "racf:acscntl",
            "acsread": "racf:acsread",
            "acsupdt": "racf:acsupdt",
            "all": "racf:all",
            "audaltr": "racf:audaltr",
            "audcntl": "racf:audcntl",
            "audnone": "racf:audnone",
            "audread": "racf:audread",
            "audupdt": "racf:audupdt",
            "authuser": "racf:authuser",
            "fvolume": "racf:fvolume",
            "gaudaltr": "racf:gaudaltr",
            "gaudcntl": "racf:gaudcntl",
            "gaudnone": "racf:gaudnone",
            "gaudread": "racf:gaudread",
            "gaudupdt": "racf:gaudupdt",
            "generic": "racf:generic",
        }
        self._segment_traits = {}
        # used to preserve segment traits for debug logging.
        self.__preserved_segment_traits = {}
        self._trait_map = {}
        self.__profile_type = profile_type
        self.__logger = Logger()
        self.__debug = debug
        self.__generate_requests_only = generate_requests_only

    def _extract_and_check_result(self, security_request: SecurityRequest) -> dict:
        """Extract a RACF profile."""
        result = self._make_request(security_request)
        if self.__generate_requests_only:
            return result
        if "error" in result["securityresult"][self.__profile_type]:
            raise SecurityRequestError(result)
        if (
            result["securityresult"]["returncode"] == 0
            and result["securityresult"]["reasoncode"] == 0
        ):
            self._format_profile(result)
            if self.__debug:
                self.__logger.log_dictionary(
                    "Result Dictionary (Formatted Profile)", result, None
                )
            return result
        raise SecurityRequestError(result)

    def _build_bool_segment_dictionaries(self, segments: dict) -> None:
        """Build segment dictionaries for profile extract."""
        for segment in segments:
            if segment in self._valid_segment_traits:
                self._segment_traits[segment] = segments[segment]
        # preserve segment traits for debug logging.
        self.__preserved_segment_traits = self._segment_traits

    def _make_request(
        self,
        security_request: SecurityRequest,
        irrsmo00_options: int = 1,
    ) -> Union[dict, bytes]:
        """Make request to IRRSMO00."""
        try:
            redact_password = self.__preserved_segment_traits["base"]["base:password"][
                "value"
            ]
        except KeyError:
            redact_password = None
        result = self.__make_request_unredacted(
            security_request,
            irrsmo00_options=irrsmo00_options,
            redact_password=redact_password,
        )
        if not redact_password:
            return result
        if isinstance(result, dict):
            # Dump to json string, redact password, and then load back to dictionary.
            return json.loads(
                self.__logger.redact_string(json.dumps(result), redact_password)
            )
        # redact password from XML bytes (Always UTF-8).
        return self.__logger.redact_string(result, bytes(redact_password, "utf-8"))

    def __make_request_unredacted(
        self,
        security_request: SecurityRequest,
        irrsmo00_options: int = 1,
        redact_password: str = None,
    ) -> Union[dict, bytes]:
        """
        Make request to IRRSMO00.
        Note: Passwords are not redacted from result, but are redacted from log messages.
        """
        if self.__debug:
            self.__logger.log_dictionary(
                "Request Dictionary", self.__preserved_segment_traits, redact_password
            )
            self.__logger.log_xml(
                "Request XML",
                security_request.dump_request_xml(encoding="utf-8"),
                redact_password,
            )
        if self.__generate_requests_only:
            return security_request.dump_request_xml(encoding="utf-8")
        result_xml = self.__irrsmo00.call_racf(
            security_request.dump_request_xml(), irrsmo00_options
        )
        if self.__debug:
            self.__logger.log_xml("Result XML", result_xml, redact_password)
        results = SecurityResult(result_xml)

        if self.__debug:
            self.__logger.log_dictionary(
                "Result Dictionary",
                results.get_result_dictionary(),
                redact_password,
            )
        result_dict = results.get_result_dictionary()
        if (
            result_dict["securityresult"]["returncode"] != 0
            or result_dict["securityresult"]["reasoncode"] != 0
        ):
            raise SecurityRequestError(result_dict)
        return result_dict

    def _format_profile(self, result: dict):
        """Placeholder for format profile function for profile extract."""

    def _format_profile_generic(self, messages: str) -> None:
        """Generic profile formatter shared by two or more RACF profile formats."""
        profile = {}
        current_segment = "base"
        (
            additional_segment_keys,
            no_segment_information_keys,
        ) = self.__build_additional_segment_keys()
        profile[current_segment] = {}
        i = 0
        while i < len(messages):
            if (
                messages[i] == " "
                or messages[i] in no_segment_information_keys
                or messages[i] is None
            ):
                i += 1
                continue
            if i < len(messages) - 1 and messages[i] in additional_segment_keys:
                current_segment = messages[i].split()[0].lower()
                profile[current_segment] = {}
                i += 2
            if self.__profile_type in ("dataset", "resource"):
                i = self.__format_data_set_generic_profile_data(
                    messages, profile, current_segment, i
                )
            if self.__profile_type == "user":
                i = self.__format_user_profile_data(
                    messages, profile, current_segment, i
                )
            if self.__profile_type == "group":
                i = self.__format_group_profile_data(
                    messages, profile, current_segment, i
                )
            i += 1
        return profile

    def __format_data_set_generic_profile_data(
        self, messages: List[str], profile: dict, current_segment: str, i: int
    ) -> int:
        """Specialized logic for formatting DataSet/General Resource profile data."""
        if "=" in messages[i]:
            self.__add_key_value_pair_to_profile(
                messages[i],
                profile,
                current_segment,
            )
        elif (
            i < len(messages) - 2
            and ("  " in messages[i])
            and ("--" in messages[i + 1])
        ):
            self.__format_semi_tabular_data(messages, profile, current_segment, i)
            i += 2
        elif (
            i < len(messages) - 2
            and messages[i + 1] is not None
            and ("-" in messages[i + 1])
        ):
            field = " ".join(
                [
                    txt.lower().strip()
                    for txt in list(filter(None, messages[i].split(" ")))
                ]
            )
            profile[current_segment][field] = self._clean_and_separate(messages[i + 2])
            i += 1
        elif "NO INSTALLATION DATA" in messages[i]:
            profile[current_segment]["installation data"] = None
        if "INFORMATION FOR DATASET" in messages[i]:
            profile[current_segment]["name"] = (
                messages[i].split("INFORMATION FOR DATASET ")[1].lower()
            )
        return i

    def __format_user_profile_data(
        self, messages: List[str], profile: dict, current_segment: str, i: int
    ) -> int:
        """Specialized logic for formatting user profile data."""
        if (
            i < len(messages) - 1
            and messages[i + 1] == " ---------------------------------------------"
        ):
            semi_tabular_data = messages[i : i + 3]
            self.__add_semi_tabular_data_to_segment(
                profile[current_segment], semi_tabular_data
            )
            i += 2
        elif messages[i][:8] == "  GROUP=":
            if "groups" not in profile[current_segment]:
                profile[current_segment]["groups"] = {}
            group = messages[i].split("=")[1].split()[0]
            profile[current_segment]["groups"][group] = {}
            message = messages[i] + messages[i + 1] + messages[i + 2] + messages[i + 3]
            self.__add_key_value_pairs_to_segment(
                profile[current_segment]["groups"][group], message[17:]
            )
            i += 3
        elif "=" not in messages[i] and messages[i].strip()[:3] != "NO-":
            messages[i] = f"{messages[i]}={messages[i+1]}"
            self.__add_key_value_pairs_to_segment(profile[current_segment], messages[i])
            i += 1
        else:
            self.__add_key_value_pairs_to_segment(profile[current_segment], messages[i])
        return i

    def __format_group_profile_data(
        self, messages: List[str], profile: dict, current_segment: str, i: int
    ) -> int:
        """Specialized logic for formatting user profile data."""
        if "users" in profile[current_segment].keys() and i < len(messages) - 2:
            self.__format_user_list_data(messages, profile, current_segment, i)
            i += 2
        if (
            "USER(S)=      ACCESS=      ACCESS COUNT=      UNIVERSAL ACCESS="
            in messages[i]
        ):
            profile[current_segment]["users"] = []
        elif "=" in messages[i]:
            self.__add_key_value_pairs_to_segment(profile[current_segment], messages[i])
        elif "NO " in messages[i]:
            field_name = messages[i].split("NO ")[1].strip().lower()
            profile[current_segment][field_name] = None
        elif "TERMUACC" in messages[i]:
            if "NO" in messages[i]:
                profile[current_segment]["termuacc"] = False
            else:
                profile[current_segment]["termuacc"] = True
        elif "INFORMATION FOR GROUP" in messages[i]:
            profile[current_segment]["name"] = (
                messages[i].split("INFORMATION FOR GROUP ")[1].lower()
            )
        return i

    def __format_user_list_data(
        self, messages: list, profile: dict, current_segment: str, i: int
    ) -> None:
        profile[current_segment]["users"].append({})
        user_index = len(profile[current_segment]["users"]) - 1
        user_fields = [
            field.strip() for field in messages[i].split(" ") if field.strip()
        ]

        profile[current_segment]["users"][user_index]["userid"] = self._cast_from_str(
            user_fields[0]
        )
        profile[current_segment]["users"][user_index]["access"] = self._cast_from_str(
            user_fields[1]
        )
        profile[current_segment]["users"][user_index][
            "access count"
        ] = self._cast_from_str(user_fields[2])
        profile[current_segment]["users"][user_index][
            "universal access"
        ] = self._cast_from_str(user_fields[3])

        self.__add_key_value_pairs_to_segment(
            profile[current_segment]["users"][user_index], messages[i + 1]
        )

        self.__add_key_value_pairs_to_segment(
            profile[current_segment]["users"][user_index], messages[i + 2]
        )

    def __build_additional_segment_keys(self) -> Tuple[str, str]:
        """Build keys for detecting additional segments in RACF profile data."""
        additional_segment_keys = [
            f"{segment.upper()} INFORMATION"
            for segment in self._valid_segment_traits
            if segment != "base"
        ]
        no_segment_information_keys = [
            f"NO {segment}" for segment in additional_segment_keys
        ]
        return (additional_segment_keys, no_segment_information_keys)

    def __add_semi_tabular_data_to_segment(
        self, segment: dict, semi_tabular_data: List[str]
    ) -> None:
        """Add semi-tabular data as key-value pairs to segment dictionary."""
        heading_tokens = list(filter(("").__ne__, semi_tabular_data[0].split("  ")))
        key_prefix = heading_tokens[0]
        keys = [f"{key_prefix}{key.strip()[1:-1]}" for key in heading_tokens[1:]]
        values = semi_tabular_data[-1].split()
        keys_length = len(keys)
        for i in range(keys_length):
            key = keys[i].strip().lower().replace(" ", "").replace("-", "")
            segment[key] = self._cast_from_str(values[i])

    def __format_semi_tabular_data(
        self,
        messages: List[str],
        profile: dict,
        current_segment: str,
        i: int,
    ) -> None:
        """Generic function for parsing semitabular data from RACF profile data."""
        tmp_ind = [j for j in range(len(messages[i + 1])) if messages[i + 1][j] == "-"]
        indexes = [
            tmp_ind[j]
            for j in range(len(tmp_ind))
            if j == 0 or tmp_ind[j] - tmp_ind[j - 1] > 1
        ]
        indexes_length = len(indexes)
        for j in range(indexes_length):
            if j < indexes_length - 1:
                ind_e0 = indexes[j + 1] - 1
                ind_e1 = indexes[j + 1] - 1
            else:
                ind_e0 = len(messages[i])
                ind_e1 = len(messages[i + 2])

            field = messages[i][indexes[j] : ind_e0].strip().lower()
            profile[current_segment][field] = self._clean_and_separate(
                messages[i + 2][indexes[j] : ind_e1]
            )

    def __add_key_value_pairs_to_segment(
        self,
        segment: dict,
        message: str,
    ) -> None:
        """Add a key value pair to a segment dictionary."""
        list_fields = ["attributes", "classauthorizations"]
        tokens = message.strip().split("=")
        key = tokens[0]
        for i in range(1, len(tokens)):
            sub_tokens = list(filter(("").__ne__, tokens[i].split("  ")))
            value = sub_tokens[0].strip()
            if key[:3] == "NO-":
                key = key[3:]
                value = "N/A"
            current_key = key.strip().lower().replace(" ", "").replace("-", "")
            if current_key in list_fields:
                if current_key not in segment:
                    segment[current_key] = []
                values = [
                    self._cast_from_str(value)
                    for value in value.split()
                    if value != "NONE"
                ]
                segment[current_key] += values
            else:
                segment[current_key] = self._cast_from_str(value)
            key = "".join(sub_tokens[1:])
            if len(sub_tokens) == 1:
                if i < len(tokens) - 1 and " " in sub_tokens[0] and i != 0:
                    sub_tokens = sub_tokens[0].split()
                    segment[current_key] = self._cast_from_str(sub_tokens[0])
                    key = sub_tokens[-1]
                else:
                    key = sub_tokens[0]

    def __add_key_value_pair_to_profile(
        self, message: str, profile: dict, current_segment: str
    ) -> None:
        """Generic function for extracting key-value pair from RACF profile data."""
        field = message.split("=")[0].strip().lower()
        profile[current_segment][field] = self._clean_and_separate(
            message.split("=")[1]
        )

    def _clean_and_separate(self, value: str) -> Union[list, str]:
        """Clean cast and separate comma and space delimited data."""
        cln_val = value.strip().lower()
        if "," in cln_val:
            out = [self._cast_from_str(val.strip()) for val in cln_val.split(",")]
        elif " " in cln_val:
            out = [self._cast_from_str(val.strip()) for val in cln_val.split(" ")]
        else:
            out = self._cast_from_str(cln_val)
        if isinstance(out, list):
            if None in out:
                return None
            open_ind = []
            close_ind = []
            cln_ind = []
            for i, val in enumerate(out):
                if "(" in val and ")" not in val:
                    open_ind.append(i)
                if ")" in val and "(" not in val:
                    close_ind.append(i)
            if not open_ind and not close_ind:
                return out
            for i, ind in enumerate(open_ind):
                out[ind] = " ".join(out[ind : (close_ind[i] + 1)])
                cln_ind = cln_ind + [*range(ind, close_ind[i] + 1)][1:]
            cln_ind.reverse()
            for i in cln_ind:
                del out[i]

        return out

    def _cast_from_str(self, value: str) -> Union[None, bool, int, float, str]:
        """Cast null values floats and integers."""
        value = value.lower()
        if value in ("n/a", "none", "none specified", "no", "None"):
            return None
        if value in (
            "in effect",
            "active",
            "active.",
            "being done.",
            "in effect.",
            "allowed.",
            "being done",
        ):
            return True
        if value in ("not in effect", "inactive", "not allowed.", "not being done"):
            return False
        if "days" in value and any(chr.isdigit() for chr in value):
            digits = "".join([chr for chr in value if chr.isdigit()])
            return int(digits)
        if "in effect for the " in value and " function." in value:
            return value.split("in effect for the ")[1].split(" function.")[0]
        return self.__cast_num(value)

    def __cast_num(self, value: str) -> Union[int, float, str]:
        if "." in value:
            try:
                return float(value)
            except ValueError:
                return value
        try:
            return int(value.replace(",", ""))
        except ValueError:
            return value

    def __validate_and_add_trait(
        self, trait: str, segment: str, value: Union[str, dict]
    ):
        """Validate the specified trait exists in the specified segment"""
        if segment not in self._valid_segment_traits:
            return False
        if trait not in self._valid_segment_traits[segment]:
            tokens = trait.split(":")
            operation = tokens[0]
            if operation not in ["add", "remove", "delete"] or len(tokens) == 1:
                return False
            trait = trait[len(operation) + 1 :]
            if trait not in self._valid_segment_traits[segment]:
                return False
            value_operation_dictionary = {"value": value, "operation": operation}
        else:
            operation = None
            if isinstance(value, bool) and not value:
                operation = "delete"
            value_operation_dictionary = {"value": value, "operation": operation}
        if segment not in self._segment_traits:
            self._segment_traits[segment] = {}
        self._segment_traits[segment][trait] = value_operation_dictionary
        self._trait_map[trait] = self._valid_segment_traits[segment][trait]
        return True

    def _build_segment_dictionaries(self, traits: dict) -> None:
        """Build segemnt dictionaries for each segment."""
        for trait in traits:
            for segment in self._valid_segment_traits:
                self.__validate_and_add_trait(trait, segment, traits[trait])
        # preserve segment traits for debug logging.
        self.__preserved_segment_traits = self._segment_traits

    def _build_xml_segments(
        self,
        security_request: SecurityRequest,
        alter: bool = False,
        extract: bool = True,
    ) -> None:
        """Build XML representation of segments."""
        security_request._build_segments(
            self._segment_traits, self._trait_map, alter=alter, extract=extract
        )
        # Clear segments for new request
        self._segment_traits = {}

    def _add_traits_directly_to_request_xml_with_no_segments(
        self, security_request: SecurityRequest, alter: bool = False
    ) -> None:
        """Add traits as directly to request xml without building segments."""
        for segment, traits in self._segment_traits.items():
            if segment == "base":
                security_request._build_segment(
                    None, traits, self._trait_map, alter=alter
                )
        # Clear segments for new request
        self._segment_traits = {}

    def _to_steps(self, results: Union[List[dict], dict, bytes]) -> dict:
        """
        Build a steps dictionary composed of each result dictionary
        in a result dictionary list, where the result dictionary list is
        assumed to be ordered chronologically in ascending order with respect
        to when each corresponding request was made.

        Note: for generate request only mode (for testing purposes),
        the all of the request xml bytes should just be concatenated together.
        """
        if isinstance(results, dict):
            results = [results]
        if self.__generate_requests_only:
            return results
        results = [result for result in results if result]
        steps_dictionary = {}
        for step, result_dictionary in enumerate(results):
            steps_dictionary[f"step{step+1}"] = result_dictionary
        return steps_dictionary
