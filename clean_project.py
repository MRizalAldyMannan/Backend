#!/usr/bin/env python3
"""
Project Cleanup Script
Removes all runtime artifacts, database files, and cache directories
to prepare the project for sharing as a clean zip file.
"""

import os
import shutil
import sys
from pathlib import Path

def remove_path(path):
    """Remove a file or directory safely"""
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"✓ Removed file: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"✓ Removed directory: {path}")
    except Exception as e:
        print(f"✗ Error removing {path}: {e}")

def clean_project():
    """Clean the project by removing runtime artifacts"""
    print("🧹 Cleaning Task Management Backend Project...")
    print("=" * 50)
    
    # Files and directories to remove
    items_to_remove = [
        # Database files
        "instance/app.db",
        "instance/",
        
        # Python cache
        "__pycache__/",
        "app/__pycache__/",
        "app/api/__pycache__/",
        "app/errors/__pycache__/",
        "migrations/__pycache__/",
        "tests/__pycache__/",
        
        # Database migrations
        "migrations/",
        
        # Environment files
        ".env",
        
        # IDE files
        ".vscode/",
        ".idea/",
        
        # OS files
        ".DS_Store",
        "Thumbs.db",
        
        # Log files
        "*.log",
        
        # Coverage files
        ".coverage",
        "htmlcov/",
        ".pytest_cache/",
        
        # Virtual environment (if exists)
        "venv/",
        "env/",
        ".venv/",
    ]
    
    # Remove items
    for item in items_to_remove:
        if os.path.exists(item):
            remove_path(item)
        else:
            print(f"- Skipped (not found): {item}")
    
    # Remove any remaining __pycache__ directories recursively
    for root, dirs, files in os.walk(".", topdown=False):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                remove_path(cache_path)
    
    print("\n" + "=" * 50)
    print("✅ Project cleaned successfully!")
    print("\n📋 Next steps for your friend:")
    print("1. Extract the zip file")
    print("2. Create virtual environment: python -m venv venv")
    print("3. Activate virtual environment:")
    print("   - Windows: venv\\Scripts\\activate")
    print("   - macOS/Linux: source venv/bin/activate")
    print("4. Install dependencies: pip install -r requirements.txt")
    print("5. Set up environment variables (create .env file)")
    print("6. Initialize database: flask db init && flask db migrate && flask db upgrade")
    print("7. Run the application: python run.py")
    print("\n📖 See README.md for detailed setup instructions!")

if __name__ == "__main__":
    # Confirm before cleaning
    print("⚠️  This will remove all runtime artifacts and database files!")
    print("   This action cannot be undone.")
    
    response = input("\nDo you want to continue? (y/N): ").strip().lower()
    if response in ['y', 'yes']:
        clean_project()
    else:
        print("❌ Cleanup cancelled.")
        sys.exit(0) 