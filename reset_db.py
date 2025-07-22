#!/usr/bin/env python
"""
Emergency database reset script for Render deployment.
Run this if the database is corrupted or migrations fail.
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def reset_database():
    """Reset the database completely."""
    print("🗄️ Resetting database...")
    
    try:
        # Drop all tables
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                if table != 'sqlite_sequence':
                    cursor.execute(f"DROP TABLE IF EXISTS {table};")
                    print(f"   Dropped table: {table}")
        
        # Run migrations
        print("📊 Running migrations...")
        call_command('migrate', verbosity=2)
        
        # Create superuser
        print("👤 Creating superuser...")
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("   Created admin user: admin@example.com / admin123")
        else:
            print("   Admin user already exists")
        
        print("✅ Database reset completed successfully!")
        
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        return False
    
    return True

if __name__ == '__main__':
    reset_database() 