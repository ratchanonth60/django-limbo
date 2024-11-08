import factory
from django_countries import countries
from faker import Faker
from limbo.apps.address.models import Address
from limbo.factory.base import BaseFactory
from phonenumber_field.phonenumber import PhoneNumber

fake = Faker()


class AddressFactory(BaseFactory):
    class Meta:
        model = Address

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    line1 = factory.Faker("street_address")
    line2 = factory.Faker("secondary_address")
    country = factory.Iterator([code for code, _ in list(countries)])
    postal_code = factory.Faker("postcode")
    phone_number = factory.LazyFunction(
        lambda: PhoneNumber.from_string(fake.phone_number(), region="US")
    )
    city = factory.Faker("city")
    state = factory.Faker("state")
