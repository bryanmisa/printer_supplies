from django.core.management.base import BaseCommand
from inventory.models import User


class Command(BaseCommand):
    help = 'Creates an administrator user with role=admin'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@localhost.com'
        password = 'admin123'

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.delete()
            self.stdout.write(f'Deleted existing user: {username}')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.save()

        self.stdout.write(self.style.SUCCESS(
            f'\nAdministrator created successfully!\n'
            f'  Username: {username}\n'
            f'  Password: {password}\n'
            f'  Role: Administrator\n'
        ))