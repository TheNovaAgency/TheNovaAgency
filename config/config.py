import os
from dataclasses import dataclass, field
from dotenv import load_dotenv


load_dotenv()


@dataclass
class ScraperConfig:
    COMPANIES_HOUSE_API_KEY: str = field(default_factory=lambda: os.getenv("COMPANIES_HOUSE_API_KEY", ""))
    GOOGLE_PLACES_API_KEY: str = field(default_factory=lambda: os.getenv("GOOGLE_PLACES_API_KEY", ""))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    COMPANIES_HOUSE_RATE_LIMIT: int = int(os.getenv("COMPANIES_HOUSE_RATE_LIMIT", "60"))
    GOOGLE_PLACES_RATE_LIMIT: int = int(os.getenv("GOOGLE_PLACES_RATE_LIMIT", "100"))
    DEFAULT_RADIUS_KM: float = float(os.getenv("DEFAULT_RADIUS_KM", "10.0"))
    GEOCODING_CACHE_PATH: str = os.getenv("GEOCODING_CACHE_PATH", "config/geocoding_cache.json")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output")
    DEFAULT_TOWN: str = os.getenv("DEFAULT_TOWN", "Chelmsford")
    DEFAULT_POSTCODE: str = os.getenv("DEFAULT_POSTCODE", "CM1 1HT")

    def validate(self) -> None:
        missing = []
        if not self.COMPANIES_HOUSE_API_KEY:
            missing.append("COMPANIES_HOUSE_API_KEY")
        if not self.GOOGLE_PLACES_API_KEY:
            missing.append("GOOGLE_PLACES_API_KEY")
        if missing:
            raise ValueError(f"Missing required API keys: {', '.join(missing)}. Set them in .env or environment variables.")


config = ScraperConfig()
