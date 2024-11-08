from unittest import TestCase

from django.core.exceptions import ValidationError

from limbo.apps.address.validators import validate_postal_code


class TestValidatePostalCode(TestCase):
    def test_no_country_code(self):
        with self.assertRaises(ValidationError) as cm:
            validate_postal_code("12345", "")
        self.assertEqual(
            str(cm.exception),
            str(["Country must be specified to validate postal code."]),
        )

    def test_no_postal_code_required(self):
        # Assume that country 'XX' does not require a postal code
        with self.assertRaises(ValidationError) as cm:
            validate_postal_code("12345", "XX")
        self.assertEqual(
            str(cm.exception),
            str(["This country does not use postal codes. Please leave it blank."]),
        )

    def test_valid_us_postal_code(self):
        try:
            validate_postal_code("12345", "US")  # Valid US postal code
        except ValidationError:
            self.fail("validate_postal_code() raised ValidationError unexpectedly!")

    def test_valid_us_postal_code_with_extension(self):
        try:
            validate_postal_code(
                "12345-6789", "US"
            )  # Valid US postal code with extension
        except ValidationError:
            self.fail("validate_postal_code() raised ValidationError unexpectedly!")

    def test_invalid_us_postal_code(self):
        with self.assertRaises(ValidationError) as cm:
            validate_postal_code("1234", "US")  # Invalid US postal code
        self.assertEqual(
            str(cm.exception), str(["Invalid postal code format for country US."])
        )

    def test_invalid_gb_postal_code(self):
        with self.assertRaises(ValidationError) as cm:
            validate_postal_code("12345", "GB")  # Invalid UK postal code
        self.assertEqual(
            str(cm.exception), str(["Invalid postal code format for country GB."])
        )

    def test_invalid_ca_postal_code(self):
        with self.assertRaises(ValidationError) as cm:
            validate_postal_code("12345", "CA")  # Invalid Canadian postal code
        self.assertEqual(
            str(cm.exception), str(["Invalid postal code format for country CA."])
        )

    def test_postal_code_required(self):
        with self.assertRaises(ValidationError) as cm:
            validate_postal_code(
                "", "US"
            )  # Postal code required for US but not provided
        self.assertEqual(
            str(cm.exception),
            str(["Postal code is required for the selected country."]),
        )
