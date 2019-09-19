import factory
import random
from apps.pets import models


def count_to_num(count):
    """
    Generate random integer if count is passed as (a, b) otherwise just return count
    itself
    """
    if isinstance(count, (tuple, list)):
        if len(count) != 2:
            raise ValueError
        return random.randint(*count)
    else:
        return count


class OwnerFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Owner

    full_name = factory.Faker("name")

    @factory.post_generation
    def pets(self, create, extracted, cats=0, dogs=0, **kwargs):
        if not create:
            return
        if cats:
            CatFactory.create_batch(count_to_num(cats), owner=self)
        if dogs:
            DogFactory.create_batch(count_to_num(dogs), owner=self)


class CatFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Cat

    name = factory.Faker("first_name")
    birthday = factory.Faker("date_of_birth", minimum_age=0, maximum_age=22)
    owner = factory.SubFactory(OwnerFactory)


class DogFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Dog

    name = factory.Faker("first_name")
    birthday = factory.Faker("date_of_birth", minimum_age=0, maximum_age=20)
    owner = factory.SubFactory(OwnerFactory)
