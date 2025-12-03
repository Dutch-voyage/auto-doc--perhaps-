# Interactive Terminal System

A comprehensive WebSocket-based interactive terminal system that provides real-time bidirectional terminal communication with full support for Claude Code and other terminal applications.

## 🚀 Features

### Core Capabilities
- **Real-time Terminal Access**: Full interactive terminal capabilities through web interface
- **Claude Code Integration**: Complete support for Claude Code with ANSI colors and formatting
- **WebSocket Communication**: Low-latency bidirectional communication
- **Multiple Applications**: Support for Claude Code, Python REPL, Bash Shell, Node.js REPL
- **Terminal Sizing**: Dynamic terminal size synchronization between frontend and backend
- **Session Management**: Multiple concurrent terminal sessions with isolation
- **Output Buffering**: Terminal history and session persistence

### Technical Features
- **PTY Support**: Proper pseudo-terminal implementation for authentic terminal behavior
- **ANSI Escape Sequences**: Full support for colors, formatting, and terminal controls
- **xterm.js Integration**: Professional terminal emulator in the browser
- **Responsive Design**: Optimized layout that adapts to different screen sizes
- **Real-time Resizing**: Dynamic terminal size adjustment with proper signal handling

## 📁 Architecture

### Backend Components

#### `terminal_server.py`
WebSocket server that handles terminal sessions and process management:
- `TerminalSession`: Manages individual terminal sessions with PTY support
- `TerminalServer`: WebSocket server handling client connections
- Process lifecycle management with proper cleanup
- Real-time output broadcasting to connected clients
- Terminal resize support with SIGWINCH signals

#### Key Classes
```python
class TerminalSession:
    """Manages a single terminal session with interactive process"""
    def __init__(self, session_id: str, command: str, cols: int = 80, rows: int = 24)
    async def start(self) -> bool
    async def resize(self, cols: int, rows: int)
    async def send_input(self, data: str)

class TerminalServer:
    """WebSocket server for terminal sessions"""
    async def client_handler(self, websocket)
    async def handle_client_message(self, websocket, message)
```

### Frontend Components

#### `interactive_terminal.py`
Streamlit component that provides the terminal interface:
- xterm.js integration for authentic terminal experience
- WebSocket client for real-time communication
- Terminal size synchronization
- Session management UI
- Multiple application support

#### Key Features
- **Professional Terminal**: VS Code-like appearance with proper themes
- **Real-time Communication**: Instant bidirectional data flow
- **Size Consistency**: Frontend/backend terminal size synchronization
- **Multi-application Support**: Easy switching between different terminal applications

#### Frontend JavaScript API
```javascript
// Terminal initialization
const terminal = new Terminal({
    theme: { /* VS Code theme */ },
    fontSize: 13,
    cursorBlink: true,
    scrollback: 1000
});

// WebSocket communication
ws.send(JSON.stringify({
    'type': 'new_session',
    'command': command,
    'cols': cols,
    'rows': rows
}));
```

### Supporting Components

#### `start_interactive_terminal.py`
Startup script with dependency checking and proper environment setup.

#### Test Scripts
- `test_websocket_client.py`: WebSocket connection testing
- `test_simple_command.py`: Basic command execution testing
- `test_claude_interactive.py`: Claude Code interactive testing

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- Node.js (for Claude Code)
- uv package manager

### Dependencies

#### Core Dependencies
```bash
uv sync
```

#### Interactive Terminal Dependencies
```bash
uv sync --extra interactive-terminal
```

Required packages:
- `websockets>=12.0` - WebSocket server implementation
- `xterm@5.3.0` - Terminal emulator (loaded via CDN)
- `xterm-addon-fit@0.8.0` - Terminal sizing (loaded via CDN)

## 🚀 Quick Start

### 1. Start the Terminal Server
```bash
cd web_ui_env
uv run python start_interactive_terminal.py
```

Expected output:
```
🚀 Starting Interactive Terminal Server
==================================================
📍 Host: localhost
🔌 Port: 8765
🖥️ Applications: Claude Code, Python REPL, Bash Shell, Node.js REPL
🔗 WebSocket URL: ws://localhost:8765
==================================================
✅ websockets module found
✅ Terminal server started successfully!
🌐 Ready for WebSocket connections...
```

### 2. Start the Web UI
```bash
uv run streamlit run web_ui.py --server.port 8501
```

### 3. Access the Interactive Terminal
1. Open http://localhost:8501 in your browser
2. Navigate to the "Terminal" tab
3. Select "🚀 Interactive Terminal"
4. Choose your desired application (Claude Code, Python REPL, Bash, Node.js)
5. Click "🚀 Start New Session"
6. Click "🔌 Connect" in the terminal

## 📱 Usage

### Basic Operation
1. **Session Creation**: Click "Start New Session" to create a new terminal session
2. **Connection**: Click "Connect" to establish WebSocket connection
3. **Interaction**: Type commands directly in the terminal, press Enter to execute
4. **Session Management**: Use "Clear Session" to reset or start fresh

### Supported Applications

#### Claude Code
Full interactive Claude Code experience with:
- ✅ Natural language interface
- ✅ File operations and editing
- ✅ Code generation and analysis
- ✅ Development tools and utilities
- ✅ Proper terminal colors and formatting

#### Python REPL
Interactive Python shell with:
- ✅ Real-time code execution
- ✅ Proper syntax highlighting
- ✅ Multi-line support
- ✅ Import and module access

#### Bash Shell
Full bash shell access with:
- ✅ Command execution
- ✅ File system operations
- ✅ Process management
- ✅ Environment variable access

#### Node.js REPL
Interactive Node.js shell with:
- ✅ JavaScript execution
- ✅ Module loading
- ✅ NPM integration
- ✅ REPL features

### Advanced Features

#### Terminal Resizing
- Automatic size detection and synchronization
- Manual resize via "📐 Resize" button
- Dynamic adjustment to window size changes

#### Session Management
- Multiple concurrent sessions
- Session isolation and security
- Session history and buffering
- Clean session termination

## 🔧 Configuration

### Environment Variables
- `COLUMNS`: Terminal width (default: 80)
- `LINES`: Terminal height (default: 24)
- `TERM`: Terminal type (default: xterm-256color)

### Server Configuration
Default server settings in `start_interactive_terminal.py`:
- Host: localhost (127.0.0.1)
- Port: 8765
- WebSocket URL: ws://localhost:8765

### Frontend Configuration
Terminal settings in `interactive_terminal.py`:
- Font size: 13px
- Theme: VS Code Dark
- Scrollback: 1000 lines
- Timeout: 500ms for WebSocket operations

## 🐛 Troubleshooting

### Common Issues

#### Server Won't Start
```bash
# Check dependencies
uv sync --extra interactive-terminal

# Verify Python and Node.js installation
python --version
node --version
```

#### No Terminal Output
1. Check server logs for output reader activity
2. Verify WebSocket connection status
3. Ensure proper application command paths
4. Check for permission issues

#### Connection Issues
1. Verify port 8765 is not blocked
2. Check firewall settings
3. Ensure both servers are running
4. Test with simple WebSocket client

### Debug Mode

#### Enable Debug Logging
```python
# In terminal_server.py
logging.basicConfig(level=logging.DEBUG)
```

#### Test WebSocket Connection
```bash
uv run python test_websocket_client.py
```

#### Test Simple Commands
```bash
uv run python test_simple_command.py
uv run python test_claude_interactive.py
```

## 🏗️ Development

### Architecture Overview

```
┌─────────────────┐    WebSocket     ┌─────────────────┐
│   Frontend       │◄─────────────────►│   Backend        │
│  (Streamlit)     │                  │  (WebSocket)     │
│                 │                  │                 │
│ ┌─────────────┐  │                  │ ┌─────────────┐  │
│ │ xterm.js    │  │                  │ │ Terminal    │  │
│ │ Terminal    │  │                  │ │ Sessions    │  │
│ │ + WebSocket│  │                  │ │ + PTY       │  │
│ └─────────────┘  │                  │ └─────────────┘  │
└─────────────────┘                  └─────────────────┘
        │                                    │
        │                              ┌─────────────┐
        │                              │   Claude     │
        │                              │   Code       │
        │                              │   Other Apps │
        └─────────────────────────────►│               │
                                       └─────────────┘
```

### Adding New Applications

1. **Update Application List** in `interactive_terminal.py`:
```python
applications = {
    "Claude Code": "/home/yyx/.nvm/versions/node/v22.18.0/bin/claude",
    "Custom App": "/path/to/your/app",
    # Add your application here
}
```

2. **Test the Application**:
```bash
# Test with manual command
uv run python test_claude_interactive.py
# Modify for your application command
```

### Extending Functionality

#### Custom Commands
Add new message types in `terminal_server.py`:
```python
elif data['type'] == 'custom_command':
    # Handle custom functionality
    pass
```

#### Frontend Features
Extend `interactive_terminal.py` JavaScript:
```javascript
// Add new WebSocket message handling
case 'custom_response':
    // Handle custom server responses
    break;
```

## 📝 API Reference

### WebSocket Messages

#### Client → Server

##### New Session
```json
{
    "type": "new_session",
    "command": "/path/to/command",
    "cols": 80,
    "rows": 24
}
```

##### Input
```json
{
    "type": "input",
    "data": "user input text\n"
}
```

##### Resize
```json
{
    "type": "resize",
    "cols": 100,
    "rows": 30
}
```

#### Server → Client

##### Session Created
```json
{
    "type": "session_created",
    "session_id": "uuid-string",
    "status": {
        "session_id": "uuid-string",
        "command": "/path/to/command",
        "is_active": true,
        "process_running": true,
        "client_count": 1
    }
}
```

##### Output
```json
{
    "type": "output",
    "data": "terminal output text",
    "timestamp": 1234567890.123,
    "session_id": "uuid-string"
}
```

##### Input Echo
```json
{
    "type": "input",
    "data": "user input text",
    "timestamp": 1234567890.123,
    "session_id": "uuid-string"
}
```

## 🔒 Security Considerations

### Session Isolation
- Each session runs in isolated process
- Separate PTY for each session
- No session data sharing between users

### Input Validation
- Command path validation
- Input sanitization
- Process execution limits

### Network Security
- Localhost-only binding by default
- WebSocket authentication (can be extended)
- CORS considerations for browser access

## 📈 Performance

### Optimization Features
- **Non-blocking I/O**: Async/await pattern for responsive operation
- **Output Buffering**: Efficient data handling and transmission
- **Connection Pooling**: Reuse of WebSocket connections
- **Memory Management**: Automatic cleanup of ended sessions

### Resource Limits
- **Session Buffer**: 1000 messages per session
- **Read Timeout**: 500ms for output reading
- **Connection Timeout**: Configurable WebSocket timeouts
- **Process Limits**: Automatic process cleanup on session end

## 🤝 Contributing

### Development Setup
1. Clone the repository
2. Install dependencies: `uv sync --extra interactive-terminal`
3. Start development servers
4. Test changes with provided test scripts

### Testing
```bash
# Run all tests
uv run python test_*.py

# Specific tests
uv run python test_websocket_client.py
uv run python test_simple_command.py
uv run python test_claude_interactive.py
```

## 📄 License

This interactive terminal system is part of the material collection project. See the main project LICENSE file for details.

## 🆘 Support

For issues, questions, or contributions:
1. Check this documentation for common solutions
2. Review the troubleshooting section
3. Examine server logs for detailed error information
4. Test with provided diagnostic tools

---

**Version**: 1.0.0
**Last Updated**: 2025-12-03
**Author**: Interactive Terminal Development Team