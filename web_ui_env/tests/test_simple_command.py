#!/usr/bin/env python3
"""
Test simple command execution with current PTY setup
"""
import subprocess
import asyncio
import os
import time

async def test_simple_command():
    """Test a simple command to see if output reading works"""

    cmd = [
        'script',
        '-q',
        '/dev/null',
        '-c',
        'echo "Hello World"; sleep 1; echo "Done"'
    ]

    env = os.environ.copy()
    env.update({
        'COLUMNS': '80',
        'LINES': '24',
        'TERM': 'xterm-256color'
    })

    print(f"Running command: {' '.join(cmd)}")

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

    print(f"Process started with PID: {process.pid}")

    # Read output for a few seconds
    start_time = time.time()
    while time.time() - start_time < 5:
        if process.poll() is not None:
            print(f"Process ended with code: {process.returncode}")
            break

        try:
            # Try to read some output
            data = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    None, process.stdout.read, 1024
                ),
                timeout=0.5
            )

            if data:
                text = data.decode('utf-8', errors='replace')
                print(f"Received output: {repr(text)}")
            else:
                print("No data available")

        except asyncio.TimeoutError:
            print("Timeout - no data available")
        except Exception as e:
            print(f"Error reading: {e}")

        await asyncio.sleep(0.1)

    # Clean up
    if process.poll() is None:
        process.terminate()
        await asyncio.sleep(1)
        if process.poll() is None:
            process.kill()

    print("Test completed")

if __name__ == "__main__":
    asyncio.run(test_simple_command())