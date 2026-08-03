import csv
import io
import json
import logging
import os
from enum import Enum
from pathlib import Path
from typing import IO, Any, Iterable, Sequence

from scraper.models.company import CompanyProfile

logger = logging.getLogger(__name__)

CSV_FIELDS: list[str] = [
    "company_name",
    "telephone",
    "email",
    "address",
    "main_contact",
    "business_type",
    "open_hours",
    "postcode",
    "town",
    "source",
    "confidence",
]


class ExportFormat(Enum):
    CSV = "csv"
    JSON = "json"
    JSONL = "jsonl"


class ExportError(Exception):
    """Raised when exporting profiles fails."""


def _resolve_profiles(profiles: Iterable[CompanyProfile]) -> list[CompanyProfile]:
    if profiles is None:
        raise ExportError("profiles must not be None")
    resolved = list(profiles)
    for profile in resolved:
        if not isinstance(profile, CompanyProfile):
            raise ExportError(
                f"Expected CompanyProfile instances, got {type(profile).__name__}"
            )
    return resolved


def _dict_for_export(profile: CompanyProfile) -> dict[str, Any]:
    data = profile.to_dict()
    return data


def _csv_rows(profiles: Sequence[CompanyProfile]) -> list[list[str]]:
    return [profile.to_csv_row() for profile in profiles]


def _write_output(output: Any, content: str) -> str | None:
    if output is None:
        return content
    if isinstance(output, (str, os.PathLike)) or hasattr(output, "write"):
        if isinstance(output, (str, os.PathLike)):
            path = Path(output)
            with open(path, "w", encoding="utf-8", newline="", errors="strict") as handle:
                handle.write(content)
            logger.info("Wrote %d byte(s) to %s", len(content), path)
            return None
        if hasattr(output, "write"):
            output.write(content)
            logger.info("Wrote %d byte(s) to buffer %s", len(content), type(output).__name__)
            return None
    raise ExportError(
        "output must be None, a file path (str/PathLike) or a writable buffer, "
        f"got {type(output).__name__}"
    )


def export_csv(profiles: Iterable[CompanyProfile], output: Any = None) -> str | None:
    resolved = _resolve_profiles(profiles)
    buffer = io.StringIO()
    writer = csv.writer(buffer, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    writer.writerow(CSV_FIELDS)
    for row in _csv_rows(resolved):
        writer.writerow(row)
    return _write_output(output, buffer.getvalue())


def export_json(
    profiles: Iterable[CompanyProfile],
    output: Any = None,
    *,
    newline_delimited: bool = False,
) -> str | None:
    resolved = _resolve_profiles(profiles)
    if newline_delimited:
        parts = [
            json.dumps(_dict_for_export(profile), ensure_ascii=False)
            for profile in resolved
        ]
        content = "".join(f"{part}\n" for part in parts)
    else:
        payload = [_dict_for_export(profile) for profile in resolved]
        content = json.dumps(payload, ensure_ascii=False, indent=2)
        if resolved:
            content += "\n"
    return _write_output(output, content)


def export(
    profiles: Iterable[CompanyProfile],
    format: ExportFormat,
    output: Any = None,
    *,
    newline_delimited: bool = False,
) -> str | None:
    if isinstance(format, str):
        try:
            fmt = ExportFormat(format.lower())
        except ValueError as exc:
            raise ExportError(
                f"Unknown export format: {format!r}. "
                f"Expected one of {[f.value for f in ExportFormat]}"
            ) from exc
    elif isinstance(format, ExportFormat):
        fmt = format
    else:
        raise ExportError(
            f"format must be an ExportFormat or str, got {type(format).__name__}"
        )

    if fmt is ExportFormat.CSV:
        if newline_delimited:
            logger.warning("newline_delimited is ignored for CSV format")
        return export_csv(profiles, output)
    if fmt is ExportFormat.JSONL:
        return export_json(profiles, output, newline_delimited=True)
    return export_json(profiles, output, newline_delimited=newline_delimited)


def summary_stats(profiles: Iterable[CompanyProfile]) -> dict[str, Any]:
    resolved = _resolve_profiles(profiles)
    count = len(resolved)

    sources_used: set[str] = set()
    for profile in resolved:
        source_field = profile.source or ""
        for source in source_field.split(","):
            source = source.strip()
            if source:
                sources_used.add(source)

    confidence_distribution: dict[str, int] = {}
    for index in range(10):
        lower = index / 10.0
        upper = lower + 0.1
        confidence_distribution[f"{lower:.1f}-{upper:.1f}"] = 0

    for profile in resolved:
        confidence = max(0.0, min(1.0, float(profile.confidence)))
        bucket = min(int(confidence * 10), 9)
        lower = bucket / 10.0
        upper = (bucket + 1) / 10.0
        key = f"{lower:.1f}-{upper:.1f}"
        confidence_distribution[key] += 1

    if resolved:
        mean_confidence = sum(float(p.confidence) for p in resolved) / count
        min_confidence = min(float(p.confidence) for p in resolved)
        max_confidence = max(float(p.confidence) for p in resolved)
    else:
        mean_confidence = 0.0
        min_confidence = 0.0
        max_confidence = 0.0

    return {
        "count": count,
        "sources_used": sorted(sources_used),
        "confidence_distribution": confidence_distribution,
        "mean_confidence": round(mean_confidence, 4),
        "min_confidence": min_confidence,
        "max_confidence": max_confidence,
    }
