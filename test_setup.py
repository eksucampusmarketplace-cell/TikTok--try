#!/usr/bin/env python3
"""
Setup validation script for TikTok Automation Bot

This script checks that all dependencies are installed correctly
and the project structure is valid.
"""

import sys
import importlib.util

def check_python_version():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.7+")
        return False

def check_module(module_name):
    """Check if a module is installed."""
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name} - OK")
        return True
    except ImportError:
        print(f"✗ {module_name} - NOT INSTALLED")
        return False

def check_file(filepath):
    """Check if a file exists."""
    import os
    if os.path.exists(filepath):
        print(f"✓ {filepath} - OK")
        return True
    else:
        print(f"✗ {filepath} - MISSING")
        return False

def main():
    print("=" * 60)
    print("TikTok Automation Bot - Setup Validation")
    print("=" * 60)
    print()
    
    # Check Python version
    print("Python Environment:")
    print("-" * 60)
    python_ok = check_python_version()
    print()
    
    # Check required modules
    print("Required Modules:")
    print("-" * 60)
    modules = [
        "selenium",
        "seleniumbase",
    ]
    modules_ok = all(check_module(module) for module in modules)
    print()
    
    # Check project structure
    print("Project Structure:")
    print("-" * 60)
    files = [
        "main.py",
        "config.py",
        "requirements.txt",
        "social_media/tiktok.py",
        "README.md",
        ".gitignore",
    ]
    files_ok = all(check_file(f) for f in files)
    print()
    
    # Summary
    print("=" * 60)
    print("Summary:")
    print("-" * 60)
    if python_ok and modules_ok and files_ok:
        print("✓ All checks passed! You're ready to use the bot.")
        print()
        print("Next steps:")
        print("1. Edit config.py with your credentials")
        print("2. Run: python main.py")
        print("   Or for interactive mode: python main.py --interactive")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print()
        if not modules_ok:
            print("To install missing modules, run:")
            print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
