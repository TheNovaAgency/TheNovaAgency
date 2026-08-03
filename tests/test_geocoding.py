import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))


def mock_urlopen(req, timeout=None):
    if isinstance(req, MagicMock):
        url = ""
    else:
        url = req.full_url if hasattr(req, "full_url") else ""
    if "/postcodes/" in url and "CM11HT" in url:
        return MockHTTPResponse({
            "status": 200,
            "result": {
                "postcode": "CM1 1HT",
                "latitude": 51.735,
                "longitude": 0.469,
                "admin_district": "Chelmsford",
            },
        })
    if "/postcodes/" in url and "INVALID" in url:
        return MockHTTPResponse({
            "status": 404,
            "error": "Invalid postcode",
        })
    if "/search" in url and "q=Chelmsford" in url:
        return MockHTTPResponse([
            {
                "lat": "51.735",
                "lon": "0.469",
                "boundingbox": ["51.7", "51.8", "0.4", "0.5"],
                "address": {"country": "United Kingdom", "country_code": "gb"},
                "display_name": "Chelmsford, Essex, England, UK",
            }
        ])
    if "/search" in url:
        return MockHTTPResponse([])
    return MockHTTPResponse({}, status=404)


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


class TestPostcodeResult(unittest.TestCase):
    def test_post_init(self):
        from scraper.geocoding.geocoder import PostcodeResult
        result = PostcodeResult(postcode="cm1 1ht", latitude=51.735, longitude=0.469, radius_km=5.0)
        self.assertEqual(result.postcode, "CM11HT")
        self.assertEqual(result.radius_km, 5.0)

    def test_min_radius(self):
        from scraper.geocoding.geocoder import PostcodeResult
        result = PostcodeResult(postcode="AB1 1AB", latitude=51.0, longitude=0.0, radius_km=0.01)
        self.assertEqual(result.radius_km, 0.1)

    def test_bbox_from_radius_with_existing_bbox(self):
        from scraper.geocoding.geocoder import PostcodeResult
        result = PostcodeResult(postcode="AB1 1AB", latitude=51.0, longitude=0.0, radius_km=1.0, bbox=(1.0, 2.0, 3.0, 4.0))
        bbox = result.bbox_from_radius()
        self.assertEqual(bbox, (1.0, 2.0, 3.0, 4.0))

    def test_bbox_from_radius_computed(self):
        from scraper.geocoding.geocoder import PostcodeResult
        result = PostcodeResult(postcode="AB1 1AB", latitude=51.0, longitude=0.0, radius_km=1.0)
        bbox = result.bbox_from_radius()
        self.assertEqual(len(bbox), 4)
        self.assertLess(bbox[0], bbox[1])
        self.assertLess(bbox[2], bbox[3])

    def test_to_dict(self):
        from scraper.geocoding.geocoder import PostcodeResult
        result = PostcodeResult(postcode="AB1 1AB", latitude=51.0, longitude=0.0, radius_km=1.0, bbox=(1.0, 2.0, 3.0, 4.0))
        d = result.to_dict()
        self.assertEqual(d["postcode"], "AB11AB")
        self.assertEqual(d["bbox"], [1.0, 2.0, 3.0, 4.0])

    def test_from_dict(self):
        from scraper.geocoding.geocoder import PostcodeResult
        data = {"postcode": "AB11AB", "latitude": 51.0, "longitude": 0.0, "radius_km": 1.0, "bbox": [1.0, 2.0, 3.0, 4.0]}
        result = PostcodeResult.from_dict(data)
        self.assertEqual(result.postcode, "AB11AB")
        self.assertEqual(result.bbox, (1.0, 2.0, 3.0, 4.0))

    def test_round_trip(self):
        from scraper.geocoding.geocoder import PostcodeResult
        original = PostcodeResult(postcode="AB1 1AB", latitude=51.735, longitude=0.469, radius_km=2.5)
        restored = PostcodeResult.from_dict(original.to_dict())
        self.assertEqual(restored.postcode, "AB11AB")
        self.assertAlmostEqual(restored.latitude, 51.735)
        self.assertAlmostEqual(restored.longitude, 0.469)
        self.assertEqual(restored.radius_km, 2.5)


class TestTownResult(unittest.TestCase):
    def test_post_init(self):
        from scraper.geocoding.geocoder import TownResult
        result = TownResult(town="  Chelmsford  ", latitude=51.735, longitude=0.469, radius_km=10.0)
        self.assertEqual(result.town, "Chelmsford")
        self.assertEqual(result.radius_km, 10.0)

    def test_min_radius(self):
        from scraper.geocoding.geocoder import TownResult
        result = TownResult(town="Town", latitude=51.0, longitude=0.0, radius_km=0.01)
        self.assertEqual(result.radius_km, 0.1)

    def test_to_dict(self):
        from scraper.geocoding.geocoder import TownResult
        result = TownResult(town="Town", latitude=51.0, longitude=0.0, radius_km=5.0)
        d = result.to_dict()
        self.assertEqual(d["town"], "Town")
        self.assertEqual(d["bbox"], None)

    def test_from_dict(self):
        from scraper.geocoding.geocoder import TownResult
        data = {"town": "Town", "latitude": 51.0, "longitude": 0.0, "radius_km": 5.0}
        result = TownResult.from_dict(data)
        self.assertEqual(result.town, "Town")
        self.assertEqual(result.radius_km, 5.0)


class TestGeocoderCache(unittest.TestCase):
    def test_get_set_roundtrip(self):
        from scraper.geocoding.geocoder import GeocoderCache
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "cache.json"
            cache = GeocoderCache(cache_path=str(cache_path))
            cache.set("key", {"value": 42})
            self.assertEqual(cache.get("key"), {"value": 42})

    def test_get_missing(self):
        from scraper.geocoding.geocoder import GeocoderCache
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "cache.json"
            cache = GeocoderCache(cache_path=str(cache_path))
            self.assertIsNone(cache.get("missing"))

    def test_clear(self):
        from scraper.geocoding.geocoder import GeocoderCache
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "cache.json"
            cache = GeocoderCache(cache_path=str(cache_path))
            cache.set("key", {"value": 1})
            cache.clear()
            self.assertIsNone(cache.get("key"))

    def test_load_corrupt_json(self):
        from scraper.geocoding.geocoder import GeocoderCache
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "cache.json"
            cache_path.write_text("not json", encoding="utf-8")
            cache = GeocoderCache(cache_path=str(cache_path))
            self.assertEqual(cache._cache, {})


class TestGeocoder(unittest.TestCase):
    def setUp(self):
        from scraper.geocoding.geocoder import Geocoder, GeocoderCache
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "cache.json"
            self.geocoder = Geocoder(cache=GeocoderCache(cache_path=str(cache_path)), timeout=10)

    @patch("scraper.geocoding.geocoder.urlopen", side_effect=mock_urlopen)
    def test_resolve_postcode(self, mock_urlopen_fn):
        from scraper.geocoding.geocoder import PostcodeResult
        result = self.geocoder.resolve_postcode("CM1 1HT")
        self.assertIsInstance(result, PostcodeResult)
        self.assertEqual(result.postcode, "CM11HT")
        self.assertAlmostEqual(result.latitude, 51.735)
        self.assertAlmostEqual(result.longitude, 0.469)

    @patch("scraper.geocoding.geocoder.urlopen", side_effect=mock_urlopen)
    def test_resolve_postcode_caches(self, mock_urlopen_fn):
        from scraper.geocoding.geocoder import PostcodeResult
        result1 = self.geocoder.resolve_postcode("CM1 1HT")
        result2 = self.geocoder.resolve_postcode("CM1 1HT")
        self.assertEqual(mock_urlopen_fn.call_count, 1)
        self.assertEqual(result1.postcode, result2.postcode)

    def test_resolve_postcode_empty(self):
        from scraper.geocoding.geocoder import InvalidPostcodeError
        with self.assertRaises(InvalidPostcodeError):
            self.geocoder.resolve_postcode("")

    @patch("scraper.geocoding.geocoder.urlopen", side_effect=mock_urlopen)
    def test_resolve_postcode_invalid(self, mock_urlopen_fn):
        from scraper.geocoding.geocoder import InvalidPostcodeError
        with self.assertRaises(InvalidPostcodeError):
            self.geocoder.resolve_postcode("INVALID")

    @patch("scraper.geocoding.geocoder.urlopen", side_effect=mock_urlopen)
    def test_resolve_town(self, mock_urlopen_fn):
        from scraper.geocoding.geocoder import TownResult
        result = self.geocoder.resolve_town("Chelmsford")
        self.assertIsInstance(result, TownResult)
        self.assertEqual(result.town, "Chelmsford")
        self.assertAlmostEqual(result.latitude, 51.735)

    def test_resolve_town_empty(self):
        from scraper.geocoding.geocoder import GeocodingError
        with self.assertRaises(GeocodingError):
            self.geocoder.resolve_town("")

    @patch("scraper.geocoding.geocoder.urlopen", side_effect=mock_urlopen)
    def test_resolve_town_no_results(self, mock_urlopen_fn):
        from scraper.geocoding.geocoder import NoResultsError
        with self.assertRaises(NoResultsError):
            self.geocoder.resolve_town("NonexistentTownXYZ")

    @patch("scraper.geocoding.geocoder.urlopen", side_effect=mock_urlopen)
    def test_resolve_town_caches(self, mock_urlopen_fn):
        from scraper.geocoding.geocoder import TownResult
        result1 = self.geocoder.resolve_town("Chelmsford")
        result2 = self.geocoder.resolve_town("Chelmsford")
        self.assertEqual(mock_urlopen_fn.call_count, 1)

    @patch("scraper.geocoding.geocoder.urlopen", side_effect=mock_urlopen)
    def test_resolve_postcode_lookup(self, mock_urlopen_fn):
        from scraper.geocoding.geocoder import PostcodeResult
        result = self.geocoder.resolve("CM1 1HT")
        self.assertIsInstance(result, PostcodeResult)

    @patch("scraper.geocoding.geocoder.urlopen", side_effect=mock_urlopen)
    def test_resolve_town_lookup(self, mock_urlopen_fn):
        from scraper.geocoding.geocoder import TownResult
        result = self.geocoder.resolve("Chelmsford")
        self.assertIsInstance(result, TownResult)

    def test_resolve_empty(self):
        from scraper.geocoding.geocoder import GeocodingError
        with self.assertRaises(GeocodingError):
            self.geocoder.resolve("")

    def test_looks_like_postcode(self):
        self.assertTrue(self.geocoder._looks_like_postcode("CM1 1HT"))
        self.assertTrue(self.geocoder._looks_like_postcode("SW1A 1AA"))
        self.assertFalse(self.geocoder._looks_like_postcode("Chelmsford"))

    def test_is_uk(self):
        self.assertTrue(self.geocoder._is_uk({"address": {"country": "United Kingdom", "country_code": "gb"}}))
        self.assertTrue(self.geocoder._is_uk({"address": {"country": "England", "country_code": "gb"}}))
        self.assertFalse(self.geocoder._is_uk({"address": {"country": "France", "country_code": "fr"}}))
        self.assertFalse(self.geocoder._is_uk({"address": {}}))

    def test_clear_cache(self):
        from scraper.geocoding.geocoder import PostcodeResult
        self.geocoder._cache.set("test", {"postcode": "AB11AB"})
        self.geocoder.clear_cache()
        self.assertIsNone(self.geocoder._cache.get("test"))
