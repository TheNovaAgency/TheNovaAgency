import json
from dataclasses import dataclass
from typing import Any


@dataclass
class CompanyProfile:
    company_name: str
    telephone: str | None
    email: str | None
    address: str
    main_contact: str | None
    business_type: str | None
    open_hours: dict | None
    postcode: str
    town: str
    source: str
    confidence: float

    def __post_init__(self) -> None:
        self.company_name = self.company_name.strip()
        self.address = self.address.strip()
        self.town = self.town.strip()
        self.postcode = self._standardise_postcode(self.postcode)
        self.source = self.source.strip()
        self.telephone = self.telephone.strip() if self.telephone is not None else None
        self.email = self.email.lower().strip() if self.email is not None else None
        self.main_contact = self.main_contact.strip() if self.main_contact is not None else None
        self.business_type = self.business_type.strip() if self.business_type is not None else None
        self.confidence = max(0.0, min(1.0, float(self.confidence)))
        if self.open_hours is not None:
            self.open_hours = {k.strip().lower(): v for k, v in self.open_hours.items()}

    @staticmethod
    def _standardise_postcode(postcode: str) -> str:
        cleaned = postcode.strip().upper().replace(" ", "")
        if len(cleaned) < 3:
            return cleaned
        outward = cleaned[:-3]
        inward = cleaned[-3:]
        return f"{outward} {inward}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "company_name": self.company_name,
            "telephone": self.telephone,
            "email": self.email,
            "address": self.address,
            "main_contact": self.main_contact,
            "business_type": self.business_type,
            "open_hours": self.open_hours,
            "postcode": self.postcode,
            "town": self.town,
            "source": self.source,
            "confidence": self.confidence,
        }

    def to_csv_row(self) -> list[str]:
        return [
            self.company_name,
            self.telephone or "",
            self.email or "",
            self.address,
            self.main_contact or "",
            self.business_type or "",
            json.dumps(self.open_hours, ensure_ascii=False) if self.open_hours is not None else "",
            self.postcode,
            self.town,
            self.source,
            f"{self.confidence:.2f}",
        ]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CompanyProfile":
        return cls(
            company_name=data.get("company_name", ""),
            telephone=data.get("telephone"),
            email=data.get("email"),
            address=data.get("address", ""),
            main_contact=data.get("main_contact"),
            business_type=data.get("business_type"),
            open_hours=data.get("open_hours"),
            postcode=data.get("postcode", ""),
            town=data.get("town", ""),
            source=data.get("source", ""),
            confidence=data.get("confidence", 0.0),
        )


@dataclass
class CompanySearchQuery:
    town: str | None = None
    postcode: str | None = None
    radius_km: float = 10.0

    def __post_init__(self) -> None:
        if self.town is not None:
            self.town = self.town.strip()
        if self.postcode is not None:
            self.postcode = self.postcode.strip().upper().replace(" ", "")
        self.radius_km = max(0.1, float(self.radius_km))

    def is_valid(self) -> bool:
        return bool(self.town or self.postcode)

    def to_dict(self) -> dict[str, Any]:
        return {
            "town": self.town,
            "postcode": self.postcode,
            "radius_km": self.radius_km,
        }