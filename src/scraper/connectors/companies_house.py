import base64
import json
import logging
import time
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from config.config import config
from scraper.models.company import CompanyProfile

logger = logging.getLogger(__name__)


class CompaniesHouseError(Exception):
    """Base exception for Companies House connector errors."""


class CompaniesHouseRateLimitError(CompaniesHouseError):
    """Raised when the API rate limit is exceeded after exhausting retries."""


class CompaniesHouseConnector:
    BASE_URL = "https://api.company-information.service.gov.uk"
    DEFAULT_ITEMS_PER_PAGE = 100
    MAX_SEARCH_PAGES = 10

    def __init__(
        self,
        api_key: str | None = None,
        rate_limit: int | None = None,
        timeout: int | None = None,
    ) -> None:
        self._api_key = api_key or config.COMPANIES_HOUSE_API_KEY
        self._rate_limit = (
            rate_limit if rate_limit is not None else config.COMPANIES_HOUSE_RATE_LIMIT
        )
        self._timeout = timeout if timeout is not None else config.REQUEST_TIMEOUT
        self._last_request_time: float = 0.0

    def _rate_limit_wait(self) -> None:
        if self._rate_limit <= 0:
            return
        min_interval = 60.0 / self._rate_limit
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)
        self._last_request_time = time.monotonic()

    def _build_request(self, path: str) -> Request:
        url = f"{self.BASE_URL}{path}"
        req = Request(url)
        req.add_header("Accept", "application/json")
        if self._api_key:
            auth_header = base64.b64encode(
                f"{self._api_key}:".encode("utf-8")
            ).decode("utf-8")
            req.add_header("Authorization", f"Basic {auth_header}")
        return req

    @staticmethod
    def _parse_retry_after(error: HTTPError) -> float | None:
        retry_after = error.headers.get("Retry-After")
        if retry_after:
            try:
                return float(retry_after)
            except (TypeError, ValueError):
                pass
        reset = error.headers.get("X-RateLimit-Reset")
        if reset:
            try:
                reset_ts = float(reset)
                return max(0.0, reset_ts - time.time())
            except (TypeError, ValueError):
                pass
        return None

    def _request(
        self,
        path: str,
        retries: int = 3,
        backoff: float = 1.0,
    ) -> dict[str, Any] | list[Any] | None:
        for attempt in range(retries + 1):
            self._rate_limit_wait()
            req = self._build_request(path)
            try:
                with urlopen(req, timeout=self._timeout) as response:
                    raw = response.read().decode("utf-8")
                    return json.loads(raw)
            except HTTPError as e:
                retry_after = self._parse_retry_after(e)
                wait = retry_after if retry_after is not None else backoff * (2 ** attempt)
                if e.code == 429:
                    if attempt < retries:
                        logger.warning(
                            "Companies House rate limited (429); backing off %.2fs "
                            "(attempt %d/%d)",
                            wait,
                            attempt + 1,
                            retries + 1,
                        )
                        time.sleep(wait)
                        continue
                    logger.warning("Companies House rate limited (429); giving up")
                    raise CompaniesHouseRateLimitError("Rate limit exceeded") from e
                if e.code >= 500:
                    if attempt < retries:
                        logger.warning(
                            "Companies House transient error %d; retrying in %.2fs",
                            e.code,
                            wait,
                        )
                        time.sleep(wait)
                        continue
                    logger.error("Companies House server error %d after retries", e.code)
                    return None
                try:
                    err_body = json.loads(e.read().decode("utf-8"))
                except (ValueError, OSError):
                    err_body = {}
                logger.error(
                    "Companies House request failed with %d: %s", e.code, err_body
                )
                return None
            except (URLError, json.JSONDecodeError, ValueError, OSError) as e:
                wait = backoff * (2 ** attempt)
                if attempt < retries:
                    logger.warning(
                        "Network/JSON error on attempt %d: %s; retrying in %.2fs",
                        attempt + 1,
                        e,
                        wait,
                    )
                    time.sleep(wait)
                    continue
                logger.error(
                    "Companies House request failed after %d retries: %s", retries, e
                )
                return None
        return None

    def _search_all(self, query: str) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        start_index = 0
        while True:
            path = (
                f"/company?q={quote(query)}"
                f"&start_index={start_index}"
                f"&items_per_page={self.DEFAULT_ITEMS_PER_PAGE}"
            )
            data = self._request(path)
            if not isinstance(data, dict):
                break
            page_items = data.get("items", [])
            if isinstance(page_items, list):
                items.extend(page_items)
            total = data.get("total_results", 0)
            per_page = data.get("items_per_page", len(page_items)) or len(page_items)
            start_index += per_page
            if not page_items or start_index >= total or len(items) >= total:
                break
            if start_index // max(per_page, 1) >= self.MAX_SEARCH_PAGES:
                break
        return items

    def search_by_postcode(self, postcode: str) -> list[dict[str, Any]]:
        cleaned = postcode.strip().upper().replace(" ", "")
        if not cleaned:
            return []
        return self._search_all(cleaned)

    def search_by_company_name(self, name: str) -> list[dict[str, Any]]:
        cleaned = name.strip()
        if not cleaned:
            return []
        return self._search_all(cleaned)

    def get_company_details(self, company_number: str) -> dict[str, Any] | None:
        if not company_number.strip():
            return None
        return self._request(f"/company/{company_number.strip()}")

    def get_officers(self, company_number: str) -> list[dict[str, Any]]:
        if not company_number.strip():
            return []
        data = self._request(f"/company/{company_number.strip()}/officers")
        if isinstance(data, dict):
            officers = data.get("items", [])
            return officers if isinstance(officers, list) else []
        if isinstance(data, list):
            return data
        return []

    def _format_address(self, address: Any) -> str:
        if isinstance(address, dict):
            fields = [
                "address_line_1",
                "address_line_2",
                "address_line_3",
                "address_line_4",
                "locality",
                "town",
                "postal_code",
                "country",
            ]
            parts = [str(address[f]).strip() for f in fields if address.get(f)]
            return ", ".join(parts)
        if isinstance(address, str):
            return address.strip()
        return ""

    @staticmethod
    def _extract_postcode(address: Any) -> str:
        if isinstance(address, dict):
            for key in ("postal_code", "registered_office_postcode", "postcode"):
                value = address.get(key)
                if value:
                    return str(value).strip().upper()
            return ""
        if isinstance(address, str):
            parts = address.split(",")
            for part in reversed(parts):
                candidate = part.strip()
                if len(candidate) >= 4:
                    return candidate.upper()
            return ""
        return ""

    @staticmethod
    def _extract_town(address: Any) -> str:
        if isinstance(address, dict):
            for key in ("locality", "town", "registered_office_town", "city"):
                value = address.get(key)
                if value:
                    return str(value).strip()
            return ""
        if isinstance(address, str):
            parts = address.split(",")
            if len(parts) >= 2:
                return parts[-2].strip()
            return ""
        return ""

    def _resolve_address_fields(
        self, item: dict[str, Any]
    ) -> tuple[str, str, str]:
        address = item.get("registered_office_address") or item.get("address")
        address_str = self._format_address(address)

        postcode = item.get("registered_office_postcode") or ""
        if not postcode and address_str:
            postcode = self._extract_postcode(address)

        town = item.get("registered_office_town") or item.get("registered_office_locality") or ""
        if not town:
            town = self._extract_town(address)

        return address_str, postcode, town

    def map_to_profile(self, item: dict[str, Any]) -> CompanyProfile | None:
        if not isinstance(item, dict):
            return None
        company_name = (item.get("company_name") or "").strip()
        if not company_name:
            return None

        address_str, postcode, town = self._resolve_address_fields(item)

        sic_codes = item.get("sic_codes", [])
        if isinstance(sic_codes, list):
            sic_codes = [str(c) for c in sic_codes if c]
        business_type = item.get("sic_industry_description") or ""
        if not business_type and sic_codes:
            business_type = ", ".join(sic_codes)
        if not business_type:
            business_type = item.get("type", "")

        company_number = item.get("company_number") or ""
        officers = self.get_officers(company_number) if company_number else []
        officer_names = [
            o.get("name", "").strip()
            for o in officers
            if isinstance(o, dict) and o.get("name")
        ]
        main_contact = officer_names[0] if officer_names else None

        confidence = 0.0
        fields_present = 0
        total_fields = 4
        if company_name:
            fields_present += 1
        if address_str:
            fields_present += 1
        if postcode:
            fields_present += 1
        if business_type:
            fields_present += 1
        confidence = fields_present / total_fields

        return CompanyProfile(
            company_name=company_name,
            telephone=None,
            email=None,
            address=address_str,
            main_contact=main_contact,
            business_type=business_type or None,
            open_hours=None,
            postcode=postcode,
            town=town,
            source="companies_house",
            confidence=confidence,
        )

    def search_by_postcode_mapped(self, postcode: str) -> list[CompanyProfile]:
        return [p for p in (self.map_to_profile(item) for item in self.search_by_postcode(postcode)) if p is not None]

    def search_by_company_name_mapped(self, name: str) -> list[CompanyProfile]:
        return [p for p in (self.map_to_profile(item) for item in self.search_by_company_name(name)) if p is not None]
