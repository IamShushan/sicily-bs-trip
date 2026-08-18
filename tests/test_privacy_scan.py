import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "privacy_scan.py"
SPEC = importlib.util.spec_from_file_location("privacy_scan", MODULE_PATH)
assert SPEC and SPEC.loader
privacy_scan = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = privacy_scan
SPEC.loader.exec_module(privacy_scan)


class PrivacyScanTests(unittest.TestCase):
    def categories(self, text: str) -> set[str]:
        return {finding.category for finding in privacy_scan.scan_text(text, "fixture.txt")}

    def test_detects_luhn_valid_payment_card(self) -> None:
        synthetic_card = "4242" + " 4242" * 3
        self.assertIn("payment-card number", self.categories(synthetic_card))

    def test_detects_checksum_valid_israeli_id_with_context(self) -> None:
        synthetic_id = "123" + "456" + "782"
        self.assertIn("Israeli identity number", self.categories(f"תעודת זהות: {synthetic_id}"))

    def test_detects_contextual_travel_identifiers(self) -> None:
        text = "Passport number: AB12" + "3456\nPNR: ZX9" + "8QW"
        categories = self.categories(text)
        self.assertIn("passport number", categories)
        self.assertIn("booking reference", categories)

    def test_detects_credentials_without_echoing_the_value(self) -> None:
        secret = "api_key=" + "synth" + "etic_value_123456789"
        self.assertIn("credential", self.categories(secret))

        output = io.StringIO()
        findings = privacy_scan.scan_text(secret, "fixture.txt")
        with redirect_stderr(output):
            privacy_scan.print_findings(findings)
        self.assertNotIn(secret, output.getvalue())
        self.assertIn("[REDACTED]", output.getvalue())

    def test_blocks_private_but_allows_official_business_email(self) -> None:
        personal = "traveler" + "@gmail.com"
        self.assertIn("private email address", self.categories(personal))
        self.assertNotIn("private email address", self.categories("info@cantinegulino.it"))

    def test_policy_wording_is_not_a_booking_reference(self) -> None:
        self.assertNotIn(
            "booking reference", self.categories("Booking references רגישים אסורים")
        )

    def test_allows_itinerary_numbers(self) -> None:
        text = "W46528, 26.11.2026, 17:15, €54, נסיעה של 35–40 דקות"
        self.assertEqual(set(), self.categories(text))

    def test_blocks_private_document_and_image_types(self) -> None:
        for path in ("ticket.pdf", "passport.jpg", "booking.xlsx"):
            with self.subTest(path=path):
                self.assertTrue(privacy_scan.scan_blob(path, b"synthetic"))

    def test_blocks_unrecognized_binary_data(self) -> None:
        findings = privacy_scan.scan_blob("artifact.dat", b"prefix\x00suffix")
        self.assertEqual("binary file", findings[0].category)


if __name__ == "__main__":
    unittest.main()
