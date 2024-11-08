from django.core.exceptions import ValidationError
from django.test import TestCase

from marketEdge.factory.address.models import AddressFactory


class TestAddressModels(TestCase):
    def setUp(self):
        self.address = AddressFactory()

    # 1. Test string representation
    def test_address_str(self):
        self.assertEqual(
            str(self.address),
            f"{self.address.line1}, {self.address.city}, {self.address.state}, {self.address.country}",
        )

    # 2. Test flag_url method with default size
    def test_flag_url_default_size(self):
        self.assertEqual(
            self.address.flag_url(),
            f"https://flagsapi.com/{self.address.country.code.upper()}/flat/48.png",
        )

    # 3. Test flag_url method with custom size
    def test_flag_url_custom_size(self):
        self.assertEqual(
            self.address.flag_url(64),
            f"https://flagsapi.com/{self.address.country.code.upper()}/flat/64.png",
        )

    # 4. Test flag_url method when country is None
    def test_flag_url_with_no_country(self):
        self.address.country = None
        self.assertEqual(self.address.flag_url(), "")

    # 5. Test first name max length
    def test_first_name_max_length(self):
        max_length = self.address._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 255)

    # 6. Test last name max length
    def test_last_name_max_length(self):
        max_length = self.address._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 255)

    # 7. Test line1 max length
    def test_line1_max_length(self):
        max_length = self.address._meta.get_field("line1").max_length
        self.assertEqual(max_length, 255)

    # 8. Test line2 max length
    def test_line2_max_length(self):
        max_length = self.address._meta.get_field("line2").max_length
        self.assertEqual(max_length, 255)

    # 9. Test city max length
    def test_city_max_length(self):
        max_length = self.address._meta.get_field("city").max_length
        self.assertEqual(max_length, 255)

    # 10. Test state max length
    def test_state_max_length(self):
        max_length = self.address._meta.get_field("state").max_length
        self.assertEqual(max_length, 255)

    # 11. Test postal code max length
    def test_postal_code_max_length(self):
        max_length = self.address._meta.get_field("postal_code").max_length
        self.assertEqual(max_length, 20)

    # 12. Test phone number is optional
    def test_phone_number_optional(self):
        self.address.phone_number = None
        self.address.save()
        self.assertIsNone(self.address.phone_number)

    # 13. Test blank city allowed
    def test_blank_city(self):
        self.address.city = ""
        self.address.save()
        self.assertEqual(self.address.city, "")

    # 14. Test blank state allowed
    def test_blank_state(self):
        self.address.state = ""
        self.address.save()
        self.assertEqual(self.address.state, "")

    # 15. Test line2 is optional
    def test_line2_optional(self):
        self.address.line2 = ""
        self.address.save()
        self.assertEqual(self.address.line2, "")

    # 16. Test country is required
    def test_country_required(self):
        self.address.country = None
        with self.assertRaises(ValidationError):
            self.address.full_clean()

    # 17. Test invalid country code
    def test_invalid_country_code(self):
        self.address.country = "XYZ"
        with self.assertRaises(ValidationError):
            self.address.full_clean()

    # 18. Test title choices valid
    def test_title_choices(self):
        self.address.title = "Mr"
        self.address.full_clean(exclude=["phone_number"])  # should not raise exception

    # 19. Test invalid title choice
    def test_invalid_title_choice(self):
        self.address.title = "InvalidTitle"
        with self.assertRaises(ValidationError):
            self.address.full_clean()

    # 20. Test address creation with valid data
    def test_address_creation(self):
        address = AddressFactory()
        self.assertTrue(address.pk)  # Check if the instance is saved

    # 21. Test country field default blank label
    def test_country_blank_label(self):
        blank_label = self.address._meta.get_field("country").blank_label
        self.assertEqual(blank_label, "Select Country")

    # 22. Test title max length
    def test_title_max_length(self):
        max_length = self.address._meta.get_field("title").max_length
        self.assertEqual(max_length, 64)

    # 23. Test postal code is optional
    def test_postal_code_optional(self):
        self.address.postal_code = ""
        self.address.save()
        self.assertEqual(self.address.postal_code, "")

    # 24. Test address without postal code
    def test_address_without_postal_code(self):
        address = AddressFactory(postal_code="")
        self.assertEqual(address.postal_code, "")

    # 25. Test address without phone number
    def test_address_without_phone_number(self):
        address = AddressFactory(phone_number=None)
        self.assertIsNone(address.phone_number)

    # 27. Test country field blank allowed
    def test_country_field_blank(self):
        self.address.country = ""
        self.address.save()
        self.assertEqual(self.address.country, "")

    # 28. Test address without city
    def test_address_without_city(self):
        self.address.city = ""
        self.address.save()
        self.assertEqual(self.address.city, "")

    # 29. Test address without state
    def test_address_without_state(self):
        self.address.state = ""
        self.address.save()
        self.assertEqual(self.address.state, "")

    # 30. Test flag URL with lowercase country code
    def test_flag_url_lowercase_country(self):
        self.address.country = "us"
        self.assertEqual(self.address.flag_url(), "https://flagsapi.com/US/flat/48.png")

    # 31. Test flag URL with uppercase country code
    def test_flag_url_uppercase_country(self):
        self.address.country = "US"
        self.assertEqual(self.address.flag_url(), "https://flagsapi.com/US/flat/48.png")

    # 32. Test saving address with valid phone number
    def test_valid_phone_number(self):
        self.address.phone_number = "+11234567890"
        self.address.save()
        self.assertEqual(self.address.phone_number, "+11234567890")

    # 33. Test saving address with invalid phone number
    def test_invalid_phone_number(self):
        self.address.phone_number = "notaphone"
        with self.assertRaises(ValidationError):
            self.address.full_clean()

    # 34. Test city field blank is allowed
    def test_blank_city_allowed(self):
        self.address.city = ""
        self.address.save()
        self.assertEqual(self.address.city, "")

    # 35. Test state field blank is allowed
    def test_blank_state_allowed(self):
        self.address.state = ""
        self.address.save()
        self.assertEqual(self.address.state, "")

    # 36. Test that first_name is required
    def test_first_name_required(self):
        self.address.first_name = ""
        with self.assertRaises(ValidationError):
            self.address.full_clean()

    # 37. Test that last_name is required
    def test_last_name_required(self):
        self.address.last_name = ""
        with self.assertRaises(ValidationError):
            self.address.full_clean()

    # 38. Test that line1 is required
    def test_line1_required(self):
        self.address.line1 = ""
        with self.assertRaises(ValidationError):
            self.address.full_clean()

    # 40. Test that line1 is required for valid address
    def test_line1_required_for_address(self):
        self.address.line1 = ""
        with self.assertRaises(ValidationError):
            self.address.full_clean()

    def test_first_name_max_length_in_batch(self):
        # Create a batch of addresses
        addresses = AddressFactory.create_batch(10)
        for address in addresses:
            max_length = address._meta.get_field("first_name").max_length
            self.assertEqual(max_length, 255)

    def test_batch_create_with_overrides(self):
        # Create a batch with overridden city and state values
        addresses = AddressFactory.create_batch(3, city="Test City", state="Test State")
        for address in addresses:
            self.assertEqual(address.city, "Test City")
            self.assertEqual(address.state, "Test State")

    def test_batch_creation_for_field_combinations(self):
        addresses = AddressFactory.create_batch(10, country="US")
        for address in addresses:
            self.assertEqual(address.country.code.upper(), "US")
