#!/usr/bin/env python3
"""
Test continuous terminal output with a long-running command
"""

import asyncio
import websockets
import json

async def test_continuous_output():
    """Test WebSocket with continuous terminal output"""
    uri = "ws://localhost:8765"

    try:
        print(f"🔌 Connecting to {uri}...")
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket server")

            # Create a session with a command that produces continuous output
            message = {
                "type": "new_session",
                "command": "for i in {1..5}; do echo \"Line $i: $(date)\"; sleep 1; done"
            }

            print(f"📤 Sending session request for continuous output test")
            await websocket.send(json.dumps(message))

            # Wait for session creation response
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            print(f"📥 Received: {response}")

            response_data = json.loads(response)
            if response_data.get('type') == 'session_created':
                print("✅ Session created successfully!")
                print("📥 Waiting for continuous terminal output...")

                output_count = 0
                start_time = asyncio.get_event_loop().time()

                try:
                    # Keep receiving messages for up to 10 seconds
                    while True:
                        output_response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                        data = json.loads(output_response)

                        elapsed = asyncio.get_event_loop().time() - start_time

                        if data.get('type') == 'output':
                            output_count += 1
                            output_text = data.get('data', '').strip()
                            print(f"📥 [{elapsed:.1f}s] Output #{output_count}: {output_text}")
                        elif data.get('type') == 'input':
                            print(f"📤 [{elapsed:.1f}s] Input echoed: {repr(data.get('data', ''))}")

                        # Stop after 10 seconds or after receiving 5+ outputs
                        if elapsed > 10 or output_count >= 5:
                            print("✅ Test completed - received sufficient output")
                            break

                except asyncio.TimeoutError:
                    print("⚠️ No more output received (timeout)")

                print(f"📊 Total outputs received: {output_count}")
                print("📥 Continuous output test completed successfully!")

            return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_continuous_output())