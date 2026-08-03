import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from scraper.models.company import CompanyProfile


def _mock_response(json_data, status=200):
    mock = MagicMock()
    mock.status_code = status
    mock.json.return_value = json_data
    mock.raise_for_status.return_value = None
    mock.text = json.dumps(json_data)
    return mock


class TestGooglePlacesHelpers(unittest.TestCase):
    def setUp(self):
        from scraper.connectors.google_places import _extract_address_component, _parse_opening_hours, _place_to_company_profile, FALLBACK_CONFIDENCE
        self._extract_address_component = _extract_address_component
        self._parse_opening_hours = _parse_opening_hours
        self._place_to_company_profile = _place_to_company_profile
        self.FALLBACK_CONFIDENCE = FALLBACK_CONFIDENCE

    def test_extract_address_component(self):
        components = [
            {"types": ["postal_code"], "long_name": "AB1 1AB", "short_name": "AB1 1AB"},
            {"types": ["locality"], "long_name": "Town", "short_name": "Town"},
        ]
        self.assertEqual(self._extract_address_component(components, "postal_code"), "AB1 1AB")
        self.assertEqual(self._extract_address_component(components, "locality"), "Town")
        self.assertIsNone(self._extract_address_component(components, "country"))

    def test_parse_opening_hours(self):
        place = {
            "opening_hours": {
                "weekday_text": ["Monday: 9:00 AM - 5:00 PM", "Tuesday: Closed"]
            }
        }
        result = self._parse_opening_hours(place)
        self.assertIsNotNone(result)
        self.assertEqual(result["monday"], "Monday: 9:00 AM - 5:00 PM")
        self.assertEqual(result["tuesday"], "Tuesday: Closed")

    def test_parse_opening_hours_no_hours(self):
        self.assertIsNone(self._parse_opening_hours({}))
        self.assertIsNone(self._parse_opening_hours({"opening_hours": {}}))

    def test_place_to_company_profile(self):
        place = {
            "name": "Acme Shop",
            "vicinity": "1 High St",
            "formatted_address": "1 High St, Town, AB1 1AB",
            "address_components": [
                {"types": ["postal_code"], "long_name": "AB1 1AB"},
                {"types": ["locality"], "long_name": "Town"},
            ],
            "types": ["store"],
            "details": {
                "formatted_phone_number": "01234 567890",
                "website": "https://acme.com",
                "opening_hours": {"weekday_text": ["Mon-Fri 9-5"]},
            },
        }
        profile = self._place_to_company_profile(place)
        self.assertEqual(profile.company_name, "Acme Shop")
        self.assertEqual(profile.address, "1 High St, Town, AB1 1AB")
        self.assertEqual(profile.postcode, "AB1 1AB")
        self.assertEqual(profile.town, "Town")
        self.assertEqual(profile.telephone, "01234 567890")
        self.assertEqual(profile.business_type, "Store")
        self.assertEqual(profile.source, "google_places")
        self.assertEqual(profile.confidence, self.FALLBACK_CONFIDENCE)
        self.assertIsNotNone(profile.open_hours)

    def test_place_to_company_profile_no_details(self):
        place = {
            "name": "Acme Shop",
            "vicinity": "1 High St",
            "address_components": [
                {"types": ["postal_code"], "long_name": "AB1 1AB"},
            ],
            "types": ["store"],
        }
        profile = self._place_to_company_profile(place)
        self.assertIsNone(profile.telephone)
        self.assertIsNone(profile.email)
        self.assertIsNone(profile.open_hours)

    def test_place_to_company_profile_postal_town(self):
        place = {
            "name": "Shop",
            "vicinity": "1 High St",
            "address_components": [
                {"types": ["postal_town"], "long_name": "Chelmsford"},
            ],
            "types": ["store"],
        }
        profile = self._place_to_company_profile(place)
        self.assertEqual(profile.town, "Chelmsford")

    def test_place_to_company_profile_main_contact_from_phone(self):
        place = {
            "name": "Shop",
            "vicinity": "1 High St",
            "address_components": [],
            "types": ["store"],
            "details": {"formatted_phone_number": "01234 567890"},
        }
        profile = self._place_to_company_profile(place)
        self.assertEqual(profile.main_contact, "01234 567890")


class TestGooglePlacesSearch(unittest.TestCase):
    def setUp(self):
        from scraper.connectors.google_places import search_by_location, place_details, enrich_company_profile, _place_to_company_profile, FALLBACK_CONFIDENCE
        self.search_by_location = search_by_location
        self.place_details = place_details
        self.enrich_company_profile = enrich_company_profile
        self.FALLBACK_CONFIDENCE = FALLBACK_CONFIDENCE

    def _make_place(self, name, address="1 High St, Town, AB1 1AB", phone=None, types=None):
        components = []
        if "AB1" in address:
            components.append({"types": ["postal_code"], "long_name": "AB1 1AB"})
        if "Town" in address:
            components.append({"types": ["locality"], "long_name": "Town"})
        details = {}
        if phone:
            details["formatted_phone_number"] = phone
        return {
            "name": name,
            "vicinity": address,
            "formatted_address": address,
            "address_components": components,
            "types": types or ["store"],
            "place_id": f"place_{name.lower().replace(' ', '_')}",
            **({"details": details} if details else {}),
        }

    def _make_profile_from_place(self, place):
        from scraper.connectors.google_places import _place_to_company_profile
        return _place_to_company_profile(place)

    @patch("scraper.connectors.google_places._request_with_retry")
    @patch("scraper.connectors.google_places.config")
    def test_search_by_location_no_api_key(self, mock_config, mock_request):
        mock_config.GOOGLE_PLACES_API_KEY = ""
        results = self.search_by_location(51.0, 0.0, 10.0, "test")
        self.assertEqual(results, [])
        mock_request.assert_not_called()

    @patch("scraper.connectors.google_places._request_with_retry")
    @patch("scraper.connectors.google_places.config")
    def test_search_by_location_text_search(self, mock_config, mock_request):
        mock_config.GOOGLE_PLACES_API_KEY = "test-key"
        mock_config.REQUEST_TIMEOUT = 30
        place = self._make_place("Acme Shop")
        mock_request.return_value = {"results": [place], "status": "OK"}
        results = self.search_by_location(51.0, 0.0, 10.0, "Acme Shop")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].company_name, "Acme Shop")

    @patch("scraper.connectors.google_places._request_with_retry")
    @patch("scraper.connectors.google_places.config")
    def test_search_by_location_deduplication(self, mock_config, mock_request):
        mock_config.GOOGLE_PLACES_API_KEY = "test-key"
        mock_config.REQUEST_TIMEOUT = 30
        place1 = self._make_place("Acme Shop")
        place2 = self._make_place("Acme Shop")
        mock_request.return_value = {"results": [place1, place2], "status": "OK"}
        results = self.search_by_location(51.0, 0.0, 10.0, "Acme Shop")
        self.assertEqual(len(results), 1)

    @patch("scraper.connectors.google_places._request_with_retry")
    @patch("scraper.connectors.google_places.config")
    def test_search_by_location_fallback_nearby(self, mock_config, mock_request):
        mock_config.GOOGLE_PLACES_API_KEY = "test-key"
        mock_config.REQUEST_TIMEOUT = 30
        place = self._make_place("Shop")
        mock_request.return_value = {"results": [place], "status": "OK"}
        results = self.search_by_location(51.0, 0.0, 10.0, "query")
        self.assertEqual(len(results), 1)

    @patch("scraper.connectors.google_places._request_with_retry")
    @patch("scraper.connectors.google_places.config")
    def test_search_by_location_zero_results(self, mock_config, mock_request):
        mock_config.GOOGLE_PLACES_API_KEY = "test-key"
        mock_config.REQUEST_TIMEOUT = 30
        mock_request.return_value = {"results": [], "status": "ZERO_RESULTS"}
        results = self.search_by_location(51.0, 0.0, 10.0, "query")
        self.assertEqual(results, [])

    @patch("scraper.connectors.google_places._request_with_retry")
    @patch("scraper.connectors.google_places.config")
    def test_place_details(self, mock_config, mock_request):
        mock_config.GOOGLE_PLACES_API_KEY = "test-key"
        mock_config.REQUEST_TIMEOUT = 30
        mock_request.return_value = {
            "result": self._make_place("Acme", phone="01234 567890"),
            "status": "OK",
        }
        profile = self.place_details("place_acme")
        self.assertIsNotNone(profile)
        self.assertEqual(profile.company_name, "Acme")
        self.assertEqual(profile.confidence, 0.8)

    @patch("scraper.connectors.google_places._request_with_retry")
    @patch("scraper.connectors.google_places.config")
    def test_place_details_no_result(self, mock_config, mock_request):
        mock_config.GOOGLE_PLACES_API_KEY = "test-key"
        mock_request.return_value = {"result": {}, "status": "OK"}
        profile = self.place_details("place_unknown")
        self.assertIsNone(profile)

    @patch("scraper.connectors.google_places.config")
    def test_place_details_no_api_key(self, mock_config):
        mock_config.GOOGLE_PLACES_API_KEY = ""
        profile = self.place_details("place_abc")
        self.assertIsNone(profile)

    @patch("scraper.connectors.google_places.search_by_location")
    @patch("scraper.connectors.google_places.config")
    def test_enrich_company_profile(self, mock_config, mock_search):
        mock_config.GOOGLE_PLACES_API_KEY = "test-key"
        profile = CompanyProfile(
            company_name="Acme Ltd",
            telephone=None,
            email=None,
            address="",
            main_contact=None,
            business_type=None,
            open_hours=None,
            postcode="",
            town="",
            source="companies_house",
            confidence=0.5,
        )
        enriched = self._make_profile_from_place(self._make_place("Acme Ltd", phone="01234 567890"))
        mock_search.return_value = [enriched]
        result = self.enrich_company_profile(profile, lat=51.0, lng=0.0)
        self.assertEqual(result.telephone, "01234 567890")
        self.assertEqual(result.source, "google_places")
        self.assertAlmostEqual(result.confidence, 0.6)

    @patch("scraper.connectors.google_places.config")
    def test_enrich_company_profile_no_api_key(self, mock_config):
        mock_config.GOOGLE_PLACES_API_KEY = ""
        profile = CompanyProfile(
            company_name="Acme", telephone=None, email=None, address="", main_contact=None,
            business_type=None, open_hours=None, postcode="", town="", source="companies_house", confidence=0.5,
        )
        result = self.enrich_company_profile(profile)
        self.assertEqual(result.telephone, None)
        self.assertEqual(result.source, "companies_house")

    @patch("scraper.connectors.google_places.search_by_location")
    @patch("scraper.connectors.google_places.config")
    def test_enrich_preserves_existing_fields(self, mock_config, mock_search):
        mock_config.GOOGLE_PLACES_API_KEY = "test-key"
        profile = CompanyProfile(
            company_name="Acme", telephone="existing", email="a@b.com", address="existing addr",
            main_contact="existing", business_type="existing", open_hours=None, postcode="AB1", town="Town",
            source="companies_house", confidence=0.7,
        )
        enriched = self._make_profile_from_place(self._make_place("Acme", phone="new_phone"))
        mock_search.return_value = [enriched]
        result = self.enrich_company_profile(profile)
        self.assertEqual(result.telephone, "existing")
        self.assertEqual(result.address, "existing addr")


class TestRateLimiter(unittest.TestCase):
    def setUp(self):
        from scraper.connectors.google_places import RateLimiter
        self.RateLimiter = RateLimiter

    def test_rate_limiter_basic(self):
        limiter = self.RateLimiter(max_requests=2, period=60.0)
        limiter.wait()
        limiter.wait()
        self.assertEqual(len(limiter._timestamps), 2)
