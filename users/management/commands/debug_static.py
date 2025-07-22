from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.staticfiles.finders import find
import os

class Command(BaseCommand):
    help = 'Debug static files configuration'

    def handle(self, *args, **options):
        self.stdout.write("=== Static Files Debug ===")
        self.stdout.write(f"STATIC_URL: {settings.STATIC_URL}")
        self.stdout.write(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        self.stdout.write(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        self.stdout.write(f"STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
        
        # Check if static root exists
        if os.path.exists(settings.STATIC_ROOT):
            self.stdout.write(f"STATIC_ROOT exists: {settings.STATIC_ROOT}")
            files = os.listdir(settings.STATIC_ROOT)
            self.stdout.write(f"Files in STATIC_ROOT: {files[:10]}")  # Show first 10 files
        else:
            self.stdout.write(f"STATIC_ROOT does not exist: {settings.STATIC_ROOT}")
        
        # Try to find admin CSS
        admin_css = find('admin/css/base.css')
        self.stdout.write(f"Admin CSS found at: {admin_css}")
        
        # Check if staticfiles directory exists
        staticfiles_dir = settings.BASE_DIR / 'staticfiles'
        if staticfiles_dir.exists():
            self.stdout.write(f"staticfiles directory exists: {staticfiles_dir}")
            admin_dir = staticfiles_dir / 'admin'
            if admin_dir.exists():
                self.stdout.write(f"admin directory exists: {admin_dir}")
                css_dir = admin_dir / 'css'
                if css_dir.exists():
                    self.stdout.write(f"css directory exists: {css_dir}")
                    base_css = css_dir / 'base.css'
                    if base_css.exists():
                        self.stdout.write(f"base.css exists: {base_css}")
                    else:
                        self.stdout.write(f"base.css does not exist: {base_css}")
                else:
                    self.stdout.write(f"css directory does not exist: {css_dir}")
            else:
                self.stdout.write(f"admin directory does not exist: {admin_dir}")
        else:
            self.stdout.write(f"staticfiles directory does not exist: {staticfiles_dir}") 