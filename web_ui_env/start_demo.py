#!/usr/bin/env python3
"""
Simple demo script to start the Tag Management Web UI
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def main():
    """Start the Tag Management Web UI demo"""
    print("🏷️  Tag Management Web UI Demo")
    print("=" * 50)

    print("📊 System Status:")
    try:
        import tag_manager
        tm = tag_manager.TagManager()
        analytics = tm.get_tag_analytics()
        print(f"   📊 Total Tags: {analytics.get('total_tags', 0)}")
        print(f"   📄 Documents: {analytics.get('total_documents', 0)}")
        print(f"   📂 Categories: {len(analytics.get('category_distribution', []))}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    print("\n🚀 Starting Web UI...")

    # Kill any existing Streamlit processes on port 8501
    try:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/IM", "streamlit.exe"], capture_output=True)
        else:
            subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
    except:
        pass

    # Start Streamlit
    try:
        print("🌐 Opening web interface...")
        print("   📍 URL: http://0.0.0.0:8501")
        print("   ⏳ Starting server...")

        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open("http://0.0.0.0:8501")
                print("   ✅ Browser opened!")
            except:
                print("   📋 Please manually open: http://0.0.0.0:8501")

        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        # Start Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            "web_ui.py",
            "--server.port", "8501",
            "--server.address", "http://0.0.0.0",
            "--browser.gatherUsageStats", "false",
            "--server.runOnSave", "true"
        ]

        subprocess.run(cmd)

    except KeyboardInterrupt:
        print("\n👋 Web UI stopped by user")
    except Exception as e:
        print(f"❌ Error starting web UI: {e}")
        print("💡 Try running manually:")
        print("   uv run streamlit run web_ui.py --server.port 8501")

if __name__ == "__main__":
    main()