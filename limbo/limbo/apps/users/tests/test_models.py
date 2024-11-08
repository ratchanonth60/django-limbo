from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError

from marketEdge.apps.users.manager import UserAdminManager
from marketEdge.factory import TestsCase

# Assuming your custom User model is already set as the AUTH_USER_MODEL
User = get_user_model()


class UserModelTestCase(TestsCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_create_user_with_valid_data(self):
        """Test creating a user with valid data."""
        user = User.objects.create_user(**self.user_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.user_data["username"])
        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertEqual(user.email, self.user_data["email"])

    def test_username_max_length(self):
        """Test that username cannot exceed max_length."""
        self.user_data["username"] = "a" * 31  # Max_length is 30
        with self.assertRaises(ValidationError):
            user = User(**self.user_data)
            user.full_clean()

    def test_username_unique(self):
        """Test that username must be unique."""
        User.objects.create_user(**self.user_data)
        with self.assertRaises(ValidationError):
            user = User(**self.user_data)
            user.full_clean()

    # def test_username_validators(self):
    #     """Test username validators for allowed characters."""
    #     invalid_usernames = ["test user", "test@user!", "test/user", "test+user"]
    #     for username in invalid_usernames:
    #         with self.subTest(username=username):
    #             self.user_data["username"] = username
    #             with self.assertRaises(ValidationError):
    #                 user = User(**self.user_data)
    #                 user.full_clean()

    def test_email_field_missing(self):
        """Test that email field is optional."""
        self.user_data.pop("email")
        with self.assertRaises(TypeError):
            User.objects.create_user(**self.user_data)

    def test_first_name_max_length(self):
        """Test that first_name cannot exceed max_length."""
        self.user_data["first_name"] = "a" * 151  # Max_length is 150
        with self.assertRaises(ValidationError):
            user = User(**self.user_data)
            user.full_clean()

    def test_last_name_max_length(self):
        """Test that last_name cannot exceed max_length."""
        self.user_data["last_name"] = "a" * 151  # Max_length is 150
        with self.assertRaises(ValidationError):
            user = User(**self.user_data)
            user.full_clean()

    def test_is_staff_default(self):
        """Test that is_staff defaults to False."""
        user = User.objects.create_user(**self.user_data)
        self.assertFalse(user.is_staff)

    def test_is_active_default(self):
        """Test that is_active defaults to True."""
        user = User.objects.create_user(**self.user_data)
        self.assertTrue(user.is_active)

    def test_date_joined_auto_now(self):
        """Test that date_joined is set automatically."""
        user = User.objects.create_user(**self.user_data)
        self.assertIsNotNone(user.date_joined)

    def test_extra_field_blank(self):
        """Test that extra_field can be blank."""
        self.user_data["extra_field"] = ""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.extra_field, "")

    def test_extra_field_max_length(self):
        """Test that extra_field cannot exceed max_length."""
        self.user_data["extra_field"] = "a" * 6  # Max_length is 5
        with self.assertRaises(ValidationError):
            user = User(**self.user_data)
            user.full_clean()

    def test_get_full_name(self):
        """Test the get_full_name method."""
        user = User.objects.create_user(**self.user_data)
        expected_full_name = (
            f"{self.user_data['first_name']} {self.user_data['last_name']}"
        )
        self.assertEqual(user.get_full_name(), expected_full_name)

    def test_get_short_name(self):
        """Test the get_short_name method."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_short_name(), self.user_data["first_name"])

    def test_get_username(self):
        """Test the get_username method."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_username(), self.user_data["username"])

    @patch("marketEdge.apps.users.models.send_mail")
    def test_email_user(self, mock_send_mail):
        """Test the email_user method."""
        user = User.objects.create_user(**self.user_data)
        user.email_user("Test Subject", "Test Message")
        mock_send_mail.assert_called_once_with(
            "Test Subject",
            "Test Message",
            None,
            [user.email],
        )

    def test_clean_normalizes_email(self):
        """Test that clean method normalizes email."""
        self.user_data["email"] = "TEST@EXAMPLE.COM"
        user = User(**self.user_data)
        user.clean()
        self.assertEqual(user.email, "TEST@example.com")

    def test_groups_related_name(self):
        """Test the groups related_name."""
        user = User.objects.create_user(**self.user_data)
        group = Group.objects.create(name="Test Group")
        user.groups.add(group)
        self.assertIn(user, group.custom_user_set.all())

    def test_user_permissions_related_name(self):
        """Test the user_permissions related_name."""
        user = User.objects.create_user(**self.user_data)
        permission = Permission.objects.first()
        user.user_permissions.add(permission)
        self.assertIn(user, permission.custom_user_set.all())

    def test_required_fields(self):
        """Test that REQUIRED_FIELDS is set correctly."""
        self.assertIn("email", User.REQUIRED_FIELDS)
        self.assertEqual(len(User.REQUIRED_FIELDS), 1)

    def test_custom_manager(self):
        """Test that the custom manager is being used."""
        self.assertIsInstance(User.objects, UserAdminManager)

    def test_user_str(self):
        """Test the __str__ method of the user."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data["username"])

    def test_user_absolute_url(self):
        """Test get_absolute_url if implemented."""
        user = User.objects.create_user(**self.user_data)
        if hasattr(user, "get_absolute_url"):
            url = user.get_absolute_url()
            self.assertIsInstance(url, str)
        else:
            self.skipTest("get_absolute_url not implemented")
