#!/usr/bin/env python3
"""
Test Claude Code with interactive input
"""
import subprocess
import asyncio
import os
import time

async def test_claude_interactive():
    """Test Claude Code with some input"""

    cmd = [
        'script',
        '-q',
        '/dev/null',
        '-c',
        '/home/yyx/.nvm/versions/node/v22.18.0/bin/claude'
    ]

    env = os.environ.copy()
    env.update({
        'COLUMNS': '80',
        'LINES': '24',
        'TERM': 'xterm-256color'
    })

    print(f"Starting Claude Code...")

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=False,
        bufsize=0,
        env=env,
        preexec_fn=os.setsid
    )

    print(f"Claude Code started with PID: {process.pid}")

    # Wait a bit for startup
    await asyncio.sleep(2)

    # Try to read some initial output
    try:
        data = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None, process.stdout.read, 4096
            ),
            timeout=3.0
        )

        if data:
            text = data.decode('utf-8', errors='replace')
            print(f"Initial output: {repr(text[:200])}")
        else:
            print("No initial output")

    except asyncio.TimeoutError:
        print("Timeout waiting for initial output")

    # Try sending some input
    if process.poll() is None:
        print("Sending 'help' command...")
        try:
            input_data = b'help\n'
            process.stdin.write(input_data)
            process.stdin.flush()
            print("Input sent successfully")
        except Exception as e:
            print(f"Error sending input: {e}")

        # Wait for response
        await asyncio.sleep(3)

        try:
            data = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    None, process.stdout.read, 4096
                ),
                timeout=3.0
            )

            if data:
                text = data.decode('utf-8', errors='replace')
                print(f"Response output: {repr(text[:200])}")
            else:
                print("No response output")

        except asyncio.TimeoutError:
            print("Timeout waiting for response")

    # Clean up
    if process.poll() is None:
        print("Terminating process...")
        process.terminate()
        await asyncio.sleep(1)
        if process.poll() is None:
            process.kill()

    print("Test completed")

if __name__ == "__main__":
    asyncio.run(test_claude_interactive())