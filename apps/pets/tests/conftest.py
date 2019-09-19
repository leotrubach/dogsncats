import pytest

from apps.pets.tests.factories import OwnerFactory


@pytest.fixture
def owner():
    return OwnerFactory()

