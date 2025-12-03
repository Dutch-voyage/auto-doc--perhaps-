#!/usr/bin/env python3
"""
Startup script for Tag Management Web UI
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")

        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "-r", "requirements_web.txt"
            ])
            print("✅ Packages installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            return False

    return True

def check_database():
    """Check if database exists and setup if needed"""
    db_path = Path("tags.db")

    if not db_path.exists():
        print("📊 Database not found. Running setup...")
        try:
            subprocess.check_call([sys.executable, "setup_tags.py"])
            print("✅ Database setup completed!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Database setup failed: {e}")
            return False

    return True

def start_web_ui():
    """Start the Streamlit web UI"""
    print("🚀 Starting Tag Management Web UI...")
    print("🌐 Opening in browser...")

    try:
        # Streamlit will automatically open the browser
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "web_ui.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Web UI stopped by user")
    except Exception as e:
        print(f"❌ Failed to start web UI: {e}")

def main():
    """Main startup function"""
    print("🏷️  Tag Management Web UI")
    print("=" * 40)

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    # Check database
    if not check_database():
        sys.exit(1)

    # Start web UI
    start_web_ui()

if __name__ == "__main__":
    main()