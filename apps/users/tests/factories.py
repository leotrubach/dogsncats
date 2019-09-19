import factory
import pytz

from apps.pets.tests.factories import OwnerFactory
from apps.users import models
from apps.users.enums import UserRole


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    role = UserRole.NONE
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(
        lambda o: "{}{}".format(o.first_name[0], o.last_name).lower()
    )
    email = factory.Faker("email")
    is_staff = True
    is_active = True
    date_joined = factory.Faker("past_datetime", tzinfo=pytz.utc)


class AdminUserFactory(UserFactory):
    is_superuser = True


class OwnerUserFactory(UserFactory):
    role = UserRole.OWNER
    owner = factory.SubFactory(
        OwnerFactory,
        full_name=factory.LazyAttribute(
            lambda o: "{} {}".format(
                o.factory_parent.first_name, o.factory_parent.last_name
            )
        ),
    )
