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