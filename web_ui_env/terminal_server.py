#!/usr/bin/env python3
"""
WebSocket Terminal Server for Interactive Sessions
Provides real-time bidirectional terminal communication
"""

import asyncio
import websockets
import json
import subprocess
import threading
import time
import os
import uuid
import signal
import pty
import select
import errno
import logging
import fcntl
import termios
import struct
from typing import Set, Dict, Any, Optional
from websockets.server import WebSocketServerProtocol
import tempfile

# Import settings manager
from settings_manager import settings_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TerminalSession:
    """Manages a single terminal session with interactive process"""

    def __init__(self, session_id: str, command: str, working_dir: str = None, cols: int = 80, rows: int = 24):
        self.session_id = session_id
        self.command = command
        # Load default working directory from settings
        self.working_dir = working_dir or settings_manager.get_setting("terminal", "default_working_dir")
        self.process = None
        self.pty_fd = None
        self.master_fd = None  # Master end of PTY
        self.slave_fd = None   # Slave end of PTY
        self.start_time = time.time()
        self.buffer = []
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.is_active = False
        self.cols = cols
        self.rows = rows

    async def start(self):
        """Start the terminal session with proper PTY"""
        try:
            # Create PTY
            self.master_fd, self.slave_fd = pty.openpty()

            # Set terminal size
            self._set_pty_size(self.master_fd, self.cols, self.rows)

            # Set non-blocking mode
            fcntl.fcntl(self.master_fd, fcntl.F_SETFL, os.O_NONBLOCK)

            # Prepare command and environment
            if self.command.strip() in ['bash', '/bin/bash']:
                cmd = ['/bin/bash', '-i']
            else:
                cmd = self.command.split()

            env = os.environ.copy()
            env.update({
                'COLUMNS': str(self.cols),
                'LINES': str(self.rows),
                'TERM': 'xterm-256color'
            })

            # Fork and create process
            pid = os.fork()

            if pid == 0:  # Child process
                # Set up slave PTY
                os.setsid()

                # Make slave PTY the controlling terminal
                os.dup2(self.slave_fd, 0)  # stdin
                os.dup2(self.slave_fd, 1)  # stdout
                os.dup2(self.slave_fd, 2)  # stderr

                # Close master FD in child
                os.close(self.master_fd)

                # Close slave FD after dup
                os.close(self.slave_fd)

                # Change to working directory
                if self.working_dir:
                    os.chdir(self.working_dir)

                # Execute command
                try:
                    os.execve(cmd[0], cmd, env)
                except OSError as e:
                    logger.error(f"Failed to exec {cmd[0]}: {e}")
                    os._exit(1)

            else:  # Parent process
                # Store the child process PID
                self.process = pid

                # Close slave FD in parent
                if self.slave_fd is not None:
                    try:
                        os.close(self.slave_fd)
                    except:
                        pass
                    self.slave_fd = None

                self.is_active = True
                logger.info(f"Started terminal session {self.session_id}: {self.command} ({self.cols}x{self.rows}) with PID {pid}")

                # Start output reader
                asyncio.create_task(self._read_output())

                return True

        except Exception as e:
            logger.error(f"Failed to start session {self.session_id}: {e}")
            # Clean up on failure
            if self.master_fd is not None:
                try:
                    os.close(self.master_fd)
                except:
                    pass
            if self.slave_fd is not None:
                try:
                    os.close(self.slave_fd)
                except:
                    pass
            return False

    def _set_pty_size(self, fd, cols, rows):
        """Set PTY terminal size"""
        try:
            # TIOCSWINSZ ioctl call to set window size
            # Format: 4 unsigned short values (rows, cols, x_pixels, y_pixels)
            s = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(fd, termios.TIOCSWINSZ, s)
        except Exception as e:
            logger.warning(f"Could not set PTY size: {e}")

    async def _read_output(self):
        """Read output from the PTY continuously and broadcast to clients"""
        logger.info(f"Starting PTY output reader for session {self.session_id}")

        read_count = 0
        try:
            while self.is_active and self.master_fd is not None:
                try:
                    # Use select to check if data is available
                    ready, _, _ = select.select([self.master_fd], [], [], 0.1)

                    if ready:
                        # Data is available, read it
                        try:
                            data = os.read(self.master_fd, 8192)

                            if data:
                                read_count += 1
                                # Decode binary data properly
                                try:
                                    text = data.decode('utf-8', errors='replace')
                                except:
                                    text = data.decode('latin-1', errors='replace')

                                # Log output activity (less frequent to avoid flooding)
                                if read_count % 10 == 0 or (text.strip() and len(text.strip()) > 5):
                                    logger.info(f"Read output #{read_count} from {self.session_id}: {len(data)} bytes, preview: {repr(text[:50])}")

                                # Send output message immediately
                                message = {
                                    'type': 'output',
                                    'data': text,
                                    'timestamp': time.time(),
                                    'session_id': self.session_id
                                }

                                # Store in buffer
                                self.buffer.append(message)
                                if len(self.buffer) > 1000:  # Limit buffer size
                                    self.buffer.pop(0)

                                # Broadcast to all connected clients
                                await self._broadcast(message)
                                if len(self.clients) > 0:
                                    logger.debug(f"Broadcast output to {len(self.clients)} clients for session {self.session_id}")

                        except OSError as e:
                            if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                                # No data available right now
                                await asyncio.sleep(0.01)
                            else:
                                logger.error(f"Error reading from PTY {self.session_id}: {e}")
                                await asyncio.sleep(0.1)
                    else:
                        # No data available, small delay
                        await asyncio.sleep(0.05)

                except Exception as e:
                    logger.error(f"Error in PTY select/read loop for {self.session_id}: {e}")
                    await asyncio.sleep(0.1)

                # Check if child process is still alive
                try:
                    # Send signal 0 to check if process is alive
                    os.kill(self.process, 0)
                except (OSError, ProcessLookupError):
                    logger.info(f"Process {self.session_id} ended")
                    break

        except Exception as e:
            logger.error(f"Fatal error in PTY output reader for {self.session_id}: {e}")
        finally:
            logger.info(f"PTY output reader for {self.session_id} stopped after {read_count} reads")

    async def resize(self, cols: int, rows: int):
        """Resize the terminal"""
        try:
            if cols != self.cols or rows != self.rows:
                old_cols, old_rows = self.cols, self.rows
                self.cols = cols
                self.rows = rows
                logger.info(f"Resized PTY {self.session_id} from {old_cols}x{old_rows} to {cols}x{rows}")

                # Set PTY size
                if self.master_fd:
                    self._set_pty_size(self.master_fd, cols, rows)

                # Send SIGWINCH to process to notify of resize
                if self.process:
                    try:
                        os.kill(self.process, signal.SIGWINCH)
                    except (ProcessLookupError, PermissionError):
                        # Process may have ended
                        pass
        except Exception as e:
            logger.error(f"Error resizing PTY {self.session_id}: {e}")

    async def send_input(self, data: str):
        """Send input to the terminal process via PTY"""
        try:
            if self.master_fd is not None and self.is_active:
                # Convert string to bytes for PTY
                if isinstance(data, str):
                    data_bytes = data.encode('utf-8')
                else:
                    data_bytes = data

                # Write to PTY master file descriptor
                os.write(self.master_fd, data_bytes)

                # Echo input back to clients
                message = {
                    'type': 'input',
                    'data': data if isinstance(data, str) else data.decode('utf-8', errors='replace'),
                    'timestamp': time.time(),
                    'session_id': self.session_id
                }
                await self._broadcast(message)

        except BrokenPipeError:
            # Process ended, this is normal behavior
            logger.info(f"Session {self.session_id} process ended (broken pipe)")
            self.is_active = False
        except OSError as e:
            if e.errno == errno.EPIPE:  # Broken pipe
                logger.info(f"Session {self.session_id} process ended")
                self.is_active = False
            elif e.errno == errno.EAGAIN:  # Would block
                pass  # Try again later
            else:
                logger.error(f"OS error sending input to {self.session_id}: {e}")
        except Exception as e:
            logger.error(f"Error sending input to {self.session_id}: {e}")

    async def _broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if self.clients:
            disconnected = []
            for client in self.clients.copy():
                try:
                    await client.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    disconnected.append(client)
                except Exception as e:
                    logger.error(f"Error broadcasting to client: {e}")
                    disconnected.append(client)

            # Remove disconnected clients
            for client in disconnected:
                self.clients.discard(client)

    def add_client(self, client: websockets.WebSocketServerProtocol):
        """Add a client to this session"""
        self.clients.add(client)

        # Send buffer history to new client
        for message in self.buffer:
            asyncio.create_task(client.send(json.dumps(message)))

    def remove_client(self, client: websockets.WebSocketServerProtocol):
        """Remove a client from this session"""
        self.clients.discard(client)

    async def stop(self):
        """Stop the terminal session and clean up PTY"""
        self.is_active = False

        # Close PTY file descriptors
        if self.master_fd is not None:
            try:
                os.close(self.master_fd)
            except Exception as e:
                logger.warning(f"Error closing master PTY: {e}")
            self.master_fd = None

        if self.slave_fd is not None:
            try:
                os.close(self.slave_fd)
            except Exception as e:
                logger.warning(f"Error closing slave PTY: {e}")
            self.slave_fd = None

        # Terminate the process
        if self.process:
            try:
                # Send SIGTERM for graceful shutdown
                os.kill(self.process, signal.SIGTERM)

                # Wait a bit for graceful shutdown
                await asyncio.sleep(2)

                # Force kill if still running
                try:
                    os.kill(self.process, 0)  # Check if still alive
                    os.kill(self.process, signal.SIGKILL)
                except (ProcessLookupError, OSError):
                    pass  # Process already ended

            except Exception as e:
                logger.error(f"Error stopping process: {e}")

        # Clear clients
        self.clients.clear()

    def get_status(self) -> dict:
        """Get session status"""
        process_running = False
        if self.process:
            try:
                # Check if process is still alive
                os.kill(self.process, 0)
                process_running = True
            except (ProcessLookupError, OSError):
                process_running = False

        return {
            'session_id': self.session_id,
            'command': self.command,
            'start_time': self.start_time,
            'is_active': self.is_active,
            'process_running': process_running,
            'pty_attached': self.master_fd is not None,
            'client_count': len(self.clients),
            'buffer_size': len(self.buffer)
        }

class TerminalServer:
    """WebSocket server for terminal sessions"""

    def __init__(self, port: int = 8765):
        self.port = port
        self.sessions: Dict[str, TerminalSession] = {}
        self.client_sessions: Dict[websockets.WebSocketServerProtocol, str] = {}

    async def register_client(self, websocket, path):
        """Register a new client connection"""
        try:
            # Wait for initial message (session connect or new session)
            message = await websocket.recv()
            data = json.loads(message)

            if data['type'] == 'connect':
                session_id = data['session_id']

                if session_id in self.sessions:
                    # Connect to existing session
                    session = self.sessions[session_id]
                    session.add_client(websocket)
                    self.client_sessions[websocket] = session_id

                    response = {
                        'type': 'connected',
                        'session_id': session_id,
                        'status': session.get_status()
                    }
                    await websocket.send(json.dumps(response))

                    logger.info(f"Client connected to session {session_id}")
                else:
                    # Session not found
                    response = {'type': 'error', 'message': f'Session {session_id} not found'}
                    await websocket.send(json.dumps(response))

            elif data['type'] == 'new_session':
                # Create new session
                session_id = str(uuid.uuid4())
                command = data['command']
                cols = data.get('cols', 80)
                rows = data.get('rows', 24)

                session = TerminalSession(session_id, command, cols=cols, rows=rows)
                self.sessions[session_id] = session
                self.client_sessions[websocket] = session_id
                session.add_client(websocket)

                # Start the session
                if await session.start():
                    response = {
                        'type': 'session_created',
                        'session_id': session_id,
                        'status': session.get_status()
                    }
                else:
                    response = {'type': 'error', 'message': 'Failed to start session'}
                    del self.sessions[session_id]

                await websocket.send(json.dumps(response))

        except Exception as e:
            logger.error(f"Error registering client: {e}")
            await websocket.close()

    async def handle_client_message(self, websocket, message):
        """Handle incoming message from client"""
        try:
            data = json.loads(message)
            session_id = self.client_sessions.get(websocket)

            if session_id and session_id in self.sessions:
                session = self.sessions[session_id]

                if data['type'] == 'input':
                    await session.send_input(data['data'])

                elif data['type'] == 'resize':
                    # Handle terminal resize
                    cols = data.get('cols', session.cols)
                    rows = data.get('rows', session.rows)
                    await session.resize(cols, rows)

                elif data['type'] == 'status':
                    response = {
                        'type': 'status_response',
                        'status': session.get_status()
                    }
                    await websocket.send(json.dumps(response))

        except Exception as e:
            logger.error(f"Error handling client message: {e}")

    async def unregister_client(self, websocket):
        """Unregister a client connection"""
        session_id = self.client_sessions.get(websocket)

        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
            session.remove_client(websocket)

            # If no more clients and session is inactive, clean up
            if not session.clients and not session.is_active:
                await session.stop()
                del self.sessions[session_id]
                logger.info(f"Cleaned up session {session_id}")

        if websocket in self.client_sessions:
            del self.client_sessions[websocket]

    async def client_handler(self, websocket):
        """Handle WebSocket client connection"""
        try:
            # Extract path from websocket if needed
            path = getattr(websocket, 'path', '')
            await self.register_client(websocket, path)

            # Handle messages
            async for message in websocket:
                await self.handle_client_message(websocket, message)

        except websockets.exceptions.ConnectionClosed:
            logger.info("Client connection closed")
        except Exception as e:
            logger.error(f"Error in client handler: {e}")
        finally:
            await self.unregister_client(websocket)

    async def start_server(self):
        """Start the WebSocket server"""
        logger.info(f"Starting terminal server on port {self.port}")

        return await websockets.serve(
            self.client_handler,
            "0.0.0.0",
            self.port,
            ping_interval=20,
            ping_timeout=10
        )

    def get_session_info(self) -> dict:
        """Get information about all active sessions"""
        return {
            'active_sessions': len(self.sessions),
            'total_clients': len(self.client_sessions),
            'sessions': {
                session_id: session.get_status()
                for session_id, session in self.sessions.items()
            }
        }

async def main():
    """Main server function"""
    server = TerminalServer()

    # Start the server
    server_task = await server.start_server()

    logger.info("Terminal server started successfully!")
    logger.info("Connect to: ws://localhost:8765")

    # Keep server running
    try:
        await server_task.wait_closed()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")

        # Stop all sessions
        for session in server.sessions.values():
            await session.stop()

if __name__ == "__main__":
    asyncio.run(main())