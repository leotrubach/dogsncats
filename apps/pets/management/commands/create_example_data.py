import getpass
from typing import List

from django.core.management import BaseCommand

from apps.users.models import User
from apps.users.tests.factories import OwnerUserFactory, AdminUserFactory


class Command(BaseCommand):
    help = "Seed database"
    owner_count = 10

    def handle(self, *args, **options):
        password = getpass.getpass("Enter pet owners' password:")
        admin_password = getpass.getpass("Enter admin password:")
        owner_users: List[User] = OwnerUserFactory.create_batch(
            10, owner__pets__dogs=(1, 3), owner__pets__cats=(1, 3)
        )
        for u in owner_users:
            u.set_password(password)
            u.save()
        print(f"Created {self.owner_count} owners with pets", file=self.stderr)
        admin = AdminUserFactory(username="admin")
        admin.set_password(admin_password)
        admin.save()
        print("Create admin user", file=self.stderr)
