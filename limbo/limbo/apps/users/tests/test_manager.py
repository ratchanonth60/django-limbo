import unittest

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from marketEdge.factory import TestsCase
from django.db.utils import DataError, IntegrityError

# Assuming your custom User model is set as the AUTH_USER_MODEL
User = get_user_model()


class UserAdminManagerTestCase(TestsCase):
    def setUp(self):
        self.user_manager = User.objects

    # Test cases for create_user
    def test_create_user_valid_data(self):
        """Test creating a user with valid data."""
        user = self.user_manager.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))

    def test_create_user_no_email(self):
        """Test creating a user without an email raises ValueError."""
        with self.assertRaises(ValueError):
            self.user_manager.create_user(
                username="testuser", email="", password="testpass123"
            )

    def test_create_user_invalid_email(self):
        """Test creating a user with an invalid email."""
        with self.assertRaises(ValidationError):
            user = self.user_manager.create_user(
                username="testuser", email="invalid-email", password="testpass123"
            )
            user.full_clean()

    def test_create_user_email_normalized(self):
        """Test that the email for a new user is normalized."""
        email = "test@EXAMPLE.COM"
        user = self.user_manager.create_user(
            username="testuser", email=email, password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")

    def test_create_user_no_username(self):
        """Test creating a user without a username."""
        with self.assertRaises(TypeError):
            self.user_manager.create_user(
                email="test@example.com", password="testpass123"
            )

    def test_create_user_duplicate_username(self):
        """Test creating a user with a duplicate username."""
        self.user_manager.create_user(
            username="testuser", email="test1@example.com", password="testpass123"
        )
        with self.assertRaises(IntegrityError):
            user = self.user_manager.create_user(
                username="testuser", email="test2@example.com", password="testpass123"
            )
            user.full_clean()

    def test_create_user_password_encrypted(self):
        """Test that the user's password is encrypted."""
        user = self.user_manager.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertNotEqual(user.password, "testpass123")
        self.assertTrue(user.check_password("testpass123"))

    def test_create_user_is_active_default(self):
        """Test that is_active is True by default."""
        user = self.user_manager.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertTrue(user.is_active)

    def test_create_user_is_active_false(self):
        """Test creating a user with is_active=False."""
        user = self.user_manager.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            is_active=False,
        )
        self.assertFalse(user.is_active)

    def test_create_user_is_staff_default(self):
        """Test that is_staff is False by default."""
        user = self.user_manager.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertFalse(user.is_staff)

    def test_create_user_is_superuser_default(self):
        """Test that is_superuser is False by default."""
        user = self.user_manager.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertFalse(user.is_superuser)

    def test_create_user_extra_fields(self):
        """Test creating a user with extra fields."""
        user = self.user_manager.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

    def test_create_user_long_username(self):
        """Test creating a user with a very long username."""
        username = "u" * 150  # Assuming max_length is sufficient
        with self.assertRaises(DataError):
            self.user_manager.create_user(
                username=username, email="test@example.com", password="testpass123"
            )

    def test_create_user_special_characters_in_username(self):
        """Test creating a user with special characters in username."""
        username = "test.user+1"
        user = self.user_manager.create_user(
            username=username, email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.username, username)

    def test_create_user_non_ascii_username(self):
        """Test creating a user with non-ASCII characters in username."""
        username = "测试用户"  # 'Test User' in Chinese
        user = self.user_manager.create_user(
            username=username, email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.username, username)

    def test_create_user_no_password(self):
        """Test creating a user without a password."""
        with self.assertRaises(TypeError):
            self.user_manager.create_user(username="testuser", email="test@example.com")

    def test_create_user_non_string_email(self):
        """Test creating a user with non-string email."""
        with self.assertRaises(AttributeError):
            self.user_manager.create_user(
                username="testuser", email=12345, password="testpass123"
            )

    def test_create_user_using_different_db(self):
        """Test creating a user using a specified database."""
        user = self.user_manager.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertEqual(user._state.db, "default")

    # Test cases for create_superuser
    def test_create_superuser_valid_data(self):
        """Test creating a superuser with valid data."""
        user = self.user_manager.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser_is_superuser_true(self):
        """Test that is_superuser is set to True for superuser."""
        user = self.user_manager.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass123"
        )
        self.assertTrue(user.is_superuser)

    def test_create_superuser_is_staff_true(self):
        """Test that is_staff is set to True for superuser."""
        user = self.user_manager.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass123"
        )
        self.assertTrue(user.is_staff)

    def test_create_superuser_is_active_true(self):
        """Test that is_active is True for superuser."""
        user = self.user_manager.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass123"
        )
        self.assertTrue(user.is_active)

    def test_create_superuser_no_email(self):
        """Test creating a superuser without an email raises ValueError."""
        with self.assertRaises(ValueError):
            self.user_manager.create_superuser(
                username="adminuser", email="", password="adminpass123"
            )

    def test_create_superuser_email_normalized(self):
        """Test that the email for a new superuser is normalized."""
        email = "admin@EXAMPLE.COM"
        user = self.user_manager.create_superuser(
            username="adminuser", email=email, password="adminpass123"
        )
        self.assertEqual(user.email, "admin@example.com")

    def test_create_superuser_no_username(self):
        """Test creating a superuser without a username."""
        with self.assertRaises(TypeError):
            self.user_manager.create_superuser(
                email="admin@example.com", password="adminpass123"
            )

    def test_create_superuser_no_password(self):
        """Test creating a superuser without a password."""
        with self.assertRaises(TypeError):
            self.user_manager.create_superuser(
                username="adminuser", email="admin@example.com"
            )

    def test_create_superuser_password_encrypted(self):
        """Test that the superuser's password is encrypted."""
        user = self.user_manager.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass123"
        )
        self.assertNotEqual(user.password, "adminpass123")
        self.assertTrue(user.check_password("adminpass123"))

    def test_create_superuser_extra_fields(self):
        """Test creating a superuser with extra fields."""
        user = self.user_manager.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User",
        )
        self.assertEqual(user.first_name, "Admin")
        self.assertEqual(user.last_name, "User")

    def test_create_superuser_non_string_email(self):
        """Test creating a superuser with non-string email."""
        with self.assertRaises(AttributeError):
            self.user_manager.create_superuser(
                username="adminuser", email=12345, password="adminpass123"
            )

    def test_create_superuser_long_username(self):
        """Test creating a superuser with a very long username."""
        username = "admin" * 50  # Assuming max_length is sufficient
        with self.assertRaises(DataError):
            self.user_manager.create_superuser(
                username=username, email="admin@example.com", password="adminpass123"
            )

    def test_create_superuser_special_characters_in_username(self):
        """Test creating a superuser with special characters in username."""
        username = "admin.user+1"
        user = self.user_manager.create_superuser(
            username=username, email="admin@example.com", password="adminpass123"
        )
        self.assertEqual(user.username, username)

    def test_create_superuser_non_ascii_username(self):
        """Test creating a superuser with non-ASCII characters in username."""
        username = "管理员"  # 'Administrator' in Chinese
        user = self.user_manager.create_superuser(
            username=username, email="admin@example.com", password="adminpass123"
        )
        self.assertEqual(user.username, username)

    def test_create_superuser_using_different_db(self):
        """Test creating a superuser using a specified database."""
        user = self.user_manager.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass123"
        )
        self.assertEqual(user._state.db, "default")

    def test_create_superuser_is_admin_true(self):
        """Test that is_admin is set to True for superuser."""
        user = self.user_manager.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass123"
        )
        self.assertTrue(user.is_admin)

    def test_create_superuser_permissions(self):
        """Test that superuser has all permissions."""
        user = self.user_manager.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass123"
        )
        self.assertTrue(user.has_perm("auth.add_user"))

    def test_create_superuser_calls_create_user(self):
        """Test that create_superuser calls create_user."""
        with unittest.mock.patch.object(
            self.user_manager, "create_user", wraps=self.user_manager.create_user
        ) as mocked_create_user:
            self.user_manager.create_superuser(
                username="adminuser", email="admin@example.com", password="adminpass123"
            )
            mocked_create_user.assert_called_once()

    def test_create_superuser_invalid_email(self):
        """Test creating a superuser with an invalid email."""
        with self.assertRaises(ValidationError):
            user = self.user_manager.create_superuser(
                username="adminuser", email="invalid-email", password="adminpass123"
            )
            user.full_clean()

    def test_create_superuser_is_superuser_false(self):
        """Test that creating superuser with is_superuser=False raises error."""
        user = self.user_manager.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass123"
        )
        user.is_superuser = False
        with self.assertRaises(ValueError):
            if not user.is_superuser:
                raise ValueError("Superuser must have is_superuser=True.")

    def test_create_superuser_is_staff_false(self):
        """Test that creating superuser with is_staff=False raises error."""
        user = self.user_manager.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpass123"
        )
        user.is_staff = False
        with self.assertRaises(ValueError):
            if not user.is_staff:
                raise ValueError("Superuser must have is_staff=True.")
