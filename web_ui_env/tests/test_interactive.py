#!/usr/bin/env python3
"""
Interactive WebSocket test with input/output
"""

import asyncio
import websockets
import json

async def test_interactive_session():
    """Test WebSocket with interactive input/output"""
    uri = "ws://localhost:8765"

    try:
        print(f"🔌 Connecting to {uri}...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket server")

            # Create a new session with a simple command
            message = {
                "type": "new_session",
                "command": "cat"
            }

            print(f"📤 Sending session request: {message}")
            await websocket.send(json.dumps(message))

            # Wait for session creation response
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print(f"📥 Received: {response}")

            # Parse the response to check session creation
            response_data = json.loads(response)
            if response_data.get('type') == 'session_created':
                print("✅ Session created successfully!")

                # Send some input to cat
                input_message = {
                    "type": "input",
                    "data": "Hello Interactive Terminal!\n"
                }

                print(f"📤 Sending input: {input_message}")
                await websocket.send(json.dumps(input_message))

                # Wait for continuous output until session ends
                print("📥 Waiting for terminal output (continuous)...")
                output_count = 0
                try:
                    while True:
                        output_response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                        data = json.loads(output_response)

                        if data.get('type') == 'output':
                            output_count += 1
                            print(f"📥 Received output #{output_count}: {repr(data.get('data', ''))}")
                        elif data.get('type') == 'input':
                            print(f"📤 Input echoed: {repr(data.get('data', ''))}")

                        # If we've received some output and the process ends, break
                        if output_count > 0:
                            break

                except asyncio.TimeoutError:
                    if output_count == 0:
                        print("⚠️ No output received within timeout")
                    else:
                        print("✅ Output stream ended")

                # Send EOF to cat (Ctrl+D) to close the session
                eof_message = {
                    "type": "input",
                    "data": "\x04"  # Ctrl+D character
                }

                print(f"📤 Sending EOF to close cat")
                await websocket.send(json.dumps(eof_message))

            return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_interactive_session())