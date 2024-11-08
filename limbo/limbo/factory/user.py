import factory
from django.utils import timezone

from limbo.apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = False
    is_active = True
    date_joined = factory.LazyFunction(timezone.now)
    extra_field = ""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        password = kwargs.pop("password", "defaultpassword")
        if cls._meta.django_get_or_create:
            return cls._get_or_create(model_class, *args, **kwargs)

        manager = cls._get_manager(model_class)
        return manager.create_user(password=password, *args, **kwargs)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        # Add groups if provided
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)

    @factory.post_generation
    def user_permissions(self, create, extracted, **kwargs):
        # Add permissions if provided
        if not create:
            return

        if extracted:
            for permission in extracted:
                self.user_permissions.add(permission)
