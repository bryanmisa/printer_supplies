from django.contrib.auth.management.commands.createsuperuser import Command as BaseCreateSuperUser


class Command(BaseCreateSuperUser):
    def handle(self, *args, **options):
        # Call parent to create the user
        super().handle(*args, **options)
        # Ensure the created user has role='admin'
        from inventory.models import User
        username = options.get('username') or 'admin'
        try:
            user = User.objects.get(username=username)
            user.role = 'admin'
            user.is_staff = True
            user.save(update_fields=['role', 'is_staff'])
            self.stdout.write(self.style.SUCCESS(f'  Set role=admin for {username}'))
        except User.DoesNotExist:
            pass
