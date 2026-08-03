import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from scraper.models.company import (
    CompanyProfile,
    CompanySearchQuery,
    PostcodeSearchQuery,
    TownSearchQuery,
)


class TestCompanyProfile(unittest.TestCase):
    def test_post_init_strips_whitespace(self):
        profile = CompanyProfile(
            company_name="  Acme Ltd  ",
            telephone=" 01234 567890 ",
            email="  INFO@ACME.COM  ",
            address="  1 High St  ",
            main_contact="  John Doe  ",
            business_type="  Retail  ",
            open_hours=None,
            postcode="cm11ht",
            town="  chelmsford  ",
            source="  companies_house  ",
            confidence=0.5,
        )
        self.assertEqual(profile.company_name, "Acme Ltd")
        self.assertEqual(profile.telephone, "01234 567890")
        self.assertEqual(profile.email, "info@acme.com")
        self.assertEqual(profile.address, "1 High St")
        self.assertEqual(profile.main_contact, "John Doe")
        self.assertEqual(profile.business_type, "Retail")
        self.assertEqual(profile.town, "chelmsford")
        self.assertEqual(profile.source, "companies_house")

    def test_post_init_standardises_postcode(self):
        profile = CompanyProfile(
            company_name="Test",
            telephone=None,
            email=None,
            address="",
            main_contact=None,
            business_type=None,
            open_hours=None,
            postcode="cm11ht",
            town="",
            source="",
            confidence=0.0,
        )
        self.assertEqual(profile.postcode, "CM1 1HT")

    def test_post_init_short_postcode(self):
        profile = CompanyProfile(
            company_name="Test",
            telephone=None,
            email=None,
            address="",
            main_contact=None,
            business_type=None,
            open_hours=None,
            postcode="ab",
            town="",
            source="",
            confidence=0.0,
        )
        self.assertEqual(profile.postcode, "AB")

    def test_post_init_clamps_confidence(self):
        profile = CompanyProfile(
            company_name="Test",
            telephone=None,
            email=None,
            address="",
            main_contact=None,
            business_type=None,
            open_hours=None,
            postcode="AB1 1AB",
            town="",
            source="",
            confidence=1.5,
        )
        self.assertEqual(profile.confidence, 1.0)

        profile2 = CompanyProfile(
            company_name="Test",
            telephone=None,
            email=None,
            address="",
            main_contact=None,
            business_type=None,
            open_hours=None,
            postcode="AB1 1AB",
            town="",
            source="",
            confidence=-0.5,
        )
        self.assertEqual(profile2.confidence, 0.0)

    def test_post_init_lowercases_open_hours_keys(self):
        profile = CompanyProfile(
            company_name="Test",
            telephone=None,
            email=None,
            address="",
            main_contact=None,
            business_type=None,
            open_hours={"Monday": "9-5", "TUESDAY": "10-6"},
            postcode="AB1 1AB",
            town="",
            source="",
            confidence=0.0,
        )
        self.assertIn("monday", profile.open_hours)
        self.assertIn("tuesday", profile.open_hours)
        self.assertEqual(profile.open_hours["monday"], "9-5")

    def test_to_dict(self):
        profile = CompanyProfile(
            company_name="Acme",
            telephone="123",
            email="a@b.com",
            address="1 High St",
            main_contact="John",
            business_type="Retail",
            open_hours={"monday": "9-5"},
            postcode="AB1 1AB",
            town="Town",
            source="companies_house",
            confidence=0.8,
        )
        d = profile.to_dict()
        self.assertEqual(d["company_name"], "Acme")
        self.assertEqual(d["telephone"], "123")
        self.assertEqual(d["email"], "a@b.com")
        self.assertEqual(d["confidence"], 0.8)
        self.assertEqual(d["open_hours"], {"monday": "9-5"})

    def test_to_csv_row(self):
        profile = CompanyProfile(
            company_name="Acme",
            telephone="123",
            email="a@b.com",
            address="1 High St",
            main_contact="John",
            business_type="Retail",
            open_hours={"monday": "9-5"},
            postcode="AB1 1AB",
            town="Town",
            source="companies_house",
            confidence=0.85,
        )
        row = profile.to_csv_row()
        self.assertEqual(row[0], "Acme")
        self.assertEqual(row[1], "123")
        self.assertEqual(row[2], "a@b.com")
        self.assertEqual(row[3], "1 High St")
        self.assertEqual(row[6], json.dumps({"monday": "9-5"}, ensure_ascii=False))
        self.assertEqual(row[7], "AB1 1AB")
        self.assertEqual(row[10], "0.85")

    def test_to_csv_row_none_values(self):
        profile = CompanyProfile(
            company_name="Acme",
            telephone=None,
            email=None,
            address="1 High St",
            main_contact=None,
            business_type=None,
            open_hours=None,
            postcode="AB1 1AB",
            town="Town",
            source="companies_house",
            confidence=0.0,
        )
        row = profile.to_csv_row()
        self.assertEqual(row[1], "")
        self.assertEqual(row[2], "")
        self.assertEqual(row[5], "")
        self.assertEqual(row[6], "")

    def test_from_dict(self):
        data = {
            "company_name": "Acme",
            "telephone": "123",
            "email": "a@b.com",
            "address": "1 High St",
            "main_contact": "John",
            "business_type": "Retail",
            "open_hours": {"monday": "9-5"},
            "postcode": "AB1 1AB",
            "town": "Town",
            "source": "companies_house",
            "confidence": 0.8,
        }
        profile = CompanyProfile.from_dict(data)
        self.assertEqual(profile.company_name, "Acme")
        self.assertEqual(profile.telephone, "123")
        self.assertEqual(profile.postcode, "AB1 1AB")
        self.assertEqual(profile.confidence, 0.8)

    def test_from_dict_defaults(self):
        profile = CompanyProfile.from_dict({})
        self.assertEqual(profile.company_name, "")
        self.assertEqual(profile.address, "")
        self.assertEqual(profile.telephone, None)
        self.assertEqual(profile.confidence, 0.0)
        self.assertEqual(profile.postcode, "")

    def test_round_trip_to_dict_from_dict(self):
        original = CompanyProfile(
            company_name="Acme Ltd",
            telephone="01234 567890",
            email="info@acme.com",
            address="1 High St, Town",
            main_contact="John Doe",
            business_type="Retail",
            open_hours={"monday": "09:00 - 17:00"},
            postcode="AB1 1AB",
            town="Town",
            source="google_places",
            confidence=0.9,
        )
        restored = CompanyProfile.from_dict(original.to_dict())
        self.assertEqual(restored.company_name, "Acme Ltd")
        self.assertEqual(restored.telephone, "01234 567890")
        self.assertEqual(restored.email, "info@acme.com")
        self.assertEqual(restored.postcode, "AB1 1AB")
        self.assertEqual(restored.confidence, 0.9)
        self.assertEqual(restored.open_hours, {"monday": "09:00 - 17:00"})

    def test_none_email_becomes_none(self):
        profile = CompanyProfile(
            company_name="Test",
            telephone=None,
            email=None,
            address="",
            main_contact=None,
            business_type=None,
            open_hours=None,
            postcode="AB1 1AB",
            town="",
            source="",
            confidence=0.0,
        )
        self.assertIsNone(profile.email)

    def test_postcode_standardise_various_formats(self):
        cases = [
            ("ab12cd", "AB1 2CD"),
            ("AB123CD", "AB12 3CD"),
            (" a b 1 2 c d ", "AB1 2CD"),
            ("SW1A1AA", "SW1A 1AA"),
        ]
        for inp, expected in cases:
            with self.subTest(inp=inp):
                profile = CompanyProfile(
                    company_name="T",
                    telephone=None,
                    email=None,
                    address="",
                    main_contact=None,
                    business_type=None,
                    open_hours=None,
                    postcode=inp,
                    town="",
                    source="",
                    confidence=0.0,
                )
                self.assertEqual(profile.postcode, expected)


class TestPostcodeSearchQuery(unittest.TestCase):
    def test_valid_query(self):
        q = PostcodeSearchQuery(postcode="AB1 1AB")
        self.assertTrue(q.is_valid())
        self.assertEqual(q.to_dict()["postcode"], "AB11AB")
        self.assertEqual(q.to_dict()["radius_km"], 1.0)

    def test_strips_and_uppercases_postcode(self):
        q = PostcodeSearchQuery(postcode=" ab1 1ab ", radius_km=5.0)
        self.assertEqual(q.postcode, "AB11AB")
        self.assertEqual(q.radius_km, 5.0)

    def test_min_radius(self):
        q = PostcodeSearchQuery(postcode="AB1 1AB", radius_km=0.01)
        self.assertEqual(q.radius_km, 0.1)

    def test_invalid_query(self):
        q = PostcodeSearchQuery(postcode="")
        self.assertFalse(q.is_valid())


class TestTownSearchQuery(unittest.TestCase):
    def test_valid_query(self):
        q = TownSearchQuery(town="Chelmsford")
        self.assertTrue(q.is_valid())

    def test_strips_town(self):
        q = TownSearchQuery(town="  Chelmsford  ", radius_km=15.0)
        self.assertEqual(q.town, "Chelmsford")
        self.assertEqual(q.radius_km, 15.0)

    def test_min_radius(self):
        q = TownSearchQuery(town="Town", radius_km=0.01)
        self.assertEqual(q.radius_km, 0.1)

    def test_invalid_query(self):
        q = TownSearchQuery(town="")
        self.assertFalse(q.is_valid())


class TestCompanySearchQuery(unittest.TestCase):
    def test_valid_with_town(self):
        q = CompanySearchQuery(town="Chelmsford")
        self.assertTrue(q.is_valid())

    def test_valid_with_postcode(self):
        q = CompanySearchQuery(postcode="AB1 1AB")
        self.assertTrue(q.is_valid())

    def test_invalid_empty(self):
        q = CompanySearchQuery()
        self.assertFalse(q.is_valid())

    def test_to_dict(self):
        q = CompanySearchQuery(town="Chelmsford", postcode="AB11AB", radius_km=5.0)
        d = q.to_dict()
        self.assertEqual(d["town"], "Chelmsford")
        self.assertEqual(d["postcode"], "AB11AB")
        self.assertEqual(d["radius_km"], 5.0)
