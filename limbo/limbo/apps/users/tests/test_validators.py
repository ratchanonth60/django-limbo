import unittest

from django.core.exceptions import ValidationError

from limbo.apps.users.validators import (
    PasswordStrongValidator,
)


class PasswordStrongValidatorTestCase(unittest.TestCase):
    def setUp(self):
        self.validator = PasswordStrongValidator()

    # Test cases for valid passwords
    def test_valid_password_all_requirements_met(self):
        """Password that meets all requirements should pass."""
        password = "Aa1@abcd"
        try:
            self.validator.validate(password)
        except ValidationError:
            self.fail(f"ValidationError raised for valid password '{password}'")

    def test_valid_password_longer_length(self):
        """Password longer than 8 characters should pass."""
        password = "Aa1@abcdefghijk"
        try:
            self.validator.validate(password)
        except ValidationError:
            self.fail(f"ValidationError raised for valid password '{password}'")

    def test_valid_password_multiple_special_characters(self):
        """Password with multiple special characters should pass."""
        password = "Aa1!@#abcd"
        try:
            self.validator.validate(password)
        except ValidationError:
            self.fail(f"ValidationError raised for valid password '{password}'")

    def test_valid_password_upper_lower_digit_special(self):
        """Password with upper, lower, digit, and special character should pass."""
        password = "Passw0rd!"
        try:
            self.validator.validate(password)
        except ValidationError:
            self.fail(f"ValidationError raised for valid password '{password}'")

    def test_valid_password_special_characters_in_middle(self):
        """Password with special character in the middle should pass."""
        password = "Abcde1@fgh"
        try:
            self.validator.validate(password)
        except ValidationError:
            self.fail(f"ValidationError raised for valid password '{password}'")

    # Test cases for invalid passwords
    def test_invalid_password_too_short(self):
        """Password less than 8 characters should fail."""
        password = "Aa1@abc"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        self.assertEqual(
            str(cm.exception), str(["Password must be at least 8 characters long."])
        )

    def test_invalid_password_no_uppercase(self):
        """Password without uppercase letters should fail."""
        password = "aa1@abcd"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        self.assertEqual(
            str(cm.exception),
            str(["Password must contain at least one uppercase letter (A-Z)."]),
        )

    def test_invalid_password_no_lowercase(self):
        """Password without lowercase letters should fail."""
        password = "AA1@ABCD"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        self.assertEqual(
            str(cm.exception),
            str(["Password must contain at least one lowercase letter (a-z)."]),
        )

    def test_invalid_password_no_digit(self):
        """Password without digits should fail."""
        password = "Aa@bcdefg"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        self.assertEqual(
            str(cm.exception), str(["Password must contain at least one digit (0-9)."])
        )

    def test_invalid_password_no_special_character(self):
        """Password without special characters should fail."""
        password = "Aa1bcdefg"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        self.assertEqual(
            str(cm.exception),
            str(
                [
                    "Password must contain at least one special character, such as @, #, $, %, &, or *."
                ]
            ),
        )

    def test_invalid_password_all_lowercase(self):
        """Password with all lowercase letters should fail."""
        password = "password1@"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        # Should raise error for missing uppercase letter
        self.assertEqual(
            str(cm.exception),
            str(["Password must contain at least one uppercase letter (A-Z)."]),
        )

    def test_invalid_password_all_uppercase(self):
        """Password with all uppercase letters should fail."""
        password = "PASSWORD1@"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        # Should raise error for missing lowercase letter
        self.assertEqual(
            str(cm.exception),
            str(["Password must contain at least one lowercase letter (a-z)."]),
        )

    def test_invalid_password_only_letters_and_digits(self):
        """Password without special characters should fail."""
        password = "Password1"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        self.assertIn("special character", str(cm.exception))

    def test_invalid_password_only_letters_and_special_chars(self):
        """Password without digits should fail."""
        password = "Password@"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        self.assertIn("digit", str(cm.exception))

    def test_invalid_password_only_digits_and_special_chars(self):
        """Password without letters should fail."""
        password = "1234567@"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        # Should raise error for missing uppercase letter first
        self.assertIn("uppercase letter", str(cm.exception))

    def test_invalid_password_spaces_in_password(self):
        """Password with spaces should be treated accordingly."""
        password = "Aa1@ abcd"
        try:
            self.validator.validate(password)
        except ValidationError as e:
            self.fail(
                f"ValidationError raised for password with spaces '{password}': {e}"
            )

    def test_valid_password_with_allowed_special_chars(self):
        """Password with allowed special characters should pass."""
        password = "Aa1&abcd"
        try:
            self.validator.validate(password)
        except ValidationError:
            self.fail(f"ValidationError raised for valid password '{password}'")

    def test_valid_password_with_long_length(self):
        """Password significantly longer than 8 characters should pass."""
        password = "Aa1@" + "a" * 100
        try:
            self.validator.validate(password)
        except ValidationError:
            self.fail(f"ValidationError raised for long valid password '{password}'")

    def test_invalid_password_empty_string(self):
        """Empty password should fail."""
        password = ""
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        self.assertEqual(
            str(cm.exception), str(["Password must be at least 8 characters long."])
        )

    def test_invalid_password_none(self):
        """None as password should raise TypeError."""
        password = None
        with self.assertRaises(TypeError):
            self.validator.validate(password)

    def test_invalid_password_non_string(self):
        """Non-string password should raise TypeError."""
        password = 12345678
        with self.assertRaises(TypeError):
            self.validator.validate(password)

    def test_invalid_password_multiple_errors(self):
        """Password failing multiple checks should raise first error."""
        password = "password"
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate(password)
        # Should raise error for missing uppercase letter first
        self.assertEqual(
            str(cm.exception),
            str(["Password must contain at least one uppercase letter (A-Z)."]),
        )

    def test_get_help_text(self):
        """Test that get_help_text returns the correct help message."""
        expected_help_text = (
            "Your password must contain at least 8 characters, "
            "include both uppercase and lowercase letters, "
            "contain at least one digit, and at least one special character "
            "such as @, #, $, %, &, or *."
        )
        self.assertEqual(self.validator.get_help_text(), expected_help_text)
