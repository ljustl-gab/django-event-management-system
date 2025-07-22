from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Setup database for deployment'

    def handle(self, *args, **options):
        self.stdout.write("🗄️ Setting up database...")
        
        try:
            # Check if we're on Render
            is_render = 'RENDER_EXTERNAL_HOSTNAME' in os.environ
            self.stdout.write(f"Platform: {'Render' if is_render else 'Other'}")
            
            # Run makemigrations
            self.stdout.write("📝 Running makemigrations...")
            call_command('makemigrations', verbosity=1)
            
            # Run migrate
            self.stdout.write("📊 Running migrations...")
            call_command('migrate', verbosity=2)
            
            # Verify tables exist
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [row[0] for row in cursor.fetchall()]
                
            self.stdout.write(f"✅ Database setup complete. Tables: {len(tables)}")
            for table in tables:
                self.stdout.write(f"   - {table}")
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Database setup failed: {e}")
            )
            raise 