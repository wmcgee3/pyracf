"""Test user result parser."""

import unittest
from unittest.mock import Mock, patch

import __init__

import tests.user.test_user_constants as TestUserConstants
from pyracf import SecurityRequestError, UserAdmin
from pyracf.irrsmo00 import IRRSMO00

# Resolves F401
__init__


@patch("pyracf.common.irrsmo00.IRRSMO00.call_racf")
class TestUserResultParser(unittest.TestCase):
    maxDiff = None
    IRRSMO00.__init__ = Mock(return_value=None)
    user_admin = UserAdmin()
    test_password = "GIyTTqdF"
    test_passphrase = "PassPhrasesAreCool!"

    # ============================================================================
    # Add User
    # ============================================================================
    def test_user_admin_can_parse_add_user_success_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = TestUserConstants.TEST_ADD_USER_RESULT_SUCCESS_XML
        self.assertEqual(
            self.user_admin.add(
                "squidwrd",
                traits=TestUserConstants.TEST_ADD_USER_REQUEST_TRAITS,
            ),
            TestUserConstants.TEST_ADD_USER_RESULT_SUCCESS_DICTIONARY,
        )

    # Error in environment, SQUIDWRD already added/exists
    def test_user_admin_can_parse_add_user_error_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = TestUserConstants.TEST_ADD_USER_RESULT_ERROR_XML
        with self.assertRaises(SecurityRequestError) as exception:
            self.user_admin.add(
                "squidwrd",
                traits=TestUserConstants.TEST_ADD_USER_REQUEST_TRAITS,
            )
        self.assertEqual(
            exception.exception.result,
            TestUserConstants.TEST_ADD_USER_RESULT_ERROR_DICTIONARY,
        )

    # ============================================================================
    # Alter User
    # ============================================================================
    def test_user_admin_can_parse_alter_user_success_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_ALTER_USER_RESULT_SUCCESS_XML
        )
        self.assertEqual(
            self.user_admin.alter(
                "squidwrd", traits=TestUserConstants.TEST_ALTER_USER_REQUEST_TRAITS
            ),
            TestUserConstants.TEST_ALTER_USER_RESULT_SUCCESS_DICTIONARY,
        )

    # Error: invalid parameter "name"
    def test_user_admin_can_parse_alter_user_error_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = TestUserConstants.TEST_ALTER_USER_RESULT_ERROR_XML
        with self.assertRaises(SecurityRequestError) as exception:
            self.user_admin.alter(
                "squidwrd", traits=TestUserConstants.TEST_ADD_USER_REQUEST_TRAITS
            )
        self.assertEqual(
            exception.exception.result,
            TestUserConstants.TEST_ALTER_USER_RESULT_ERROR_DICTIONARY,
        )

    # ============================================================================
    # Extract User
    # ============================================================================
    def test_user_admin_can_parse_extract_user_base_omvs_success_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_EXTRACT_USER_RESULT_BASE_OMVS_SUCCESS_XML
        )
        self.assertEqual(
            self.user_admin.extract("squidwrd", segments={"omvs": True}),
            TestUserConstants.TEST_EXTRACT_USER_RESULT_BASE_OMVS_SUCCESS_DICTIONARY,
        )

    def test_user_admin_can_parse_extract_user_base_only_no_omvs_success_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_EXTRACT_USER_RESULT_BASE_ONLY_NO_OMVS_SUCCESS_XML
        )
        self.assertEqual(
            self.user_admin.extract("squidwrd", segments={"omvs": True}),
            TestUserConstants.TEST_EXTRACT_USER_RESULT_BASE_ONLY_NO_OMVS_SUCCESS_JSON,
        )

    # Error in environment, SQUIDWRD already deleted/not added
    def test_user_admin_can_parse_extract_user_base_omvs_error_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_EXTRACT_USER_RESULT_BASE_OMVS_ERROR_XML
        )
        with self.assertRaises(SecurityRequestError) as exception:
            self.user_admin.extract("squidwrd", segments={"omvs": True})
        self.assertEqual(
            exception.exception.result,
            TestUserConstants.TEST_EXTRACT_USER_RESULT_BASE_OMVS_ERROR_DICTIONARY,
        )

    def test_user_admin_can_parse_extract_user_and_ignore_command_audit_trail_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_EXTRACT_USER_RESULT_WITH_COMMAND_AUDIT_TRAIL_XML
        )
        self.assertEqual(
            self.user_admin.extract("squidwrd", segments={"omvs": True}),
            TestUserConstants.TEST_EXTRACT_USER_RESULT_BASE_OMVS_SUCCESS_DICTIONARY,
        )

    # ============================================================================
    # Password and Password Phrase Redaction
    # ============================================================================
    def test_user_admin_password_redacted_add_user_success_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_ADD_USER_PASSWORD_RESULT_SUCCESS_XML
        )
        result = self.user_admin.add(
            "squidwrd",
            traits=TestUserConstants.TEST_ADD_USER_REQUEST_TRAITS_PASSWORD,
        )
        self.assertEqual(
            result,
            TestUserConstants.TEST_ADD_USER_PASSWORD_RESULT_SUCCESS_DICTIONARY,
        )
        self.assertNotIn(self.test_password, str(result))

    # Error in environment, SQUIDWRD already added/exists
    def test_user_admin_password_redacted_add_user_error_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_ADD_USER_PASSWORD_RESULT_ERROR_XML
        )
        with self.assertRaises(SecurityRequestError) as exception:
            self.user_admin.add(
                "squidwrd",
                traits=TestUserConstants.TEST_ADD_USER_REQUEST_TRAITS_PASSWORD,
            )
        self.assertEqual(
            exception.exception.result,
            TestUserConstants.TEST_ADD_USER_PASSWORD_RESULT_ERROR_DICTIONARY,
        )
        self.assertNotIn(self.test_password, str(exception.exception.result))

    def test_user_admin_passphrase_redacted_add_user_success_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_ADD_USER_PASSPHRASE_RESULT_SUCCESS_XML
        )
        result = self.user_admin.add(
            "squidwrd",
            traits=TestUserConstants.TEST_ADD_USER_REQUEST_TRAITS_PASSPHRASE,
        )
        self.assertEqual(
            result,
            TestUserConstants.TEST_ADD_USER_PASSPHRASE_RESULT_SUCCESS_DICTIONARY,
        )
        self.assertNotIn(self.test_passphrase, str(result))

    # Error in environment, SQUIDWRD already added/exists
    def test_user_admin_passphrase_redacted_add_user_error_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_ADD_USER_PASSPHRASE_RESULT_ERROR_XML
        )
        with self.assertRaises(SecurityRequestError) as exception:
            self.user_admin.add(
                "squidwrd",
                traits=TestUserConstants.TEST_ADD_USER_REQUEST_TRAITS_PASSPHRASE,
            )
        self.assertEqual(
            exception.exception.result,
            TestUserConstants.TEST_ADD_USER_PASSPHRASE_RESULT_ERROR_DICTIONARY,
        )
        self.assertNotIn(self.test_passphrase, str(exception.exception.result))

    def test_user_admin_passphrase_and_password_redacted_add_user_success_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_ADD_USER_PASSPHRASE_AND_PASSWORD_RESULT_SUCCESS_XML
        )
        result = self.user_admin.add(
            "squidwrd",
            traits=TestUserConstants.TEST_ADD_USER_REQUEST_TRAITS_PASSPHRASE_AND_PASSWORD,
        )
        self.assertEqual(
            result,
            TestUserConstants.TEST_ADD_USER_PASSPHRASE_AND_PASSWORD_RESULT_SUCCESS_DICTIONARY,
        )
        self.assertNotIn(self.test_passphrase, str(result))
        self.assertNotIn(self.test_password, str(result))

    # Error in environment, SQUIDWRD already added/exists
    def test_user_admin_passphrase_and_password_redacted_add_user_error_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_ADD_USER_PASSPHRASE_AND_PASSWORD_RESULT_ERROR_XML
        )
        with self.assertRaises(SecurityRequestError) as exception:
            self.user_admin.add(
                "squidwrd",
                traits=TestUserConstants.TEST_ADD_USER_REQUEST_TRAITS_PASSPHRASE_AND_PASSWORD,
            )
        self.assertEqual(
            exception.exception.result,
            TestUserConstants.TEST_ADD_USER_PASSPHRASE_AND_PASSWORD_RESULT_ERROR_DICTIONARY,
        )
        self.assertNotIn(self.test_passphrase, str(exception.exception.result))
        self.assertNotIn(self.test_password, str(exception.exception.result))

    # ============================================================================
    # Delete User
    # ============================================================================
    def test_user_admin_can_parse_delete_user_success_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_DELETE_USER_RESULT_SUCCESS_XML
        )
        self.assertEqual(
            self.user_admin.delete("squidwrd"),
            TestUserConstants.TEST_DELETE_USER_RESULT_SUCCESS_DICTIONARY,
        )

    # Error in environment, SQUIDWRD already deleted/not added
    def test_user_admin_can_parse_delete_user_error_xml(
        self,
        call_racf_mock: Mock,
    ):
        call_racf_mock.return_value = (
            TestUserConstants.TEST_DELETE_USER_RESULT_ERROR_XML
        )
        with self.assertRaises(SecurityRequestError) as exception:
            self.user_admin.delete("squidwrd")
        self.assertEqual(
            exception.exception.result,
            TestUserConstants.TEST_DELETE_USER_RESULT_ERROR_DICTIONARY,
        )

    # ============================================================================
    # Extract User With Custom Field Data
    # ============================================================================
    def test_user_admin_can_parse_extract_user_base_omvs_csdata_success_xml(
        self,
        call_racf_mock: Mock,
    ):
        user_admin = UserAdmin(
            add_field_data=TestUserConstants.TEST_USER_UPDATE_SEGMENTS
        )
        call_racf_mock.return_value = (
            TestUserConstants.TEST_EXTRACT_USER_RESULT_BASE_OMVS_CSDATA_SUCCESS_XML
        )
        self.assertEqual(
            user_admin.extract("squidwrd", {"omvs": True, "csdata": True}),
            TestUserConstants.TEST_EXTRACT_USER_RESULT_BASE_OMVS_CSDATA_SUCCESS_DICTIONARY,
        )
