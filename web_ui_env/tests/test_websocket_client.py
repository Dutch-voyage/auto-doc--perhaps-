#!/usr/bin/env python3
"""
Simple WebSocket client to test terminal server connection
"""
import asyncio
import websockets
import json

async def test_connection():
    uri = "ws://localhost:8765"
    try:
        print(f"Connecting to {uri}...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket server")

            # Send new session request
            message = {
                "type": "new_session",
                "command": "echo 'Hello World'"
            }
            await websocket.send(json.dumps(message))
            print(f"📤 Sent: {message}")

            # Wait for response
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print(f"📥 Received: {response}")

    except websockets.exceptions.InvalidMessage as e:
        print(f"❌ Invalid Message: {e}")
    except websockets.exceptions.InvalidUpgrade as e:
        print(f"❌ Invalid Upgrade: {e}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"❌ Connection Closed: {e}")
    except asyncio.TimeoutError:
        print(f"⏰ Timeout waiting for response")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())