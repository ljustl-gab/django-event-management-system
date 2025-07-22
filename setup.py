#!/usr/bin/env python
"""
Setup script for Event Management System
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 11):
        print("✗ Python 3.11 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_env_file():
    """Create .env file from template."""
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            import shutil
            shutil.copy('env.example', '.env')
            print("✓ Created .env file from template")
            print("⚠️  Please edit .env file with your configuration")
        else:
            print("⚠️  env.example not found, please create .env file manually")
    else:
        print("✓ .env file already exists")

def main():
    """Main setup function."""
    print("🚀 Setting up Event Management System")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        if not run_command("python -m venv venv", "Create virtual environment"):
            sys.exit(1)
    
    # Determine activation command
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Install Python dependencies"):
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    print("✓ Created logs directory")
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your configuration")
    print("2. Create PostgreSQL database: createdb event_management")
    print("3. Run migrations: python manage.py migrate")
    print("4. Create superuser: python manage.py createsuperuser")
    print("5. Start the server: python manage.py runserver")
    print("\nFor Docker deployment:")
    print("docker-compose up --build")
    
    print("\n📚 Documentation available at:")
    print("- API Documentation: http://localhost:8000/swagger/")
    print("- README.md for detailed instructions")

if __name__ == "__main__":
    main() 