from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create default admin user if none exists'

    def handle(self, *args, **options):
        username = 'admin'
        password = 'nomad123'

        if User.objects.filter(username=username).exists():
            # Update password for existing user
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Updated password for {username}'))
        else:
            User.objects.create_superuser(
                username=username,
                email='admin@nomadsocks.mn',
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {username}'))
