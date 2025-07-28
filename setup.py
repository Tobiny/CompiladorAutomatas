#!/usr/bin/env python3
"""
Setup script for Automata Compiler API

This script helps set up the development environment and dependencies.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a system command with error handling."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {description} failed: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} is not compatible (requires 3.9+)")
        return False


def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    directories = ['temp', 'uploads', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ Created {directory}/ directory")


def install_dependencies():
    """Install Python dependencies."""
    return run_command("pip install -r requirements.txt", "Installing dependencies")


def run_tests():
    """Run basic tests if available."""
    if Path("tests").exists():
        return run_command("python -m pytest tests/ -v", "Running tests")
    else:
        print("📝 No tests directory found, skipping tests")
        return True


def main():
    """Main setup function."""
    print("🚀 Setting up Automata Compiler API")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Incompatible Python version")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Setup completed with test failures")
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   • Run the API: python app.py")
    print("   • Compile a file: python compile.py examples/basic_program.af")
    print("   • View examples: ls examples/")
    print("   • Check API health: curl http://localhost:5000/api/health")
    print("\n🌐 For deployment to Render.com:")
    print("   • Push to GitHub")
    print("   • Connect repository to Render")
    print("   • Deploy as Web Service")


if __name__ == "__main__":
    main() 