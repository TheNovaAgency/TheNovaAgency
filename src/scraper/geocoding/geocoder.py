import json
import logging
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from config.config import config

logger = logging.getLogger(__name__)


class GeocodingError(Exception):
    """Base exception for geocoding errors."""


class InvalidPostcodeError(GeocodingError):
    """Raised when a postcode format is invalid."""


class NoResultsError(GeocodingError):
    """Raised when no geocoding results are found."""


class AmbiguousResultError(GeocodingError):
    """Raised when multiple results are returned for a town name."""


@dataclass
class PostcodeResult:
    postcode: str
    latitude: float
    longitude: float
    radius_km: float
    bbox: tuple[float, float, float, float] | None = None

    def __post_init__(self) -> None:
        self.postcode = self.postcode.strip().upper().replace(" ", "")
        self.radius_km = max(0.1, float(self.radius_km))

    def bbox_from_radius(self) -> tuple[float, float, float, float]:
        if self.bbox is not None:
            return self.bbox
        lat_deg_per_km = 1.0 / 110.574
        lng_deg_per_km = 1.0 / (111.320 * abs(self._cos_lat(self.latitude)))
        lat_offset = self.radius_km * lat_deg_per_km
        lng_offset = self.radius_km * lng_deg_per_km
        return (
            self.latitude - lat_offset,
            self.latitude + lat_offset,
            self.longitude - lng_offset,
            self.longitude + lng_offset,
        )

    @staticmethod
    def _cos_lat(lat: float) -> float:
        import math
        return max(0.001, math.cos(math.radians(lat)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "postcode": self.postcode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "radius_km": self.radius_km,
            "bbox": list(self.bbox) if self.bbox is not None else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PostcodeResult":
        bbox = data.get("bbox")
        bbox_tuple = tuple(bbox) if bbox is not None else None
        return cls(
            postcode=data.get("postcode", ""),
            latitude=data.get("latitude", 0.0),
            longitude=data.get("longitude", 0.0),
            radius_km=data.get("radius_km", 1.0),
            bbox=bbox_tuple,
        )


@dataclass
class TownResult:
    town: str
    latitude: float
    longitude: float
    radius_km: float
    bbox: tuple[float, float, float, float] | None = None

    def __post_init__(self) -> None:
        self.town = self.town.strip()
        self.radius_km = max(0.1, float(self.radius_km))

    def bbox_from_radius(self) -> tuple[float, float, float, float]:
        if self.bbox is not None:
            return self.bbox
        lat_deg_per_km = 1.0 / 110.574
        lng_deg_per_km = 1.0 / (111.320 * abs(self._cos_lat(self.latitude)))
        lat_offset = self.radius_km * lat_deg_per_km
        lng_offset = self.radius_km * lng_deg_per_km
        return (
            self.latitude - lat_offset,
            self.latitude + lat_offset,
            self.longitude - lng_offset,
            self.longitude + lng_offset,
        )

    @staticmethod
    def _cos_lat(lat: float) -> float:
        import math
        return max(0.001, math.cos(math.radians(lat)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "town": self.town,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "radius_km": self.radius_km,
            "bbox": list(self.bbox) if self.bbox is not None else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TownResult":
        bbox = data.get("bbox")
        bbox_tuple = tuple(bbox) if bbox is not None else None
        return cls(
            town=data.get("town", ""),
            latitude=data.get("latitude", 0.0),
            longitude=data.get("longitude", 0.0),
            radius_km=data.get("radius_km", 10.0),
            bbox=bbox_tuple,
        )


class GeocoderCache:
    def __init__(self, cache_path: str | None = None) -> None:
        self._cache_path = cache_path or config.GEOCODING_CACHE_PATH
        self._cache: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self._cache_path):
            try:
                with open(self._cache_path, "r", encoding="utf-8") as f:
                    self._cache = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logger.warning("Failed to load geocoding cache: %s", e)
                self._cache = {}

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self._cache_path) or ".", exist_ok=True)
        try:
            with open(self._cache_path, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, ensure_ascii=False, indent=2)
        except OSError as e:
            logger.warning("Failed to save geocoding cache: %s", e)

    def get(self, key: str) -> dict[str, Any] | None:
        return self._cache.get(key)

    def set(self, key: str, value: dict[str, Any]) -> None:
        self._cache[key] = value
        self._save()

    def clear(self) -> None:
        self._cache = {}
        self._save()


class Geocoder:
    POSTCODES_IO_BASE = "https://api.postcodes.io"
    NOMINATIM_BASE = "https://nominatim.openstreetmap.org"
    DEFAULT_TOWN_RADIUS_KM = 10.0
    DEFAULT_POSTCODE_RADIUS_KM = 1.0
    NOMINATIM_USER_AGENT = "business-data-scraper/1.0"

    def __init__(
        self,
        cache: GeocoderCache | None = None,
        timeout: int | None = None,
    ) -> None:
        self._cache = cache or GeocoderCache()
        self._timeout = timeout if timeout is not None else config.REQUEST_TIMEOUT

    def _request_json(self, url: str) -> dict[str, Any] | list[Any] | None:
        req = Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", self.NOMINATIM_USER_AGENT)
        try:
            with urlopen(req, timeout=self._timeout) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw)
        except HTTPError as e:
            logger.error("Geocoding HTTP error %d for %s: %s", e.code, url, e.reason)
            return None
        except (URLError, json.JSONDecodeError, ValueError, OSError) as e:
            logger.error("Geocoding request failed for %s: %s", url, e)
            return None

    def resolve_postcode(self, postcode: str, radius_km: float | None = None) -> PostcodeResult:
        cleaned = postcode.strip().upper().replace(" ", "")
        if not cleaned:
            raise InvalidPostcodeError("Postcode must not be empty")

        cache_key = f"postcode:{cleaned}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return PostcodeResult.from_dict(cached)

        url = f"{self.POSTCODES_IO_BASE}/postcodes/{quote(cleaned)}"
        data = self._request_json(url)
        if not isinstance(data, dict):
            raise NoResultsError(f"No result for postcode {cleaned}")

        result = data.get("result")
        if not isinstance(result, dict) or result.get("status") == 404:
            raise InvalidPostcodeError(f"Invalid or unknown postcode: {cleaned}")

        latitude = result.get("latitude")
        longitude = result.get("longitude")
        if latitude is None or longitude is None:
            raise NoResultsError(f"Missing coordinates for postcode {cleaned}")

        postcode_result = PostcodeResult(
            postcode=cleaned,
            latitude=float(latitude),
            longitude=float(longitude),
            radius_km=radius_km if radius_km is not None else self.DEFAULT_POSTCODE_RADIUS_KM,
        )

        self._cache.set(cache_key, postcode_result.to_dict())
        return postcode_result

    def resolve_town(self, town: str, radius_km: float | None = None) -> TownResult:
        cleaned = town.strip()
        if not cleaned:
            raise GeocodingError("Town name must not be empty")

        cache_key = f"town:{cleaned.lower()}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return TownResult.from_dict(cached)

        url = (
            f"{self.NOMINATIM_BASE}/search"
            f"?q={quote(cleaned)}"
            f"&format=json"
            f"&limit=5"
            f"&addressdetails=1"
        )
        data = self._request_json(url)
        if not isinstance(data, list) or not data:
            raise NoResultsError(f"No geocoding results for town: {cleaned}")

        uk_results = [r for r in data if self._is_uk(r)]
        if not uk_results:
            uk_results = data

        if len(uk_results) > 1:
            raise AmbiguousResultError(
                f"Multiple results for town '{cleaned}'; please be more specific"
            )

        top = uk_results[0]
        lat = top.get("lat")
        lon = top.get("lon")
        bbox_raw = top.get("boundingbox")

        if lat is None or lon is None:
            raise NoResultsError(f"Missing coordinates for town: {cleaned}")

        bbox: tuple[float, float, float, float] | None = None
        if isinstance(bbox_raw, list) and len(bbox_raw) == 4:
            try:
                bbox = (float(bbox_raw[0]), float(bbox_raw[1]), float(bbox_raw[2]), float(bbox_raw[3]))
            except (TypeError, ValueError):
                bbox = None

        town_result = TownResult(
            town=cleaned,
            latitude=float(lat),
            longitude=float(lon),
            radius_km=radius_km if radius_km is not None else self.DEFAULT_TOWN_RADIUS_KM,
            bbox=bbox,
        )

        self._cache.set(cache_key, town_result.to_dict())
        return town_result

    def resolve(self, location: str, radius_km: float | None = None) -> PostcodeResult | TownResult:
        cleaned = location.strip()
        if not cleaned:
            raise GeocodingError("Location must not be empty")

        if self._looks_like_postcode(cleaned):
            try:
                return self.resolve_postcode(cleaned, radius_km=radius_km)
            except InvalidPostcodeError:
                pass
            except NoResultsError:
                pass

        return self.resolve_town(cleaned, radius_km=radius_km)

    def _looks_like_postcode(self, value: str) -> bool:
        import re
        cleaned = value.strip().upper().replace(" ", "")
        return bool(re.match(r"^[A-Z]{1,2}[0-9][0-9A-Z]?\s*[0-9][A-Z]{2}$", value.strip(), re.IGNORECASE))

    @staticmethod
    def _is_uk(result: dict[str, Any]) -> bool:
        address = result.get("address", {})
        if not isinstance(address, dict):
            return False
        country = (address.get("country") or "").lower()
        country_code = (address.get("country_code") or "").lower()
        return country in ("united kingdom", "uk", "great britain", "england", "scotland", "wales") or country_code == "gb"

    def clear_cache(self) -> None:
        self._cache.clear()
