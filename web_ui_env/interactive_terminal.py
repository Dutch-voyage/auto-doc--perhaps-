#!/usr/bin/env python3
"""
Interactive Terminal Component for Streamlit
WebSocket-based terminal with xterm.js frontend
"""

import streamlit as st
import json
import asyncio
import uuid
import time
from typing import Dict, Optional
import threading

# Global state for terminal sessions
if 'terminal_sessions' not in st.session_state:
    st.session_state.terminal_sessions = {}

class InteractiveTerminal:
    """Interactive terminal with WebSocket backend"""

    def __init__(self, server_url: str = "ws://localhost:8765"):
        self.server_url = server_url
        self.current_session_id = None

    def render_terminal_html(self, session_id: Optional[str] = None, command: str = None) -> str:
        """Generate HTML for the interactive terminal"""
        session_id = session_id or str(uuid.uuid4())

        html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Interactive Terminal</title>

    <!-- Load xterm.js CSS and JS from CDN -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@5.3.0/css/xterm.css" />
    <script src="https://cdn.jsdelivr.net/npm/xterm@5.3.0/lib/xterm.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.8.0/lib/xterm-addon-fit.js"></script>

    <style>
        body {{
            margin: 0;
            padding: 5px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1e1e1e;
            color: #ffffff;
            overflow: hidden;
        }}

        #terminal-container {{
            background-color: #000000;
            border: 1px solid #333333;
            border-radius: 5px;
            height: 520px;
            min-height: 400px;
            overflow: hidden;
            position: relative;
            margin: 5px 0;
            width: 100%;
        }}

        #terminal {{
            height: 100%;
            width: 100%;
            min-height: 400px;
        }}

        #controls {{
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }}

        .control-btn {{
            padding: 8px 16px;
            background-color: #007acc;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-family: inherit;
            transition: background-color 0.2s;
        }}

        .control-btn:hover {{
            background-color: #005a9e;
        }}

        .control-btn:disabled {{
            background-color: #666666;
            cursor: not-allowed;
        }}

        #status {{
            background-color: #2d2d30;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 12px;
            color: #cccccc;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }}

        .status-connected {{ color: #4ec9b0; }}
        .status-disconnected {{ color: #f44747; }}
        .status-connecting {{ color: #ffcc02; }}

        .status-info {{
            display: flex;
            gap: 15px;
            align-items: center;
        }}

        /* Custom scrollbar for better appearance */
        ::-webkit-scrollbar {{
            width: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: #1e1e1e;
        }}

        ::-webkit-scrollbar-thumb {{
            background: #555555;
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #777777;
        }}
    </style>
</head>
<body>
    <div id="terminal-container">
        <div id="controls">
            <button class="control-btn" id="connect-btn" onclick="connectTerminal()">🔌 Connect</button>
            <button class="control-btn" id="disconnect-btn" onclick="disconnectTerminal()" disabled>🔌 Disconnect</button>
            <button class="control-btn" id="clear-btn" onclick="clearTerminal()">🗑️ Clear</button>
            <button class="control-btn" id="resize-btn" onclick="resizeTerminal()">📐 Resize</button>
        </div>

        <div id="terminal"></div>

        <div id="status">
            <div class="status-info">
                <span class="status-disconnected" id="connection-status">🔌 Disconnected</span>
                <span>Session: <span id="session-id">None</span></span>
                <span>Buffer: <span id="buffer-size">0</span> lines</span>
            </div>
        </div>
    </div>

    <script>
        let ws = null;
        let sessionId = '{session_id}';
        let isConnected = false;
        let command = '{command or "/home/yyx/.nvm/versions/node/v22.18.0/bin/claude"}';
        let terminal = null;
        let fitAddon = null;

        // Initialize xterm.js terminal
        function initTerminal() {{
            // Create terminal instance with optimized sizing for Streamlit
            terminal = new Terminal({{
                theme: {{
                    background: '#000000',
                    foreground: '#ffffff',
                    cursor: '#ffffff',
                    selection: '#ffffff40',
                    black: '#000000',
                    red: '#f44747',
                    green: '#4ec9b0',
                    yellow: '#ffcc02',
                    blue: '#007acc',
                    magenta: '#c586c0',
                    cyan: '#9cdcfe',
                    white: '#ffffff',
                    brightBlack: '#666666',
                    brightRed: '#f44747',
                    brightGreen: '#4ec9b0',
                    brightYellow: '#ffcc02',
                    brightBlue: '#007acc',
                    brightMagenta: '#c586c0',
                    brightCyan: '#9cdcfe',
                    brightWhite: '#ffffff'
                }},
                fontSize: 13,
                fontFamily: 'Consolas, Monaco, "Courier New", monospace',
                lineHeight: 1.1,
                cursorBlink: true,
                cursorStyle: 'block',
                scrollback: 2000,
                tabStopWidth: 4,
                cols: 80,
                rows: 30
            }});

            // Add fit addon for proper sizing
            const FitAddon = window.FitAddon;
            fitAddon = new FitAddon.FitAddon();
            terminal.loadAddon(fitAddon);

            // Open terminal in the container
            terminal.open(document.getElementById('terminal'));

            // Fit terminal to container with better timing
            setTimeout(() => {{
                fitAddon.fit();
                // Ensure minimum size
                if (terminal.cols < 80) terminal.resize(80, terminal.rows);
                if (terminal.rows < 24) terminal.resize(terminal.cols, 24);

                window.addEventListener('resize', () => {{
                    setTimeout(() => {{
                        fitAddon.fit();
                        if (terminal.cols < 80) terminal.resize(80, terminal.rows);
                        if (terminal.rows < 24) terminal.resize(terminal.cols, 24);
                    }}, 50);
                }});
            }}, 200);

            // Additional resize attempts to ensure proper sizing
            setTimeout(() => {{
                fitAddon.fit();
                if (terminal.cols < 80) terminal.resize(80, terminal.rows);
                if (terminal.rows < 24) terminal.resize(terminal.cols, 24);
            }}, 500);

            setTimeout(() => {{
                fitAddon.fit();
                if (terminal.cols < 80) terminal.resize(80, terminal.rows);
                if (terminal.rows < 24) terminal.resize(terminal.cols, 24);
            }}, 1000);

            // Show welcome message
            terminal.writeln('\\x1b[36mInteractive Terminal v1.0\\x1b[0m');
            terminal.writeln('\\x1b[36mType "help" for available commands\\x1b[0m');
            terminal.writeln('');

            updateStatus('disconnected');
        }}

        // WebSocket connection
        function connectTerminal() {{
            if (isConnected) return;

            updateStatus('connecting');
            terminal.writeln('\\x1b[33mConnecting to terminal server...\\x1b[0m');

            try {{
                // Create WebSocket with proper error handling
                ws = new WebSocket('{self.server_url}');

                ws.onopen = function(event) {{
                    console.log('WebSocket connected successfully');
                    terminal.writeln('\\x1b[32m✅ Connected to terminal server\\x1b[0m');
                    updateStatus('connected');

                    // Get terminal dimensions
                    const dims = fitAddon.proposeDimensions();
                    const cols = dims ? dims.cols : 80;
                    const rows = dims ? dims.rows : 24;

                    // Create new session with size information
                    const sessionMessage = {{
                        'type': 'new_session',
                        'command': command,
                        'cols': cols,
                        'rows': rows
                    }};

                    console.log('Sending session request:', sessionMessage);
                    ws.send(JSON.stringify(sessionMessage));
                }};

                ws.onmessage = function(event) {{
                    try {{
                        const data = JSON.parse(event.data);
                        console.log('Received message:', data);
                        handleWebSocketMessage(data);
                    }} catch (e) {{
                        console.error('Failed to parse message:', e, event.data);
                        terminal.writeln('\\x1b[31mError parsing server response\\x1b[0m');
                    }}
                }};

                ws.onclose = function(event) {{
                    console.log('WebSocket disconnected. Code:', event.code, 'Reason:', event.reason);
                    updateStatus('disconnected');
                    isConnected = false;
                    updateButtons();
                    terminal.writeln('\\x1b[33m🔌 Disconnected from terminal server\\x1b[0m');
                }};

                ws.onerror = function(error) {{
                    console.error('WebSocket error:', error);
                    updateStatus('disconnected');
                    terminal.writeln('\\x1b[31m❌ WebSocket connection error. Server may be down.\\x1b[0m');

                    // Try to provide helpful error information
                    if (error.code === 1006) {{
                        terminal.writeln('\\x1b[31mConnection was closed abnormally. Check if server is running on port 8765.\\x1b[0m');
                    }}
                }};

            }} catch (error) {{
                console.error('Connection error:', error);
                updateStatus('disconnected');
                terminal.writeln('\\x1b[31m❌ Failed to connect to terminal server: ' + error.message + '\\x1b[0m');
            }}
        }}

        function disconnectTerminal() {{
            if (ws) {{
                ws.close();
                ws = null;
            }}
        }}

        function handleWebSocketMessage(data) {{
            switch(data.type) {{
                case 'session_created':
                    sessionId = data.session_id;
                    isConnected = true;
                    updateStatus('connected');
                    updateButtons();
                    terminal.writeln('\\x1b[32m✅ Session created: ' + sessionId + '\\x1b[0m');
                    terminal.writeln('\\x1b[36m🚀 Starting command: ' + command + '\\x1b[0m');

                    // Add a welcome message and set up terminal input
                    setTimeout(() => {{
                        terminal.writeln('\\x1b[32mReady! You can now interact with the terminal.\\x1b[0m');
                        terminal.focus();
                    }}, 500);
                    break;

                case 'connected':
                    sessionId = data.session_id;
                    isConnected = true;
                    updateStatus('connected');
                    updateButtons();
                    terminal.writeln('\\x1b[32mConnected to existing session: ' + sessionId + '\\x1b[0m');
                    terminal.focus();
                    break;

                case 'output':
                    // Write terminal output directly
                    terminal.write(data.data);
                    break;

                case 'input':
                    // Echo input back to terminal
                    terminal.write(data.data);
                    break;

                case 'error':
                    terminal.writeln('\\x1b[31mError: ' + data.message + '\\x1b[0m');
                    break;

                case 'status_response':
                    updateSessionInfo(data.status);
                    break;
            }}

            updateBufferCount();
        }}

        function sendInput(input) {{
            if (!isConnected || !ws) return;

            try {{
                ws.send(JSON.stringify({{
                    'type': 'input',
                    'data': input
                }}));
            }} catch (error) {{
                console.error('Send error:', error);
                terminal.writeln('\\x1b[31mSend error: ' + error.message + '\\x1b[0m');
            }}
        }}

        function clearTerminal() {{
            terminal.clear();
            terminal.writeln('\\x1b[36mTerminal cleared\\x1b[0m');
        }}

        function resizeTerminal() {{
            // Send terminal resize signal
            if (isConnected && ws && fitAddon) {{
                fitAddon.fit();
                const dims = fitAddon.proposeDimensions();
                const cols = dims ? dims.cols : 80;
                const rows = dims ? dims.rows : 24;

                ws.send(JSON.stringify({{
                    'type': 'resize',
                    'cols': cols,
                    'rows': rows
                }}));

                console.log(`Terminal resized to ${{cols}}x${{rows}}`);
            }}
        }}

        function updateStatus(status) {{
            const statusElement = document.getElementById('connection-status');
            statusElement.className = 'status-' + status;
            statusElement.textContent = status === 'connected' ? '🟢 Connected' :
                                      status === 'connecting' ? '🟡 Connecting' : '🔌 Disconnected';

            document.getElementById('session-id').textContent = sessionId || 'None';
        }}

        function updateButtons() {{
            document.getElementById('connect-btn').disabled = isConnected;
            document.getElementById('disconnect-btn').disabled = !isConnected;
        }}

        function updateBufferCount() {{
            // For xterm.js, buffer count is the terminal's buffer length
            if (terminal && terminal.buffer) {{
                const lines = terminal.buffer.length;
                document.getElementById('buffer-size').textContent = lines;
            }}
        }}

        function updateSessionInfo(status) {{
            if (status.client_count !== undefined) {{
                // Update connection count if needed
            }}
        }}

        // Initialize on load
        window.onload = function() {{
            initTerminal();

            // Set up terminal input handling
            if (terminal) {{
                terminal.onData((data) => {{
                    sendInput(data);
                }});
            }}

            // Auto-connect if command is provided
            if (command && command !== 'None') {{
                setTimeout(connectTerminal, 500);
            }}
        }};

        // Clean up on unload
        window.onbeforeunload = function() {{
            disconnectTerminal();
        }};
    </script>
</body>
</html>
        """

        return html_code

    def render_interactive_terminal(self, app_name: str = "Claude Code", command: str = None):
        """Render the interactive terminal interface"""

        if command is None:
            if app_name == "Claude Code":
                command = "/home/yyx/.nvm/versions/node/v22.18.0/bin/claude"
            elif app_name == "Python REPL":
                command = "python3"
            elif app_name == "Bash":
                command = "bash"
            else:
                command = "bash"

        st.markdown(f"### 🖥️ Interactive Terminal - {app_name}")
        st.markdown("*Real-time terminal interface with full interactive capabilities*")

        # Instructions
        with st.expander("📖 How to Use", expanded=True):
            st.markdown(f"""
            **Interactive Terminal Features:**

            1. **🔌 Connect** - Click the Connect button to start the terminal
            2. **⌨️ Type Commands** - Enter commands and press Enter to execute
            3. **🔄 Real-time Output** - See terminal output immediately
            4. **🎯 Full Functionality** - Use all features of {app_name}

            **Current Command:** `{command}`

            **Note:** Make sure the terminal server is running on port 8765 for full functionality.
            """)

        # Session management
        if 'terminal_session_id' not in st.session_state:
            st.session_state.terminal_session_id = None

        # Control buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("🚀 Start New Session", key="start_terminal"):
                st.session_state.terminal_session_id = str(uuid.uuid4())
                st.rerun()

        with col2:
            if st.button("🗑️ Clear Session", key="clear_terminal"):
                st.session_state.terminal_session_id = None
                st.rerun()

        with col3:
            if st.button("📊 Server Status", key="server_status"):
                self.show_server_status()

        # Embed the terminal
        session_id = st.session_state.terminal_session_id

        if session_id:
            st.markdown(f"**Session ID:** `{session_id[:8]}...`")

            # Embed the interactive terminal
            terminal_html = self.render_terminal_html(session_id, command)
            st.components.v1.html(terminal_html, height=650, scrolling=False)

            st.info("""
            **Interactive Terminal Active!**

            - Click **🔌 Connect** in the terminal above to start the session
            - Type commands and press **Enter** to execute
            - Use **Tab** completion and **Arrow** keys for navigation
            - Click **🔌 Disconnect** when done
            """)

        else:
            st.warning("""
            No active terminal session. Click **"🚀 Start New Session"** to create an interactive terminal.
            """)

    def show_server_status(self):
        """Show terminal server status"""
        try:
            # Try to connect to server to check if it's running
            import requests
            response = requests.get("http://localhost:8765/status", timeout=2)
            st.success("✅ Terminal server is running")
            st.json(response.json())
        except Exception as e:
            st.error("""
            ❌ Terminal server is not running on port 8765

            **To start the server:**
            ```bash
            cd /home/yyx/data_management/material_collection/web_ui_env
            python terminal_server.py
            ```
            """)
        except Exception as e:
            st.error(f"Error checking server status: {e}")

def render_interactive_claude_terminal():
    """Render interactive Claude Code terminal"""
    terminal = InteractiveTerminal()
    terminal.render_interactive_terminal("Claude Code", "/home/yyx/.nvm/versions/node/v22.18.0/bin/claude")

def render_interactive_python_terminal():
    """Render interactive Python terminal"""
    terminal = InteractiveTerminal()
    terminal.render_interactive_terminal("Python REPL", "python3")

if __name__ == "__main__":
    render_interactive_claude_terminal()