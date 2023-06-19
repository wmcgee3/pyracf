"""Test access result parser."""

import unittest
from unittest.mock import Mock, patch

import __init__

import tests.access.test_access_constants as TestAccessConstants
from pyracf import AccessAdmin
from pyracf.common.security_request_error import SecurityRequestError

# Resolves F401
__init__


@patch("pyracf.common.irrsmo00.IRRSMO00.call_racf")
@patch("pyracf.common.irrsmo00.IRRSMO00.__init__")
class TestAccessResultParser(unittest.TestCase):
    maxDiff = None

    def boilerplate(self, irrsmo00_init_mock: Mock) -> AccessAdmin:
        irrsmo00_init_mock.return_value = None
        return AccessAdmin()

    # ============================================================================
    # Add Access
    # ============================================================================
    def test_access_admin_can_parse_add_access_success_xml(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        access_admin = self.boilerplate(irrsmo00_init_mock)
        call_racf_mock.return_value = (
            TestAccessConstants.TEST_ADD_ACCESS_RESULT_SUCCESS_XML
        )
        self.assertEqual(
            access_admin.add("TESTING", "ELIJTEST", "ESWIFT", {"base:access": "READ"}),
            TestAccessConstants.TEST_ADD_ACCESS_RESULT_SUCCESS_DICTIONARY,
        )

    # Error in environment, TESTING resource already deleted/not added
    def test_access_admin_can_parse_add_access_error_xml(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        access_admin = self.boilerplate(irrsmo00_init_mock)
        call_racf_mock.return_value = (
            TestAccessConstants.TEST_ADD_ACCESS_RESULT_ERROR_XML
        )
        with self.assertRaises(SecurityRequestError) as exception:
            access_admin.add("TESTING", "ELIJTEST", "ESWIFT", {"base:access": "READ"})
        self.assertEqual(
            exception.exception.results,
            TestAccessConstants.TEST_ADD_ACCESS_RESULT_ERROR_DICTIONARY,
        )

    # ============================================================================
    # Alter Access
    # ============================================================================
    def test_access_admin_can_parse_alter_access_success_xml(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        access_admin = self.boilerplate(irrsmo00_init_mock)
        call_racf_mock.return_value = (
            TestAccessConstants.TEST_ALTER_ACCESS_RESULT_SUCCESS_XML
        )
        self.assertEqual(
            access_admin.alter("TESTING", "ELITEST", "ESWIFT", {"base:access": "NONE"}),
            TestAccessConstants.TEST_ALTER_ACCESS_RESULT_SUCCESS_DICTIONARY,
        )

    # Error, UserID MCGINLEY not defined to RACF
    def test_access_admin_can_parse_alter_access_error_xml(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        access_admin = self.boilerplate(irrsmo00_init_mock)
        call_racf_mock.return_value = (
            TestAccessConstants.TEST_ALTER_ACCESS_RESULT_ERROR_XML
        )
        with self.assertRaises(SecurityRequestError) as exception:
            access_admin.alter(
                "TESTING", "ELITEST", "MCGINLEY", {"base:access": "NONE"}
            )
        self.assertEqual(
            exception.exception.results,
            TestAccessConstants.TEST_ALTER_ACCESS_RESULT_ERROR_DICTIONARY,
        )

    # ============================================================================
    # Delete Access
    # ============================================================================
    def test_access_admin_can_parse_delete_access_success_xml(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        access_admin = self.boilerplate(irrsmo00_init_mock)
        call_racf_mock.return_value = (
            TestAccessConstants.TEST_DELETE_ACCESS_RESULT_SUCCESS_XML
        )
        self.assertEqual(
            access_admin.delete("TESTING", "ELIJTEST", "ESWIFT"),
            TestAccessConstants.TEST_DELETE_ACCESS_RESULT_SUCCESS_DICTIONARY,
        )

    # Error User not authorized, delete ignored
    def test_access_admin_can_parse_delete_access_error_xml(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        access_admin = self.boilerplate(irrsmo00_init_mock)
        call_racf_mock.return_value = (
            TestAccessConstants.TEST_DELETE_ACCESS_RESULT_ERROR_XML
        )
        with self.assertRaises(SecurityRequestError) as exception:
            access_admin.delete("TESTING", "ELIJTEST", "ESWIFT")
        self.assertEqual(
            exception.exception.results,
            TestAccessConstants.TEST_DELETE_ACCESS_RESULT_ERROR_DICTIONARY,
        )
