import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))


class MockHTTPResponse:
    def __init__(self, payload, status=200, headers=None):
        self.status = status
        self.headers = headers or {}
        self._payload = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def mock_urlopen(req, timeout=None):
    if isinstance(req, MagicMock):
        url = ""
    else:
        url = req.full_url if hasattr(req, "full_url") else ""
    if "/company?q=" in url and "start_index=0" in url:
        return MockHTTPResponse({
            "items": [
                {"company_name": "Acme Ltd", "registered_office_address": {"address_line_1": "1 High St", "postal_code": "AB1 1AB", "locality": "Town"}, "sic_industry_description": "Retail", "company_number": "12345678"},
                {"company_name": "Beta Ltd", "registered_office_address": {"address_line_1": "2 Low St", "postal_code": "CD2 2CD", "locality": "City"}, "sic_codes": ["62020"], "company_number": "87654321"},
            ],
            "total_results": 2,
            "items_per_page": 100,
        })
    if "/company?q=" in url:
        return MockHTTPResponse({"items": [], "total_results": 0, "items_per_page": 100})
    if "/company/12345678/officers" in url:
        return MockHTTPResponse({
            "items": [
                {"name": "Alice Smith", "officer_role": "director"},
                {"name": "Bob Jones", "officer_role": "secretary"},
            ]
        })
    if "/company/87654321/officers" in url:
        return MockHTTPResponse({"items": []})
    if "/company/12345678" in url:
        return MockHTTPResponse({
            "company_name": "Acme Ltd",
            "registered_office_address": {"address_line_1": "1 High St", "postal_code": "AB1 1AB", "locality": "Town"},
            "type": "ltd",
        })
    return MockHTTPResponse({}, status=404)


class TestCompaniesHouseConnector(unittest.TestCase):
    def setUp(self):
        with patch("scraper.connectors.companies_house.config") as mock_config, \
             patch("scraper.connectors.companies_house.time") as mock_time:
            mock_config.COMPANIES_HOUSE_API_KEY = "test-key"
            mock_config.COMPANIES_HOUSE_RATE_LIMIT = 0
            mock_config.REQUEST_TIMEOUT = 10
            mock_time.monotonic.return_value = 0.0
            from scraper.connectors.companies_house import CompaniesHouseConnector
            self.connector = CompaniesHouseConnector.__new__(CompaniesHouseConnector)
            self.connector._api_key = mock_config.COMPANIES_HOUSE_API_KEY
            self.connector._rate_limit = mock_config.COMPANIES_HOUSE_RATE_LIMIT
            self.connector._timeout = mock_config.REQUEST_TIMEOUT
            self.connector._last_request_time = 0.0

    @patch("scraper.connectors.companies_house.urlopen", side_effect=mock_urlopen)
    def test_search_by_company_name(self, mock_urlopen_fn):
        results = self.connector.search_by_company_name("Acme")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["company_name"], "Acme Ltd")

    @patch("scraper.connectors.companies_house.urlopen", side_effect=mock_urlopen)
    def test_search_by_postcode(self, mock_urlopen_fn):
        results = self.connector.search_by_postcode("AB1 1AB")
        self.assertEqual(len(results), 2)

    def test_search_empty_name(self):
        results = self.connector.search_by_company_name("")
        self.assertEqual(results, [])

    def test_search_empty_postcode(self):
        results = self.connector.search_by_postcode("")
        self.assertEqual(results, [])

    @patch("scraper.connectors.companies_house.urlopen", side_effect=mock_urlopen)
    def test_get_company_details(self, mock_urlopen_fn):
        details = self.connector.get_company_details("12345678")
        self.assertEqual(details["company_name"], "Acme Ltd")

    def test_get_company_details_empty(self):
        details = self.connector.get_company_details("")
        self.assertIsNone(details)

    @patch("scraper.connectors.companies_house.urlopen", side_effect=mock_urlopen)
    def test_get_officers(self, mock_urlopen_fn):
        officers = self.connector.get_officers("12345678")
        self.assertEqual(len(officers), 2)
        self.assertEqual(officers[0]["name"], "Alice Smith")

    def test_get_officers_empty_company_number(self):
        officers = self.connector.get_officers("")
        self.assertEqual(officers, [])

    @patch("scraper.connectors.companies_house.urlopen", side_effect=mock_urlopen)
    def test_get_officers_no_officers(self, mock_urlopen_fn):
        officers = self.connector.get_officers("87654321")
        self.assertEqual(officers, [])

    @patch("scraper.connectors.companies_house.urlopen", side_effect=mock_urlopen)
    def test_map_to_profile(self, mock_urlopen_fn):
        item = {
            "company_name": "Acme Ltd",
            "registered_office_address": {
                "address_line_1": "1 High St",
                "postal_code": "AB1 1AB",
                "locality": "Town",
            },
            "sic_industry_description": "Retail",
            "company_number": "12345678",
        }
        profile = self.connector.map_to_profile(item)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.company_name, "Acme Ltd")
        self.assertEqual(profile.address, "1 High St, Town, AB1 1AB")
        self.assertEqual(profile.postcode, "AB1 1AB")
        self.assertEqual(profile.town, "Town")
        self.assertEqual(profile.business_type, "Retail")
        self.assertEqual(profile.main_contact, "Alice Smith")
        self.assertEqual(profile.source, "companies_house")

    def test_map_to_profile_no_name(self):
        item = {"company_name": "", "registered_office_address": {}}
        profile = self.connector.map_to_profile(item)
        self.assertIsNone(profile)

    def test_map_to_profile_none_item(self):
        profile = self.connector.map_to_profile(None)
        self.assertIsNone(profile)

    def test_map_to_profile_sic_codes_fallback(self):
        item = {
            "company_name": "Tech Ltd",
            "registered_office_address": {"address_line_1": "1 Tech St", "postal_code": "AB1 1AB"},
            "sic_codes": ["62020", "62030"],
            "company_number": "111",
        }
        profile = self.connector.map_to_profile(item)
        self.assertEqual(profile.business_type, "62020, 62030")

    def test_map_to_profile_type_fallback(self):
        item = {
            "company_name": "Charity",
            "registered_office_address": {"address_line_1": "1 Charity St", "postal_code": "AB1 1AB"},
            "type": "other",
            "company_number": "222",
        }
        profile = self.connector.map_to_profile(item)
        self.assertEqual(profile.business_type, "other")

    @patch("scraper.connectors.companies_house.urlopen", side_effect=mock_urlopen)
    def test_map_to_profile_confidence(self, mock_urlopen_fn):
        item = {
            "company_name": "Acme",
            "registered_office_address": {"address_line_1": "1 High St", "postal_code": "AB1 1AB", "locality": "Town"},
            "sic_industry_description": "Retail",
            "company_number": "12345678",
        }
        profile = self.connector.map_to_profile(item)
        self.assertEqual(profile.confidence, 1.0)

    def test_format_address_string(self):
        result = self.connector._format_address("123 Main St")
        self.assertEqual(result, "123 Main St")

    def test_format_address_dict(self):
        addr = {"address_line_1": "1 High St", "locality": "Town", "postal_code": "AB1 1AB"}
        result = self.connector._format_address(addr)
        self.assertIn("1 High St", result)
        self.assertIn("Town", result)
        self.assertIn("AB1 1AB", result)

    def test_format_address_none(self):
        result = self.connector._format_address(None)
        self.assertEqual(result, "")

    def test_extract_postcode_from_dict(self):
        addr = {"postal_code": "AB1 1AB", "registered_office_postcode": "CD2 2CD"}
        result = self.connector._extract_postcode(addr)
        self.assertEqual(result, "AB1 1AB")

    def test_extract_postcode_from_string(self):
        result = self.connector._extract_postcode("1 High St, Town, AB1 1AB")
        self.assertEqual(result, "AB1 1AB")

    def test_extract_town_from_dict(self):
        addr = {"locality": "Town", "registered_office_town": "Other Town"}
        result = self.connector._extract_town(addr)
        self.assertEqual(result, "Town")

    def test_extract_town_from_string(self):
        result = self.connector._extract_town("1 High St, Town")
        self.assertEqual(result, "1 High St")

    def test_resolve_address_fields(self):
        item = {
            "registered_office_address": {"address_line_1": "1 High St", "postal_code": "AB1 1AB", "locality": "Town"},
            "registered_office_postcode": "CD2 2CD",
            "registered_office_town": "Other Town",
        }
        addr, postcode, town = self.connector._resolve_address_fields(item)
        self.assertEqual(postcode, "CD2 2CD")
        self.assertEqual(town, "Other Town")
        self.assertIn("1 High St", addr)

    @patch("scraper.connectors.companies_house.urlopen", side_effect=mock_urlopen)
    def test_search_by_postcode_mapped(self, mock_urlopen_fn):
        profiles = self.connector.search_by_postcode_mapped("AB1 1AB")
        self.assertEqual(len(profiles), 2)

    @patch("scraper.connectors.companies_house.urlopen", side_effect=mock_urlopen)
    def test_search_by_company_name_mapped(self, mock_urlopen_fn):
        profiles = self.connector.search_by_company_name_mapped("Acme")
        self.assertEqual(len(profiles), 2)

    def test_rate_limit_wait_zero(self):
        with patch("scraper.connectors.companies_house.time") as mock_time:
            mock_time.monotonic.return_value = 0.0
            from scraper.connectors.companies_house import CompaniesHouseConnector
            connector = CompaniesHouseConnector.__new__(CompaniesHouseConnector)
            connector._api_key = "test"
            connector._rate_limit = 0
            connector._timeout = 10
            connector._last_request_time = 0.0
            connector._rate_limit_wait()
