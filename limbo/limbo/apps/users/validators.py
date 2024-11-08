from django.core.exceptions import ValidationError
import re


class PasswordStrongValidator:
    def validate(self, password, user=None):
        # Define the password requirements
        requirements = [
            (r"[A-Z]", "Password must contain at least one uppercase letter (A-Z)."),
            (r"[a-z]", "Password must contain at least one lowercase letter (a-z)."),
            (r"\d", "Password must contain at least one digit (0-9)."),
            (
                r'[!@#$%^&*(),.?":{}|<>]',
                "Password must contain at least one special character, such as @, #, $, %, &, or *.",
            ),
        ]

        # Check password length
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Validate each requirement
        for pattern, error_message in requirements:
            if not re.search(pattern, password):
                raise ValidationError(error_message)

    def get_help_text(self):
        return (
            "Your password must contain at least 8 characters, "
            "include both uppercase and lowercase letters, "
            "contain at least one digit, and at least one special character "
            "such as @, #, $, %, &, or *."
        )
