import csv
import json
import sys
import unittest
from io import StringIO
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


class TestExportCsv(unittest.TestCase):
    def test_export_csv_to_string(self):
        from scraper.export.exporter import export_csv
        profiles = [make_profile("Acme", "AB1 1AB", town="Town", telephone="123", email="a@b.com", business_type="Retail", confidence=0.9)]
        result = export_csv(profiles)
        self.assertIsInstance(result, str)
        self.assertIn("company_name", result)
        self.assertIn("Acme", result)

    def test_export_csv_header(self):
        from scraper.export.exporter import export_csv, CSV_FIELDS
        profiles = []
        result = export_csv(profiles)
        reader = csv.reader(StringIO(result))
        header = next(reader)
        self.assertEqual(header, CSV_FIELDS)

    def test_export_csv_row_values(self):
        from scraper.export.exporter import export_csv
        profiles = [make_profile("Acme", "AB1 1AB", telephone="123", email="a@b.com", address="1 High St", business_type="Retail", open_hours={"monday": "9-5"}, confidence=0.85)]
        result = export_csv(profiles)
        reader = csv.reader(StringIO(result))
        rows = list(reader)
        self.assertEqual(len(rows), 2)
        data_row = rows[1]
        self.assertEqual(data_row[0], "Acme")
        self.assertEqual(data_row[1], "123")
        self.assertEqual(data_row[2], "a@b.com")
        self.assertEqual(data_row[7], "AB1 1AB")
        self.assertEqual(data_row[10], "0.85")

    def test_export_csv_none_values_as_empty(self):
        from scraper.export.exporter import export_csv
        profiles = [make_profile("Acme", "AB1 1AB")]
        result = export_csv(profiles)
        reader = csv.reader(StringIO(result))
        rows = list(reader)
        data_row = rows[1]
        self.assertEqual(data_row[1], "")
        self.assertEqual(data_row[2], "")
        self.assertEqual(data_row[5], "")
        self.assertEqual(data_row[6], "")

    def test_export_csv_to_file(self):
        from scraper.export.exporter import export_csv
        import tempfile
        profiles = [make_profile("Acme", "AB1 1AB")]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            path = f.name
        try:
            export_csv(profiles, output=path)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Acme", content)
        finally:
            Path(path).unlink(missing_ok=True)

    def test_export_csv_multiple_profiles(self):
        from scraper.export.exporter import export_csv
        profiles = [
            make_profile("Acme", "AB1 1AB", town="TownA"),
            make_profile("Beta", "CD2 2CD", town="TownB"),
        ]
        result = export_csv(profiles)
        reader = csv.reader(StringIO(result))
        rows = list(reader)
        self.assertEqual(len(rows), 3)


class TestExportJson(unittest.TestCase):
    def test_export_json_to_string(self):
        from scraper.export.exporter import export_json
        profiles = [make_profile("Acme", "AB1 1AB", confidence=0.9)]
        result = export_json(profiles)
        self.assertIsInstance(result, str)
        data = json.loads(result)
        self.assertIsInstance(data, list)
        self.assertEqual(data[0]["company_name"], "Acme")

    def test_export_json_newline_delimited(self):
        from scraper.export.exporter import export_json
        profiles = [
            make_profile("Acme", "AB1 1AB"),
            make_profile("Beta", "CD2 2CD"),
        ]
        result = export_json(profiles, newline_delimited=True)
        lines = result.strip().split("\n")
        self.assertEqual(len(lines), 2)
        first = json.loads(lines[0])
        self.assertEqual(first["company_name"], "Acme")

    def test_export_json_to_file(self):
        from scraper.export.exporter import export_json
        import tempfile
        profiles = [make_profile("Acme", "AB1 1AB")]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name
        try:
            export_json(profiles, output=path)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data[0]["company_name"], "Acme")
        finally:
            Path(path).unlink(missing_ok=True)

    def test_export_json_empty_profiles(self):
        from scraper.export.exporter import export_json
        result = export_json([])
        self.assertEqual(result, "[]")


class TestExport(unittest.TestCase):
    def test_export_csv_format(self):
        from scraper.export.exporter import export, ExportFormat
        profiles = [make_profile("Acme", "AB1 1AB")]
        result = export(profiles, ExportFormat.CSV)
        self.assertIn("Acme", result)
        self.assertIn("company_name", result)

    def test_export_json_format(self):
        from scraper.export.exporter import export, ExportFormat
        profiles = [make_profile("Acme", "AB1 1AB")]
        result = export(profiles, ExportFormat.JSON)
        data = json.loads(result)
        self.assertEqual(data[0]["company_name"], "Acme")

    def test_export_jsonl_format(self):
        from scraper.export.exporter import export, ExportFormat
        profiles = [make_profile("Acme", "AB1 1AB")]
        result = export(profiles, ExportFormat.JSONL)
        lines = result.strip().split("\n")
        self.assertEqual(len(lines), 1)

    def test_export_string_format_csv(self):
        from scraper.export.exporter import export
        profiles = [make_profile("Acme", "AB1 1AB")]
        result = export(profiles, "csv")
        self.assertIn("Acme", result)

    def test_export_string_format_json(self):
        from scraper.export.exporter import export
        profiles = [make_profile("Acme", "AB1 1AB")]
        result = export(profiles, "json")
        data = json.loads(result)
        self.assertEqual(data[0]["company_name"], "Acme")

    def test_export_invalid_format(self):
        from scraper.export.exporter import export, ExportError
        profiles = [make_profile("Acme", "AB1 1AB")]
        with self.assertRaises(ExportError):
            export(profiles, "invalid_format")

    def test_export_invalid_format_type(self):
        from scraper.export.exporter import export, ExportError
        profiles = [make_profile("Acme", "AB1 1AB")]
        with self.assertRaises(ExportError):
            export(profiles, 123)

    def test_export_none_profiles(self):
        from scraper.export.exporter import export, ExportError
        with self.assertRaises(ExportError):
            export(None, "csv")

    def test_export_non_profile_raises(self):
        from scraper.export.exporter import export, ExportError
        with self.assertRaises(ExportError):
            export(["not a profile"], "csv")


class TestSummaryStats(unittest.TestCase):
    def test_summary_empty(self):
        from scraper.export.exporter import summary_stats
        stats = summary_stats([])
        self.assertEqual(stats["count"], 0)
        self.assertEqual(stats["sources_used"], [])
        self.assertEqual(stats["mean_confidence"], 0.0)

    def test_summary_with_profiles(self):
        from scraper.export.exporter import summary_stats
        profiles = [
            make_profile("A", "AB1 1AB", source="companies_house", confidence=0.8),
            make_profile("B", "CD2 2CD", source="google_places", confidence=0.6),
        ]
        stats = summary_stats(profiles)
        self.assertEqual(stats["count"], 2)
        self.assertIn("companies_house", stats["sources_used"])
        self.assertIn("google_places", stats["sources_used"])
        self.assertAlmostEqual(stats["mean_confidence"], 0.7)
        self.assertEqual(stats["min_confidence"], 0.6)
        self.assertEqual(stats["max_confidence"], 0.8)

    def test_summary_confidence_distribution(self):
        from scraper.export.exporter import summary_stats
        profiles = [make_profile("A", "AB1 1AB", confidence=0.85)]
        stats = summary_stats(profiles)
        self.assertEqual(stats["count"], 1)
        self.assertEqual(stats["confidence_distribution"]["0.8-0.9"], 1)

    def test_summary_combined_sources(self):
        from scraper.export.exporter import summary_stats
        profiles = [
            make_profile("A", "AB1 1AB", source="companies_house,google_places", confidence=0.8),
        ]
        stats = summary_stats(profiles)
        self.assertEqual(stats["count"], 1)
        self.assertIn("companies_house", stats["sources_used"])
        self.assertIn("google_places", stats["sources_used"])


class TestCsvFields(unittest.TestCase):
    def test_csv_fields_complete(self):
        from scraper.export.exporter import CSV_FIELDS
        expected = ["company_name", "telephone", "email", "address", "main_contact", "business_type", "open_hours", "postcode", "town", "source", "confidence"]
        self.assertEqual(CSV_FIELDS, expected)
