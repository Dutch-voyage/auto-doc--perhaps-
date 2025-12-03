#!/usr/bin/env python3
"""
Startup script for interactive terminal server
Launches WebSocket terminal server for interactive sessions
"""

import subprocess
import sys
import os
import signal
import time
import argparse

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Shutting down terminal server...")
    sys.exit(0)

def main():
    """Main startup function"""
    parser = argparse.ArgumentParser(description="Start Interactive Terminal Server")
    parser.add_argument("--port", type=int, default=8765, help="Port to run server on (default: 8765)")
    parser.add_argument("--host", type=str, default="localhost", help="Host to bind server to (default: localhost)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("🚀 Starting Interactive Terminal Server")
    print("=" * 50)
    print(f"📍 Host: {args.host}")
    print(f"🔌 Port: {args.port}")
    print(f"🖥️ Applications: Claude Code, Python REPL, Bash Shell, Node.js REPL")
    print(f"🔗 WebSocket URL: ws://{args.host}:{args.port}")
    print("=" * 50)

    # Check if required dependencies are available
    try:
        import websockets
        print("✅ websockets module found")
    except ImportError:
        print("❌ websockets module not found. Please install with:")
        print("   uv sync --extra interactive-terminal")
        sys.exit(1)

    # Start the terminal server
    try:
        import asyncio
        from terminal_server import TerminalServer

        async def run_server():
            server = TerminalServer()

            # Start the server
            server_task = await server.start_server()

            print("✅ Terminal server started successfully!")
            print("🌐 Ready for WebSocket connections...")
            print("💡 Start the web UI and go to the Terminal tab to connect")
            print("💻 Press Ctrl+C to stop the server")
            print()

            # Keep server running
            try:
                await server_task.wait_closed()
            except KeyboardInterrupt:
                pass

        # Run the async main function
        asyncio.run(run_server())

    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()