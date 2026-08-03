import asyncio
import logging
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable

from scraper.connectors.companies_house import CompaniesHouseConnector
from scraper.connectors.google_places import (
    GooglePlacesError,
    search_by_location,
)
from scraper.geocoding.geocoder import (
    Geocoder,
    GeocodingError,
    PostcodeResult,
    TownResult,
)
from scraper.models.company import (
    CompanyProfile,
    PostcodeSearchQuery,
    TownSearchQuery,
)

logger = logging.getLogger(__name__)

SOURCE_COMPANIES_HOUSE = "companies_house"
SOURCE_GOOGLE_PLACES = "google_places"

# Confidence boost applied for each additional source that corroborates a record.
CORROBORATION_BOOST_PER_SOURCE = 0.2


class ScraperError(Exception):
    """Base exception raised by the scraper orchestrator."""


@dataclass
class ScrapeStats:
    """Aggregated statistics about a single scrape operation."""

    query: dict[str, Any]
    location: dict[str, Any] | None = None
    sources: dict[str, int] = field(default_factory=dict)
    total_raw: int = 0
    total_unique: int = 0
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "location": self.location,
            "sources": self.sources,
            "total_raw": self.total_raw,
            "total_unique": self.total_unique,
            "errors": self.errors,
        }


class ScraperOrchestrator:
    """Coordinates geocoding, source fetching, deduplication and scoring.

    Accepts a :class:`PostcodeSearchQuery` or :class:`TownSearchQuery`,
    resolves the location via the geocoder, parallel-fetches companies from the
    Companies House and Google Places connectors, merges and deduplicates the
    results, applies confidence scoring based on source corroboration, and
    returns a list of :class:`CompanyProfile` objects sorted by confidence.
    """

    def __init__(
        self,
        geocoder: Geocoder | None = None,
        companies_house: CompaniesHouseConnector | None = None,
        google_places_search_fn: Callable[..., list[CompanyProfile]] | None = None,
        max_workers: int = 2,
    ) -> None:
        self._geocoder = geocoder or Geocoder()
        self._companies_house = companies_house or CompaniesHouseConnector()
        self._google_places_search = google_places_search_fn or search_by_location
        self._max_workers = max(1, int(max_workers))
        self.last_stats: ScrapeStats | None = None

    # -- Public API ---------------------------------------------------------

    def scrape_by_postcode(
        self,
        postcode: str,
        radius_km: float | None = None,
        sync: bool = True,
    ) -> list[CompanyProfile]:
        query = PostcodeSearchQuery(postcode=postcode, radius_km=radius_km if radius_km is not None else 1.0)
        return self.scrape(query, sync=sync)

    def scrape_by_town(
        self,
        town: str,
        radius_km: float | None = None,
        sync: bool = True,
    ) -> list[CompanyProfile]:
        query = TownSearchQuery(town=town, radius_km=radius_km if radius_km is not None else 10.0)
        return self.scrape(query, sync=sync)

    def scrape(
        self,
        query: PostcodeSearchQuery | TownSearchQuery,
        sync: bool = True,
    ) -> list[CompanyProfile]:
        if not isinstance(query, (PostcodeSearchQuery, TownSearchQuery)):
            raise ScraperError(f"Unsupported query type: {type(query).__name__}")
        if not query.is_valid():
            raise ScraperError("Query is not valid; provide a postcode or town")

        if sync:
            return self._scrape_sync(query)
        return asyncio.run(self._scrape_async(query))

    # -- Scraping -----------------------------------------------------------

    def _scrape_sync(self, query: PostcodeSearchQuery | TownSearchQuery) -> list[CompanyProfile]:
        location = self._resolve_location(query)
        stats = self._new_stats(query, location)

        with ThreadPoolExecutor(max_workers=self._max_workers) as pool:
            ch_future = pool.submit(self._fetch_companies_house, query, stats)
            gp_future = pool.submit(self._fetch_google_places, location, query, stats)
            ch_profiles = ch_future.result()
            gp_profiles = gp_future.result()

        raw_profiles = ch_profiles + gp_profiles
        stats.sources[SOURCE_COMPANIES_HOUSE] = len(ch_profiles)
        stats.sources[SOURCE_GOOGLE_PLACES] = len(gp_profiles)
        stats.total_raw = len(raw_profiles)

        results = self._deduplicate_and_merge(raw_profiles, stats)
        self._log_results(stats, sync=True)
        self.last_stats = stats
        return results

    async def _scrape_async(self, query: PostcodeSearchQuery | TownSearchQuery) -> list[CompanyProfile]:
        location = await asyncio.to_thread(self._resolve_location, query)
        stats = self._new_stats(query, location)

        ch_profiles, gp_profiles = await asyncio.gather(
            asyncio.to_thread(self._fetch_companies_house, query, stats),
            asyncio.to_thread(self._fetch_google_places, location, query, stats),
        )

        raw_profiles = ch_profiles + gp_profiles
        stats.sources[SOURCE_COMPANIES_HOUSE] = len(ch_profiles)
        stats.sources[SOURCE_GOOGLE_PLACES] = len(gp_profiles)
        stats.total_raw = len(raw_profiles)

        results = self._deduplicate_and_merge(raw_profiles, stats)
        self._log_results(stats, sync=False)
        self.last_stats = stats
        return results

    # -- Location resolution ------------------------------------------------

    def _resolve_location(
        self, query: PostcodeSearchQuery | TownSearchQuery
    ) -> PostcodeResult | TownResult:
        try:
            if isinstance(query, PostcodeSearchQuery):
                logger.info(
                    "Resolving postcode '%s' (radius %.2f km)",
                    query.postcode,
                    query.radius_km,
                )
                return self._geocoder.resolve_postcode(query.postcode, query.radius_km)
            logger.info(
                "Resolving town '%s' (radius %.2f km)",
                query.town,
                query.radius_km,
            )
            return self._geocoder.resolve_town(query.town, query.radius_km)
        except GeocodingError as exc:
            logger.error("Geocoding failed for %s: %s", type(query).__name__, exc)
            raise ScraperError(str(exc)) from exc

    @staticmethod
    def _location_to_dict(location: PostcodeResult | TownResult) -> dict[str, Any]:
        data = location.to_dict()
        data["type"] = type(location).__name__
        return data

    # -- Source fetching ----------------------------------------------------

    def _fetch_companies_house(
        self,
        query: PostcodeSearchQuery | TownSearchQuery,
        stats: ScrapeStats,
    ) -> list[CompanyProfile]:
        search_term = query.postcode if isinstance(query, PostcodeSearchQuery) else query.town
        try:
            if isinstance(query, PostcodeSearchQuery):
                profiles = self._companies_house.search_by_postcode_mapped(query.postcode)
            else:
                profiles = self._companies_house.search_by_company_name_mapped(query.town)
        except Exception as exc:
            logger.error("Companies House fetch failed: %s", exc)
            stats.errors.append(f"{SOURCE_COMPANIES_HOUSE}: {exc}")
            return []
        logger.info(
            "Source '%s' returned %d profiles (search=%r)",
            SOURCE_COMPANIES_HOUSE,
            len(profiles),
            search_term,
        )
        return profiles

    def _fetch_google_places(
        self,
        location: PostcodeResult | TownResult,
        query: PostcodeSearchQuery | TownSearchQuery,
        stats: ScrapeStats,
    ) -> list[CompanyProfile]:
        search_term = query.postcode if isinstance(query, PostcodeSearchQuery) else query.town
        try:
            profiles = self._google_places_search(
                lat=location.latitude,
                lng=location.longitude,
                radius=location.radius_km,
                query=search_term,
            )
        except GooglePlacesError as exc:
            logger.error("Google Places fetch failed: %s", exc)
            stats.errors.append(f"{SOURCE_GOOGLE_PLACES}: {exc}")
            return []
        except Exception as exc:
            logger.error("Google Places fetch failed unexpectedly: %s", exc)
            stats.errors.append(f"{SOURCE_GOOGLE_PLACES}: {exc}")
            return []
        logger.info(
            "Source '%s' returned %d profiles (search=%r, lat=%.5f, lng=%.5f)",
            SOURCE_GOOGLE_PLACES,
            len(profiles),
            search_term,
            location.latitude,
            location.longitude,
        )
        return profiles

    # -- Merging / deduplication --------------------------------------------

    def _deduplicate_and_merge(
        self,
        profiles: list[CompanyProfile],
        stats: ScrapeStats,
    ) -> list[CompanyProfile]:
        groups: dict[tuple[str, str], list[CompanyProfile]] = {}
        for profile in profiles:
            key = (
                self._normalize_name(profile.company_name),
                self._normalize_postcode(profile.postcode),
            )
            groups.setdefault(key, []).append(profile)

        merged: list[CompanyProfile] = []
        duplicates = 0
        for group in groups.values():
            if len(group) == 1:
                merged.append(group[0])
            else:
                duplicates += len(group) - 1
                merged.append(self._merge_profiles(group))

        stats.total_unique = len(merged)
        corroborated = sum(1 for g in groups.values() if len({p.source for p in g}) > 1)
        logger.info(
            "Merged %d profiles into %d unique (%d duplicates removed, %d corroborated by multiple sources)",
            len(profiles),
            len(merged),
            duplicates,
            corroborated,
        )
        if stats.errors:
            logger.warning("Scrape completed with %d error(s)", len(stats.errors))

        merged.sort(key=lambda p: (-p.confidence, p.company_name.lower()))
        return merged

    def _merge_profiles(self, group: list[CompanyProfile]) -> CompanyProfile:
        sources = sorted({p.source for p in group})
        name = self._pick_non_empty([p.company_name for p in group], default=group[0].company_name)
        address = self._pick_non_empty([p.address for p in group], default="")
        postcode = self._pick_non_empty([p.postcode for p in group], default="")
        town = self._pick_non_empty([p.town for p in group], default="")
        telephone = self._pick_non_empty([p.telephone for p in group], default=None)
        email = self._pick_non_empty([p.email for p in group], default=None)
        main_contact = self._pick_non_empty([p.main_contact for p in group], default=None)
        business_type = self._pick_non_empty([p.business_type for p in group], default=None)
        open_hours = next((p.open_hours for p in group if p.open_hours is not None), None)

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
            source=",".join(sources),
            confidence=self._compute_confidence(group),
        )

    @staticmethod
    def _compute_confidence(profiles: list[CompanyProfile]) -> float:
        sources = {p.source for p in profiles}
        if not profiles:
            return 0.0
        avg_base = sum(p.confidence for p in profiles) / len(profiles)
        corroboration_boost = CORROBORATION_BOOST_PER_SOURCE * (len(sources) - 1)
        return min(1.0, max(0.0, avg_base + corroboration_boost))

    # -- Helpers ------------------------------------------------------------

    @staticmethod
    def _normalize_name(name: str) -> str:
        return re.sub(r"\s+", " ", (name or "").strip().lower())

    @staticmethod
    def _normalize_postcode(postcode: str) -> str:
        return (postcode or "").strip().upper().replace(" ", "")

    @staticmethod
    def _pick_non_empty(values: list[Any], default: Any = None) -> Any:
        for value in values:
            if value is None:
                continue
            if isinstance(value, str) and not value.strip():
                continue
            return value
        return default

    def _new_stats(
        self, query: PostcodeSearchQuery | TownSearchQuery, location: PostcodeResult | TownResult
    ) -> ScrapeStats:
        return ScrapeStats(
            query=query.to_dict(),
            location=self._location_to_dict(location),
            sources={},
            total_raw=0,
            total_unique=0,
            errors=[],
        )

    def _log_results(self, stats: ScrapeStats, sync: bool) -> None:
        mode = "sync" if sync else "async"
        logger.info(
            "[%s] Scrape complete: %d raw profiles, %d unique profiles",
            mode,
            stats.total_raw,
            stats.total_unique,
        )
        for source, count in stats.sources.items():
            if stats.total_raw:
                rate = count / stats.total_raw
            else:
                rate = 0.0
            logger.info(
                "[%s] Source '%s' hit rate: %d/%d (%.0f%%)",
                mode,
                source,
                count,
                stats.total_raw,
                rate * 100.0,
            )
