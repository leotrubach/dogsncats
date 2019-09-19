from rest_framework.test import APIClient
import pytest
from apps.users.tests.factories import AdminUserFactory, OwnerUserFactory


@pytest.fixture
def admin():
    return AdminUserFactory()


@pytest.fixture
def owneruser():
    return OwnerUserFactory(owner__pets__cats=(1, 2), owner__pets__dogs=(1, 2))


@pytest.fixture
def adminclient(db, admin):
    client = APIClient()
    client.force_authenticate(admin)
    return client


@pytest.fixture
def ownerclient(db, owneruser):
    client = APIClient()
    client.force_authenticate(owneruser)
    return client
