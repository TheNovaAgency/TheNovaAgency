import logging
import time
from collections import deque
from threading import Lock
from typing import Any

import requests

from config.config import config
from src.scraper.models.company import CompanyProfile

logger = logging.getLogger(__name__)

PLACES_BASE_URL = "https://maps.googleapis.com/maps/api/place"
FALLBACK_CONFIDENCE = 0.6


class GooglePlacesError(Exception):
    pass


class GooglePlacesQuotaExceeded(GooglePlacesError):
    pass


class RateLimiter:
    def __init__(self, max_requests: int, period: float = 60.0) -> None:
        self._max_requests = max_requests
        self._period = period
        self._timestamps: deque[float] = deque()
        self._lock = Lock()

    def wait(self) -> None:
        with self._lock:
            now = time.time()
            while self._timestamps and now - self._timestamps[0] >= self._period:
                self._timestamps.popleft()

            if len(self._timestamps) >= self._max_requests:
                sleep_time = self._period - (now - self._timestamps[0])
                if sleep_time > 0:
                    logger.debug("Rate limit reached, sleeping for %.2f seconds", sleep_time)
                    time.sleep(sleep_time)
                now = time.time()
                while self._timestamps and now - self._timestamps[0] >= self._period:
                    self._timestamps.popleft()

            self._timestamps.append(time.time())


_rate_limiter = RateLimiter(max_requests=config.GOOGLE_PLACES_RATE_LIMIT)


def _require_api_key() -> str:
    api_key = config.GOOGLE_PLACES_API_KEY
    if not api_key:
        logger.warning("GOOGLE_PLACES_API_KEY is not configured")
        raise GooglePlacesError("Google Places API key is not configured")
    return api_key


def _request_with_retry(
    url: str,
    params: dict[str, Any],
    max_retries: int = 4,
    base_delay: float = 1.0,
) -> dict[str, Any]:
    api_key = _require_api_key()
    params["key"] = api_key

    last_exception = None
    for attempt in range(max_retries):
        _rate_limiter.wait()
        try:
            response = requests.get(
                url,
                params=params,
                timeout=config.REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            result = response.json()

            status = result.get("status", "")

            if status == "OVER_QUERY_LIMIT":
                logger.warning("Google Places API quota exceeded (attempt %d)", attempt + 1)
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.info("Retrying after %.1f seconds", delay)
                    time.sleep(delay)
                    continue
                raise GooglePlacesQuotaExceeded("Google Places API quota exceeded")

            if status == "REQUEST_DENIED":
                raise GooglePlacesError(f"Google Places API request denied: {result.get('error_message', '')}")

            if status == "INVALID_REQUEST":
                raise GooglePlacesError(f"Google Places API invalid request: {result.get('error_message', '')}")

            if status == "ZERO_RESULTS":
                return {"results": [], "status": "ZERO_RESULTS"}

            if status == "OK":
                return result

            if status == "":
                raise GooglePlacesError("Empty response from Google Places API")

            logger.warning("Unexpected Google Places API status: %s", status)
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
                continue
            raise GooglePlacesError(f"Google Places API returned status: {status}")

        except requests.exceptions.Timeout:
            logger.warning("Request timeout (attempt %d)", attempt + 1)
            last_exception = GooglePlacesError("Request to Google Places API timed out")
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
                continue
            raise last_exception

        except requests.exceptions.HTTPError as exc:
            status_code = exc.response.status_code if exc.response is not None else 0
            logger.warning("HTTP error %d (attempt %d)", status_code, attempt + 1)
            last_exception = GooglePlacesError(f"Google Places API HTTP error: {exc}")
            if 500 <= status_code < 600 and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
                continue
            raise last_exception

        except requests.exceptions.ConnectionError:
            logger.warning("Connection error (attempt %d)", attempt + 1)
            last_exception = GooglePlacesError("Could not connect to Google Places API")
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
                continue
            raise last_exception

        except requests.exceptions.RequestException as exc:
            last_exception = GooglePlacesError(f"Request to Google Places API failed: {exc}")
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                time.sleep(delay)
                continue
            raise last_exception

    raise last_exception or GooglePlacesError("Google Places API request failed after all retries")


def _extract_address_component(components: list[dict[str, Any]], component_type: str) -> str | None:
    for component in components:
        if component_type in component.get("types", []):
            return component.get("long_name", "") or component.get("short_name", "")
    return None


def _parse_opening_hours(place: dict[str, Any]) -> dict[str, str] | None:
    opening_hours = place.get("opening_hours")
    if not opening_hours:
        return None

    weekday_text = opening_hours.get("weekday_text", [])
    if not weekday_text:
        return None

    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    parsed: dict[str, str] = {}
    for idx, text in enumerate(weekday_text):
        if idx < len(days):
            parsed[days[idx]] = text

    return parsed if parsed else None


def _place_to_company_profile(
    place: dict[str, Any],
    lat: float | None = None,
    lng: float | None = None,
) -> CompanyProfile:
    name = place.get("name", "")
    vicinity = place.get("vicinity", "")
    address = place.get("formatted_address") or vicinity or ""

    components = place.get("address_components", [])
    postcode = _extract_address_component(components, "postal_code") or ""
    town = (
        _extract_address_component(components, "locality")
        or _extract_address_component(components, "postal_town")
        or ""
    )

    business_type = ""
    types = place.get("types", [])
    if types:
        business_type = types[0].replace("_", " ").title()

    phone = None
    website = None
    open_hours = None

    if "details" in place:
        details = place["details"]
        phone = details.get("formatted_phone_number") or details.get("international_phone_number")
        website = details.get("website")
        open_hours = _parse_opening_hours(details)

    main_contact = phone

    profile = CompanyProfile(
        company_name=name,
        telephone=phone,
        email=None,
        address=address,
        main_contact=main_contact,
        business_type=business_type or None,
        open_hours=open_hours,
        postcode=postcode,
        town=town,
        source="google_places",
        confidence=FALLBACK_CONFIDENCE,
    )
    return profile


def search_by_location(
    lat: float,
    lng: float,
    radius: float,
    query: str,
) -> list[CompanyProfile]:
    api_key = config.GOOGLE_PLACES_API_KEY
    if not api_key:
        logger.warning("Skipping Google Places search: API key not configured")
        return []

    radius_m = min(int(radius * 1000), 50000)

    results: list[dict[str, Any]] = []

    text_url = f"{PLACES_BASE_URL}/textsearch/json"
    text_params: dict[str, Any] = {
        "query": query,
        "location": f"{lat},{lng}",
        "radius": radius_m,
    }
    try:
        text_result = _request_with_retry(text_url, text_params)
        text_results = text_result.get("results", [])
        results.extend(text_results)
        logger.info("Text Search returned %d results", len(text_results))
    except (GooglePlacesError, GooglePlacesQuotaExceeded) as exc:
        logger.warning("Text Search failed: %s", exc)

    if not results:
        nearby_url = f"{PLACES_BASE_URL}/nearbysearch/json"
        nearby_params: dict[str, Any] = {
            "location": f"{lat},{lng}",
            "radius": radius_m,
            "keyword": query,
        }
        try:
            nearby_result = _request_with_retry(nearby_url, nearby_params)
            nearby_results = nearby_result.get("results", [])
            results.extend(nearby_results)
            logger.info("Nearby Search returned %d results", len(nearby_results))
        except (GooglePlacesError, GooglePlacesQuotaExceeded) as exc:
            logger.warning("Nearby Search failed: %s", exc)

    seen = set()
    profiles: list[CompanyProfile] = []
    for place in results:
        place_id = place.get("place_id", "")
        key = place_id or place.get("name", "")
        if key in seen:
            continue
        seen.add(key)

        try:
            profile = _place_to_company_profile(place, lat=lat, lng=lng)
            profiles.append(profile)
        except Exception as exc:
            logger.warning("Failed to map place '%s' to CompanyProfile: %s", place.get("name"), exc)

    logger.info("search_by_location returned %d unique profiles for query '%s'", len(profiles), query)
    return profiles


def place_details(place_id: str) -> CompanyProfile | None:
    api_key = config.GOOGLE_PLACES_API_KEY
    if not api_key:
        logger.warning("Skipping Google Places detail fetch: API key not configured")
        return None

    url = f"{PLACES_BASE_URL}/details/json"
    params: dict[str, Any] = {
        "place_id": place_id,
        "fields": ",".join(
            [
                "name",
                "formatted_address",
                "formatted_phone_number",
                "international_phone_number",
                "website",
                "opening_hours",
                "address_components",
                "types",
                "vicinity",
            ]
        ),
    }

    try:
        result = _request_with_retry(url, params)
        place = result.get("result", {})
        if not place:
            logger.warning("No result returned for place_id: %s", place_id)
            return None

        profile = _place_to_company_profile(place)
        profile.confidence = 0.8
        logger.info("Fetched details for place '%s'", profile.company_name)
        return profile

    except GooglePlacesQuotaExceeded:
        logger.error("Quota exceeded while fetching details for place_id: %s", place_id)
        return None

    except GooglePlacesError as exc:
        logger.error("Failed to fetch details for place_id %s: %s", place_id, exc)
        return None


def enrich_company_profile(
    profile: CompanyProfile,
    lat: float | None = None,
    lng: float | None = None,
) -> CompanyProfile:
    api_key = config.GOOGLE_PLACES_API_KEY
    if not api_key:
        logger.debug("Skipping enrichment: Google Places API key not configured")
        return profile

    try:
        search_results = search_by_location(
            lat=lat or 51.0,
            lng=lng or 0.0,
            radius=10.0,
            query=profile.company_name,
        )
    except GooglePlacesQuotaExceeded:
        logger.warning("Quota exceeded during enrichment for '%s', returning original profile", profile.company_name)
        return profile

    if not search_results:
        return profile

    best_match = search_results[0]
    if best_match.company_name.lower() != profile.company_name.lower():
        logger.debug(
            "Enrichment best match '%s' differs from query '%s'",
            best_match.company_name,
            profile.company_name,
        )

    if not profile.telephone and best_match.telephone:
        profile.telephone = best_match.telephone
    if not profile.address or profile.address == "":
        profile.address = best_match.address
    if not profile.business_type:
        profile.business_type = best_match.business_type
    if not profile.town:
        profile.town = best_match.town
    if not profile.postcode:
        profile.postcode = best_match.postcode
    if not profile.open_hours:
        profile.open_hours = best_match.open_hours
    if best_match.main_contact and not profile.main_contact:
        profile.main_contact = best_match.main_contact

    profile.confidence = min(1.0, profile.confidence + 0.1)
    profile.source = "google_places"
    return profile
