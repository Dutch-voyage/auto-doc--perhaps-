#!/usr/bin/env python3
"""
Simple WebSocket test to verify connection to terminal server
"""

import asyncio
import websockets
import json

async def test_connection():
    """Test WebSocket connection to terminal server"""
    uri = "ws://localhost:8765"

    try:
        print(f"🔌 Connecting to {uri}...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket server")

            # Test creating a new session
            message = {
                "type": "new_session",
                "command": "echo 'Hello WebSocket Test'"
            }

            print(f"📤 Sending: {message}")
            await websocket.send(json.dumps(message))

            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print(f"📥 Received: {response}")

            return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())