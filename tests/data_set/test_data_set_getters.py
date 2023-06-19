"""Test data set profile getter functions."""

import unittest
from unittest.mock import Mock, patch

import __init__

import tests.data_set.test_data_set_constants as TestDataSetConstants
from pyracf import DataSetAdmin
from pyracf.common.security_request_error import SecurityRequestError

# Resolves F401
__init__


@patch("pyracf.common.irrsmo00.IRRSMO00.call_racf")
@patch("pyracf.common.irrsmo00.IRRSMO00.__init__")
class TestDataSetGetters(unittest.TestCase):
    maxDiff = None

    def boilerplate(self, irrsmo00_init_mock: Mock) -> DataSetAdmin:
        irrsmo00_init_mock.return_value = None
        return DataSetAdmin()

    # ============================================================================
    # Access
    # ============================================================================
    def test_data_set_admin_get_universal_access_returns_valid_when_read(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        data_set_admin = self.boilerplate(irrsmo00_init_mock)
        call_racf_mock.return_value = (
            TestDataSetConstants.TEST_EXTRACT_DATA_SET_RESULT_BASE_SUCCESS_XML
        )
        self.assertTrue(
            data_set_admin.get_universal_access("ESWIFT.TEST.T1136242.P3020470").title()
            == "Read"
        )

    def test_data_set_admin_get_universal_access_returns_valid_when_none(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        data_set_admin = self.boilerplate(irrsmo00_init_mock)
        data_set_extract_no_universal_access = (
            TestDataSetConstants.TEST_EXTRACT_DATA_SET_RESULT_BASE_SUCCESS_XML
        )
        data_set_extract_no_universal_access = (
            data_set_extract_no_universal_access.replace(
                "<message> 00    ESWIFT          READ          NO      NO</message>",
                "<message> 00    ESWIFT          NONE          NO      NO</message>",
            )
        )
        call_racf_mock.return_value = data_set_extract_no_universal_access
        self.assertTrue(
            data_set_admin.get_universal_access("ESWIFT.TEST.T1136242.P3020470") is None
        )

    # Error in environment, ESWIFT.TEST.T1136242.P3020470 already deleted/not added
    def test_data_set_admin_get_universal_access_raises_an_exception_when_extract_fails(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        data_set_admin = self.boilerplate(irrsmo00_init_mock)
        call_racf_mock.return_value = (
            TestDataSetConstants.TEST_EXTRACT_DATA_SET_RESULT_BASE_ERROR_XML
        )
        with self.assertRaises(SecurityRequestError):
            data_set_admin.get_universal_access("ESWIFT.TEST.T1136242.P3020470")

    def test_data_set_admin_get_my_access_returns_valid_when_alter(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        data_set_admin = self.boilerplate(irrsmo00_init_mock)
        call_racf_mock.return_value = (
            TestDataSetConstants.TEST_EXTRACT_DATA_SET_RESULT_BASE_SUCCESS_XML
        )
        self.assertTrue(
            data_set_admin.get_my_access("ESWIFT.TEST.T1136242.P3020470").title()
            == "Alter"
        )

    def test_data_set_admin_get_my_access_returns_valid_when_none(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        data_set_admin = self.boilerplate(irrsmo00_init_mock)
        data_set_extract_no_my_access = (
            TestDataSetConstants.TEST_EXTRACT_DATA_SET_RESULT_BASE_SUCCESS_XML
        )
        data_set_extract_no_my_access = data_set_extract_no_my_access.replace(
            "<message> ALTER        SYS1           NON-VSAM</message>",
            "<message> NONE         SYS1           NON-VSAM</message>",
        )
        call_racf_mock.return_value = data_set_extract_no_my_access
        self.assertTrue(
            data_set_admin.get_my_access("ESWIFT.TEST.T1136242.P3020470") is None
        )

    # Error in environment, ESWIFT.TEST.T1136242.P3020470 already deleted/not added
    def test_data_set_admin_get_my_access_raises_an_exception_when_extract_fails(
        self,
        irrsmo00_init_mock: Mock,
        call_racf_mock: Mock,
    ):
        data_set_admin = self.boilerplate(irrsmo00_init_mock)
        call_racf_mock.return_value = (
            TestDataSetConstants.TEST_EXTRACT_DATA_SET_RESULT_BASE_ERROR_XML
        )
        with self.assertRaises(SecurityRequestError):
            data_set_admin.get_my_access("ESWIFT.TEST.T1136242.P3020470")
