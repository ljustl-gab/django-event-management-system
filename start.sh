#!/bin/bash

set -e  # Exit on any error

echo "🚀 Starting Django Event Management System on Railway..."
echo "📊 Environment:"
echo "   PORT: $PORT"
echo "   DEBUG: $DEBUG"
echo "   ALLOWED_HOSTS: $ALLOWED_HOSTS"
echo "   RENDER_EXTERNAL_HOSTNAME: $RENDER_EXTERNAL_HOSTNAME"

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

# Force database initialization
echo "🗄️ Initializing database..."
python manage.py makemigrations --noinput || echo "No new migrations needed"
python manage.py migrate --noinput --verbosity=2

# Verify database tables exist
echo "🔍 Verifying database tables..."
python manage.py dbshell --command=".tables" || echo "Database verification failed"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Test the application
echo "🧪 Testing Django application..."
python manage.py check --deploy

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