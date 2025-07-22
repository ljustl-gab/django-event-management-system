#!/bin/bash

echo "🚀 Django Event Management System - Deployment Script"
echo "=================================================="

# Check if git is clean
if [[ -n $(git status --porcelain) ]]; then
    echo "❌ Please commit all changes before deploying"
    exit 1
fi

echo "✅ Git repository is clean"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo ""
echo "1. Go to https://railway.app"
echo "2. Sign up/Login with GitHub"
echo "3. Click 'New Project'"
echo "4. Select 'Deploy from GitHub repo'"
echo "5. Choose: ljustl-gab/django-event-management-system"
echo "6. Railway will automatically deploy your app"
echo ""
echo "🔧 After deployment, set these environment variables:"
echo "   DEBUG=False"
echo "   SECRET_KEY=your-secret-key-here"
echo "   ALLOWED_HOSTS=your-railway-domain.railway.app"
echo ""
echo "👤 Create admin user in Railway terminal:"
echo "   python manage.py createsuperuser --username admin --email admin@example.com"
echo ""
echo "📧 Send email to emanuel@freelaw.work with your live URL"
echo ""
echo "✅ Deployment files are ready!" 