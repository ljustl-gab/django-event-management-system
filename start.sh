#!/bin/bash

set -e  # Exit on any error

echo "🚀 Starting Django Event Management System on Railway..."
echo "📊 Environment:"
echo "   PORT: $PORT"
echo "   DEBUG: $DEBUG"
echo "   ALLOWED_HOSTS: $ALLOWED_HOSTS"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p staticfiles

# Check if we can run Python
echo "🐍 Testing Python..."
python --version

# Check if Django is installed
echo "🔧 Testing Django..."
python -c "import django; print(f'Django version: {django.get_version()}')"

# Run migrations
echo "📊 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Test the application
echo "🧪 Testing Django application..."
python manage.py check

# Create superuser if it doesn't exist
echo "👤 Checking for admin user..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    admin_user = User.objects.get(email='admin@example.com')
    print(f'Admin user already exists: {admin_user.email}')
except User.DoesNotExist:
    try:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print(f'Admin user created successfully: {admin_user.email}')
    except Exception as e:
        print(f'Error creating admin user: {e}')
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
            print(f'Admin user created with alternative method: {admin_user.email}')
        except Exception as e2:
            print(f'Alternative method also failed: {e2}')
"

# Start the application
echo "🌐 Starting Gunicorn server on port $PORT..."
echo "   Command: gunicorn event_management.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --access-logfile - --error-logfile - --log-level info"

gunicorn event_management.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info 