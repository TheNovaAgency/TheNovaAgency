import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))


def make_profile(name, postcode, town="", source="companies_house", confidence=0.8, telephone=None, email=None, address="", main_contact=None, business_type=None, open_hours=None):
    from scraper.models.company import CompanyProfile
    return CompanyProfile(
        company_name=name,
        telephone=telephone,
        email=email,
        address=address,
        main_contact=main_contact,
        business_type=business_type,
        open_hours=open_hours,
        postcode=postcode,
        town=town,
        source=source,
        confidence=confidence,
    )


class TestScraperOrchestratorDeduplication(unittest.TestCase):
    def setUp(self):
        from scraper.orchestrator.scraper import ScraperOrchestrator
        self.orchestrator = ScraperOrchestrator.__new__(ScraperOrchestrator)

    def test_deduplicate_unique_profiles(self):
        profiles = [
            make_profile("Acme", "AB1 1AB", source="companies_house"),
            make_profile("Beta", "CD2 2CD", source="google_places"),
        ]
        result = self.orchestrator._deduplicate_and_merge(profiles, MagicMock())
        self.assertEqual(len(result), 2)

    def test_deduplicate_same_name_same_postcode(self):
        profiles = [
            make_profile("Acme Ltd", "AB1 1AB", source="companies_house", confidence=0.7),
            make_profile("Acme Ltd", "AB1 1AB", source="google_places", confidence=0.9),
        ]
        result = self.orchestrator._deduplicate_and_merge(profiles, MagicMock())
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].company_name, "Acme Ltd")
        self.assertEqual(result[0].source, "companies_house,google_places")

    def test_deduplicate_case_insensitive(self):
        profiles = [
            make_profile("Acme Ltd", "AB1 1AB", source="companies_house"),
            make_profile("acme ltd", "ab1 1ab", source="google_places"),
        ]
        result = self.orchestrator._deduplicate_and_merge(profiles, MagicMock())
        self.assertEqual(len(result), 1)

    def test_merge_preserves_best_fields(self):
        profiles = [
            make_profile("Acme", "AB1 1AB", source="companies_house", telephone="111", address="Addr CH", business_type=None),
            make_profile("Acme", "AB1 1AB", source="google_places", telephone=None, address="Addr GP", business_type="Tech"),
        ]
        result = self.orchestrator._deduplicate_and_merge(profiles, MagicMock())
        merged = result[0]
        self.assertEqual(merged.telephone, "111")
        self.assertEqual(merged.address, "Addr CH")
        self.assertEqual(merged.business_type, "Tech")

    def test_merge_uses_non_empty_telephone(self):
        profiles = [
            make_profile("Acme", "AB1 1AB", source="companies_house", telephone="111", address="A", business_type=None),
            make_profile("Acme", "AB1 1AB", source="google_places", telephone="222", address="B", business_type=None),
        ]
        result = self.orchestrator._deduplicate_and_merge(profiles, MagicMock())
        merged = result[0]
        self.assertEqual(merged.telephone, "111")

    def test_merge_open_hours(self):
        profiles = [
            make_profile("Acme", "AB1 1AB", source="companies_house"),
            make_profile("Acme", "AB1 1AB", source="google_places"),
        ]
        profiles[1].open_hours = {"monday": "9-5"}
        result = self.orchestrator._deduplicate_and_merge(profiles, MagicMock())
        self.assertEqual(result[0].open_hours, {"monday": "9-5"})

    def test_sorted_by_confidence_desc(self):
        profiles = [
            make_profile("A", "AB1 1AB", source="companies_house", confidence=0.5),
            make_profile("B", "CD2 2CD", source="companies_house", confidence=0.9),
            make_profile("C", "EF3 3EF", source="companies_house", confidence=0.7),
        ]
        result = self.orchestrator._deduplicate_and_merge(profiles, MagicMock())
        confidences = [p.confidence for p in result]
        self.assertEqual(confidences, sorted(confidences, reverse=True))


class TestConfidenceComputation(unittest.TestCase):
    def test_single_source_avg(self):
        from scraper.orchestrator.scraper import ScraperOrchestrator
        profiles = [make_profile("A", "AB1 1AB", confidence=0.5)]
        result = ScraperOrchestrator._compute_confidence(profiles)
        self.assertAlmostEqual(result, 0.5)

    def test_two_sources_boost(self):
        from scraper.orchestrator.scraper import CORROBORATION_BOOST_PER_SOURCE, ScraperOrchestrator
        profiles = [
            make_profile("A", "AB1 1AB", source="companies_house", confidence=0.5),
            make_profile("A", "AB1 1AB", source="google_places", confidence=0.9),
        ]
        result = ScraperOrchestrator._compute_confidence(profiles)
        avg = (0.5 + 0.9) / 2
        expected = min(1.0, avg + CORROBORATION_BOOST_PER_SOURCE)
        self.assertAlmostEqual(result, expected)

    def test_empty_profiles(self):
        from scraper.orchestrator.scraper import ScraperOrchestrator
        result = ScraperOrchestrator._compute_confidence([])
        self.assertEqual(result, 0.0)

    def test_clamped_max(self):
        from scraper.orchestrator.scraper import ScraperOrchestrator
        profiles = [
            make_profile("A", "AB1 1AB", source="companies_house", confidence=1.0),
            make_profile("A", "AB1 1AB", source="google_places", confidence=1.0),
        ]
        result = ScraperOrchestrator._compute_confidence(profiles)
        self.assertLessEqual(result, 1.0)

    def test_clamped_min(self):
        from scraper.orchestrator.scraper import ScraperOrchestrator
        profiles = [
            make_profile("A", "AB1 1AB", source="companies_house", confidence=0.0),
            make_profile("A", "AB1 1AB", source="google_places", confidence=0.0),
        ]
        result = ScraperOrchestrator._compute_confidence(profiles)
        self.assertGreaterEqual(result, 0.0)


class TestScraperHelpers(unittest.TestCase):
    def setUp(self):
        from scraper.orchestrator.scraper import ScraperOrchestrator
        self.orchestrator = ScraperOrchestrator.__new__(ScraperOrchestrator)

    def test_normalize_name(self):
        result = self.orchestrator._normalize_name("  Acme   Ltd  ")
        self.assertEqual(result, "acme ltd")

    def test_normalize_postcode(self):
        result = self.orchestrator._normalize_postcode("AB1 1AB")
        self.assertEqual(result, "AB11AB")

    def test_normalize_postcode_empty(self):
        result = self.orchestrator._normalize_postcode("")
        self.assertEqual(result, "")

    def test_pick_non_empty_first(self):
        values = ["first", "", None, "second"]
        result = self.orchestrator._pick_non_empty(values)
        self.assertEqual(result, "first")

    def test_pick_non_empty_skip_none_and_empty(self):
        values = [None, "", "value"]
        result = self.orchestrator._pick_non_empty(values)
        self.assertEqual(result, "value")

    def test_pick_non_empty_default(self):
        values = [None, "", None]
        result = self.orchestrator._pick_non_empty(values, default="default")
        self.assertEqual(result, "default")


class TestScraperStats(unittest.TestCase):
    def test_stats_to_dict(self):
        from scraper.orchestrator.scraper import ScrapeStats
        stats = ScrapeStats(query={"town": "Chelmsford"}, location={"type": "TownResult", "town": "Chelmsford"})
        stats.sources = {"companies_house": 10, "google_places": 5}
        stats.total_raw = 15
        stats.total_unique = 12
        stats.errors = ["error1"]
        d = stats.to_dict()
        self.assertEqual(d["total_raw"], 15)
        self.assertEqual(d["total_unique"], 12)
        self.assertEqual(d["errors"], ["error1"])


class TestScraperScrape(unittest.TestCase):
    def test_scrape_invalid_query_type(self):
        from scraper.orchestrator.scraper import ScraperOrchestrator, ScraperError
        from scraper.models.company import CompanySearchQuery
        orchestrator = ScraperOrchestrator.__new__(ScraperOrchestrator)
        query = CompanySearchQuery(town="Chelmsford")
        with self.assertRaises(ScraperError):
            orchestrator.scrape(query)

    def test_scrape_invalid_query_empty(self):
        from scraper.orchestrator.scraper import ScraperOrchestrator, ScraperError
        from scraper.models.company import PostcodeSearchQuery
        orchestrator = ScraperOrchestrator.__new__(ScraperOrchestrator)
        query = PostcodeSearchQuery(postcode="")
        with self.assertRaises(ScraperError):
            orchestrator.scrape(query)

    def test_scrape_by_postcode(self):
        from scraper.orchestrator.scraper import ScraperOrchestrator
        from scraper.models.company import PostcodeSearchQuery
        from scraper.geocoding.geocoder import PostcodeResult, Geocoder
        from scraper.connectors.companies_house import CompaniesHouseConnector

        mock_geocoder = MagicMock(spec=Geocoder)
        mock_location = PostcodeResult(postcode="AB11AB", latitude=51.0, longitude=0.0, radius_km=1.0)
        mock_geocoder.resolve_postcode.return_value = mock_location

        mock_ch = MagicMock(spec=CompaniesHouseConnector)
        mock_ch.search_by_postcode_mapped.return_value = [make_profile("Acme", "AB11AB")]

        def mock_gp_search(lat, lng, radius, query):
            return [make_profile("Acme", "AB11AB", source="google_places", telephone="123")]

        orchestrator = ScraperOrchestrator(
            geocoder=mock_geocoder,
            companies_house=mock_ch,
            google_places_search_fn=mock_gp_search,
            max_workers=1,
        )
        query = PostcodeSearchQuery(postcode="AB1 1AB")
        result = orchestrator.scrape(query, sync=True)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].company_name, "Acme")

    def test_scrape_by_town(self):
        from scraper.orchestrator.scraper import ScraperOrchestrator
        from scraper.models.company import TownSearchQuery
        from scraper.geocoding.geocoder import TownResult, Geocoder
        from scraper.connectors.companies_house import CompaniesHouseConnector

        mock_geocoder = MagicMock(spec=Geocoder)
        mock_location = TownResult(town="Chelmsford", latitude=51.735, longitude=0.469, radius_km=10.0)
        mock_geocoder.resolve_town.return_value = mock_location

        mock_ch = MagicMock(spec=CompaniesHouseConnector)
        mock_ch.search_by_company_name_mapped.return_value = [make_profile("Acme", "AB11AB")]

        def mock_gp_search(lat, lng, radius, query):
            return [make_profile("Beta", "CD22CD", source="google_places", telephone="456")]

        orchestrator = ScraperOrchestrator(
            geocoder=mock_geocoder,
            companies_house=mock_ch,
            google_places_search_fn=mock_gp_search,
            max_workers=1,
        )
        query = TownSearchQuery(town="Chelmsford")
        result = orchestrator.scrape(query, sync=True)
        self.assertEqual(len(result), 2)
