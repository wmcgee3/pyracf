"""
Sample data for testing User Administration functions.
"""

from typing import Union

import tests.test_utilities as TestUtilities


def get_sample(sample_file: str) -> Union[str, bytes]:
    return TestUtilities.get_sample(sample_file, "user")


# ============================================================================
# User Administration Result Sample Data
# ============================================================================

# Add User
TEST_ADD_USER_RESULT_SUCCESS_XML = get_sample("add_user_result_success.xml")
TEST_ADD_USER_RESULT_SUCCESS_DICTIONARY = get_sample("add_user_result_success.json")
TEST_ADD_USER_RESULT_ERROR_XML = get_sample("add_user_result_error.xml")
TEST_ADD_USER_RESULT_ERROR_DICTIONARY = get_sample("add_user_result_error.json")

# Alter User
TEST_ALTER_USER_RESULT_SUCCESS_XML = get_sample("alter_user_result_success.xml")
TEST_ALTER_USER_RESULT_SUCCESS_DICTIONARY = get_sample("alter_user_result_success.json")
TEST_ALTER_USER_RESULT_ERROR_XML = get_sample("alter_user_result_error.xml")
TEST_ALTER_USER_RESULT_ERROR_DICTIONARY = get_sample("alter_user_result_error.json")

# Extract User
TEST_EXTRACT_USER_RESULT_BASE_OMVS_SUCCESS_XML = get_sample(
    "extract_user_result_base_omvs_success.xml"
)
TEST_EXTRACT_USER_RESULT_BASE_OMVS_SUCCESS_DICTIONARY = get_sample(
    "extract_user_result_base_omvs_success.json"
)
TEST_EXTRACT_USER_RESULT_BASE_OMVS_ERROR_XML = get_sample(
    "extract_user_result_base_omvs_error.xml"
)
TEST_EXTRACT_USER_RESULT_BASE_OMVS_ERROR_DICTIONARY = get_sample(
    "extract_user_result_base_omvs_error.json"
)
TEST_EXTRACT_USER_RESULT_BASE_ONLY_NO_OMVS_SUCCESS_XML = get_sample(
    "extract_user_result_base_only_no_omvs_success.xml"
)
TEST_EXTRACT_USER_RESULT_BASE_ONLY_NO_OMVS_SUCCESS_JSON = get_sample(
    "extract_user_result_base_only_no_omvs_success.json"
)
TEST_EXTRACT_USER_RESULT_WITH_CLASS_AUTHORIZATIONS = get_sample(
    "extract_user_result_with_class_authorizations.xml"
)
TEST_EXTRACT_USER_RESULT_WITH_COMMAND_AUDIT_TRAIL_XML = get_sample(
    "extract_user_result_with_command_audit_trail.xml"
)

# Delete User
TEST_DELETE_USER_RESULT_SUCCESS_XML = get_sample("delete_user_result_success.xml")
TEST_DELETE_USER_RESULT_SUCCESS_DICTIONARY = get_sample(
    "delete_user_result_success.json"
)
TEST_DELETE_USER_RESULT_ERROR_XML = get_sample("delete_user_result_error.xml")
TEST_DELETE_USER_RESULT_ERROR_DICTIONARY = get_sample("delete_user_result_error.json")

# ============================================================================
# User Administration Request Sample Data
# ============================================================================

# Add User
TEST_ADD_USER_REQUEST_XML = get_sample("add_user_request.xml")
TEST_ADD_USER_REQUEST_TRAITS = {
    "base:name": "Squidward",
    "base:password": "GIyTTqdF",
    "base:owner": "leonard",
    "base:special": True,
    "base:operator": False,
    "omvs:uid": "2424",
    "omvs:home": "/u/squidwrd",
    "omvs:program": "/bin/sh",
}

# Alter User
TEST_ALTER_USER_REQUEST_XML = get_sample("alter_user_request.xml")
TEST_ALTER_USER_REQUEST_TRAITS = {
    "base:special": False,
    "base:operator": True,
    "omvs:home": "/u/clarinet",
    "omvs:program": False,
}

# Extract User
TEST_EXTRACT_USER_REQUEST_BASE_OMVS_XML = get_sample(
    "extract_user_request_base_omvs.xml"
)
TEST_EXTRACT_USER_REQUEST_BASE_OMVS_TRAITS = {
    "omvs": True,
    "mfa": False,
}

# Delete User
TEST_DELETE_USER_REQUEST_XML = get_sample("delete_user_request.xml")

# ============================================================================
# User Administration Setters Sample Data
# ============================================================================

TEST_USER_GIVE_SPECIAL_AUTHORITY_XML = get_sample(
    "user_give_special_authority_request.xml"
)
TEST_USER_REMOVE_SPECIAL_AUTHORITY_XML = get_sample(
    "user_remove_special_authority_request.xml"
)
TEST_USER_GIVE_AUDITOR_AUTHORITY_XML = get_sample(
    "user_give_auditor_authority_request.xml"
)
TEST_USER_REMOVE_AUDITOR_AUTHORITY_XML = get_sample(
    "user_remove_auditory_authority_request.xml"
)
TEST_USER_GIVE_OPERATIONS_AUTHORITY_XML = get_sample(
    "user_give_operations_authority_request.xml"
)
TEST_USER_REMOVE_OPERATIONS_AUTHORITY_XML = get_sample(
    "user_remove_operations_authority_request.xml"
)
TEST_USER_SET_PASSWORD_XML = get_sample("user_set_password_request.xml")
TEST_USER_ADD_CLASS_AUTHORIZATIONS_SINGLE_CLASS_XML = get_sample(
    "user_add_class_authorizations_single_class_request.xml"
)
TEST_USER_ADD_CLASS_AUTHORIZATIONS_MULTIPLE_CLASSES_XML = get_sample(
    "user_add_class_authorizations_multiple_classes_request.xml"
)
TEST_USER_REMOVE_CLASS_AUTHORIZATIONS_SINGLE_CLASS_XML = get_sample(
    "user_remove_class_authorizations_single_class_request.xml"
)
TEST_USER_REMOVE_CLASS_AUTHORIZATIONS_MULTIPLE_CLASSES_XML = get_sample(
    "user_remove_class_authorizations_multiple_classes_request.xml"
)
TEST_USER_DELETE_ALL_CLASS_AUTHORIZATIONS_XML = get_sample(
    "user_delete_all_class_authorizations_request.xml"
)
TEST_USER_SET_CLASS_AUTHORIZATIONS_XML = get_sample(
    "user_set_class_authorizations_request.xml"
)
TEST_USER_SET_OMVS_UID_XML = get_sample("user_set_omvs_uid_request.xml")
TEST_USER_SET_OMVS_HOME_XML = get_sample("user_set_omvs_home_request.xml")

# ============================================================================
# Debug Logging
# ============================================================================

TEST_ADD_USER_SUCCESS_LOG = get_sample("add_user_success.log")
TEST_ADD_USER_ERROR_LOG = get_sample("add_user_error.log")

TEST_EXTRACT_USER_BASE_OMVS_SUCCESS_LOG = get_sample(
    "extract_user_base_omvs_success.log"
)
TEST_EXTRACT_USER_BASE_OMVS_ERROR_LOG = get_sample("extract_user_base_omvs_error.log")
