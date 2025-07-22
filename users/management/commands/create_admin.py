from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create admin user for the application'

    def handle(self, *args, **options):
        try:
            # Check if admin user already exists
            if User.objects.filter(email='admin@example.com').exists():
                self.stdout.write(
                    self.style.SUCCESS('Admin user already exists: admin@example.com')
                )
                return

            # Create admin user
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user: {admin_user.email}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {e}')
            )
            # Try alternative method
            try:
                admin_user = User.objects.create_user(
                    username='admin',
                    email='admin@example.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='User',
                    is_staff=True,
                    is_superuser=True
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created admin user with alternative method: {admin_user.email}')
                )
            except Exception as e2:
                self.stdout.write(
                    self.style.ERROR(f'Alternative method also failed: {e2}')
                ) 