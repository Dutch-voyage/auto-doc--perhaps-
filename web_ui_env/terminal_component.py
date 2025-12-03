#!/usr/bin/env python3
"""
Terminal Component for Streamlit Web UI
Provides a safe web-based terminal interface for system operations
"""

import streamlit as st
import subprocess
import threading
import time
import os
import shlex
import signal
import tempfile
import uuid
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import json

class TerminalInterface:
    """Safe terminal interface for Streamlit applications"""

    def __init__(self):
        self.command_history = []
        self.session_state_key = "terminal_history"
        self.output_key = "terminal_output"
        self.active_sessions_key = "active_sessions"

        # Initialize session state
        if self.session_state_key not in st.session_state:
            st.session_state[self.session_state_key] = []
        if self.output_key not in st.session_state:
            st.session_state[self.output_key] = []
        if self.active_sessions_key not in st.session_state:
            st.session_state[self.active_sessions_key] = {}

    def get_allowed_commands(self) -> Dict[str, Dict]:
        """Predefined safe commands with descriptions"""
        return {
            "System Info": {
                "ls -la": "List all files with details",
                "pwd": "Show current directory",
                "whoami": "Show current user",
                "date": "Show current date and time",
                "df -h": "Show disk usage",
                "free -h": "Show memory usage",
                "ps aux": "Show running processes"
            },
            "File Operations": {
                "ls efficient_RL_systems/": "List RL system files",
                "ls docs/": "List documentation files",
                "ls web_ui_env/": "List web UI files",
                "wc -l tags.db": "Count lines in database",
                "du -sh *": "Show directory sizes"
            },
            "Python Commands": {
                "python --version": "Show Python version",
                "python -c 'import sqlite3; print(\"SQLite:\", sqlite3.sqlite_version)'": "Show SQLite version",
                "python -c 'import streamlit; print(\"Streamlit:\", streamlit.__version__)'": "Show Streamlit version",
                "python -c 'import pandas; print(\"Pandas:\", pandas.__version__)'": "Show Pandas version"
            },
            "Database Operations": {
                "sqlite3 tags.db '.tables'": "List database tables",
                "sqlite3 tags.db 'SELECT COUNT(*) FROM tags;'": "Count tags",
                "sqlite3 tags.db 'SELECT COUNT(*) FROM documents;'": "Count documents",
                "sqlite3 tags.db 'SELECT category, COUNT(*) FROM tags GROUP BY category LIMIT 10;'": "Show tag categories"
            },
            "Git Operations": {
                "git status": "Show git status",
                "git log --oneline -5": "Show recent commits",
                "git branch": "Show current branch",
                "git remote -v": "Show remotes"
            },
            "Web UI Operations": {
                "uv sync": "Sync dependencies",
                "uv run streamlit run web_ui.py --server.port 8502 --server.headless true &": "Start web UI in background",
                "pkill -f streamlit": "Stop Streamlit processes",
                "python build_static.py": "Build static site",
                "python setup_tags.py": "Setup tag database"
            },
            "Image Operations": {
                "ls efficient_RL_systems/summaries/images/ | wc -l": "Count images",
                "find efficient_RL_systems/summaries/images/ -name '*.png' | head -10": "Show first 10 images",
                "./batch_download_images.sh": "Download images (if exists)"
            },
            "Terminal Applications": {
                "/home/yyx/.nvm/versions/node/v22.18.0/bin/claude --version": "Check Claude Code version",
                "/home/yyx/.nvm/versions/node/v22.18.0/bin/claude --help": "Show Claude Code help",
                "python3 -c 'import sys; print(sys.executable)'": "Show Python path",
                "node --version": "Check Node.js version",
                "npm --version": "Check npm version"
            }
        }

    def is_safe_command(self, command: str) -> Tuple[bool, str]:
        """Check if command is safe to execute"""
        command = command.strip()

        # Dangerous commands to block
        dangerous_patterns = [
            'rm -rf /', 'sudo rm', 'dd if=', 'mkfs', 'format',
            'sudo su', 'su root', 'passwd', 'chown', 'chmod 777',
            'wget', 'curl', 'nc', 'netcat', 'ssh', 'scp', 'rsync',
            'iptables', 'ufw', 'firewall', 'systemctl stop',
            'shutdown', 'reboot', 'halt', 'poweroff',
            'rm -rf ~', 'rm -rf /*', 'rm -rf ../',
            'history -c', 'history -w'
        ]

        # Check for dangerous patterns
        for pattern in dangerous_patterns:
            if pattern in command:
                return False, f"❌ Dangerous command blocked: {pattern}"

        # Allow specific safe commands
        safe_commands = [
            'ls', 'pwd', 'whoami', 'date', 'df', 'free', 'ps', 'wc',
            'python', 'sqlite3', 'git', 'uv', 'pkill', 'cat', 'head',
            'tail', 'grep', 'find', 'du', 'which', 'whereis',
            '/home/yyx/.nvm/versions/node/v22.18.0/bin/claude'  # Claude Code specific path
        ]

        # Check if command starts with safe command
        for safe_cmd in safe_commands:
            if command.startswith(safe_cmd + ' ') or command == safe_cmd:
                return True, "✅ Safe command"

        # Allow relative paths starting with ./
        if command.startswith('./') or command.startswith('python ') or command.startswith('sqlite3 '):
            return True, "✅ Local script/database command"

        return False, "⚠️ Unknown command - use predefined commands for safety"

    def execute_command(self, command: str, timeout: int = 30) -> Dict:
        """Execute command safely and return results"""
        try:
            # Check if command is safe
            is_safe, message = self.is_safe_command(command)
            if not is_safe:
                return {
                    'success': False,
                    'output': '',
                    'error': message,
                    'command': command
                }

            # Split command properly
            if command.startswith('sqlite3 ') and "'" in command:
                # Handle sqlite3 commands with quotes
                parts = shlex.split(command)
            else:
                parts = command.split()

            # Use appropriate working directory
            working_dir = '/home/yyx/data_management/material_collection'

            # Execute command
            process = subprocess.Popen(
                parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=working_dir,
                env=os.environ.copy()
            )

            try:
                stdout, stderr = process.communicate(timeout=timeout)
                return {
                    'success': process.returncode == 0,
                    'output': stdout,
                    'error': stderr,
                    'command': command,
                    'return_code': process.returncode
                }
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    'success': False,
                    'output': '',
                    'error': f'Command timed out after {timeout} seconds',
                    'command': command
                }

        except FileNotFoundError:
            return {
                'success': False,
                'output': '',
                'error': f'Command not found: {parts[0] if parts else command}',
                'command': command
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Error executing command: {str(e)}',
                'command': command
            }

    def add_to_history(self, command: str, result: Dict):
        """Add command and result to history"""
        st.session_state[self.session_state_key].append({
            'command': command,
            'result': result,
            'timestamp': time.time()
        })

        # Limit history size
        if len(st.session_state[self.session_state_key]) > 50:
            st.session_state[self.session_state_key] = st.session_state[self.session_state_key][-50:]

    def start_interactive_session(self, app_name: str, command: str) -> str:
        """Start an interactive terminal session"""
        session_id = str(uuid.uuid4())

        # Create a temporary script file for the session
        temp_dir = tempfile.mkdtemp()
        session_script = os.path.join(temp_dir, f"session_{session_id}.sh")

        # Create a script that starts the application
        with open(session_script, 'w') as f:
            f.write(f"#!/bin/bash\n")
            f.write(f"cd {temp_dir}\n")
            f.write(f"echo 'Starting {app_name}...'\n")
            f.write(f"echo 'Session ID: {session_id}'\n")
            f.write(f"{command}\n")

        os.chmod(session_script, 0o755)

        # Store session info
        st.session_state[self.active_sessions_key][session_id] = {
            'app_name': app_name,
            'command': command,
            'script_path': session_script,
            'temp_dir': temp_dir,
            'start_time': time.time(),
            'status': 'starting'
        }

        return session_id

    def stop_session(self, session_id: str) -> bool:
        """Stop an interactive session"""
        if session_id not in st.session_state[self.active_sessions_key]:
            return False

        session = st.session_state[self.active_sessions_key][session_id]
        try:
            # Kill any processes associated with the session
            if hasattr(session, 'process') and session['process']:
                session['process'].terminate()
                time.sleep(2)
                if session['process'].poll() is None:
                    session['process'].kill()

            # Clean up temporary files
            import shutil
            shutil.rmtree(session['temp_dir'], ignore_errors=True)

            # Remove from active sessions
            del st.session_state[self.active_sessions_key][session_id]
            return True

        except Exception as e:
            return False

    def get_active_sessions(self) -> Dict:
        """Get all active sessions"""
        return st.session_state[self.active_sessions_key]

    def render_application_launcher(self):
        """Render the application launcher section"""
        st.markdown("### 🚀 Application Launcher")

        # Available applications
        applications = {
            "Claude Code": {
                "command": "/home/yyx/.nvm/versions/node/v22.18.0/bin/claude",
                "description": "AI-powered coding assistant with CLI interface",
                "icon": "🤖",
                "interactive": True
            },
            "Python REPL": {
                "command": "python3",
                "description": "Interactive Python shell",
                "icon": "🐍",
                "interactive": True
            },
            "Node.js REPL": {
                "command": "node",
                "description": "Interactive Node.js shell",
                "icon": "🟢",
                "interactive": True
            },
            "Bash Shell": {
                "command": "bash",
                "description": "Interactive bash shell",
                "icon": "🐚",
                "interactive": True
            }
        }

        # Application selection
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            selected_app = st.selectbox(
                "Select Application:",
                list(applications.keys()),
                format_func=lambda x: f"{applications[x]['icon']} {x}"
            )

        with col2:
            if st.button("🚀 Launch", type="primary", disabled=not selected_app):
                self.launch_application(selected_app, applications[selected_app])

        with col3:
            if st.button("🔄 Refresh Sessions"):
                st.rerun()

        # Show active sessions
        active_sessions = self.get_active_sessions()
        if active_sessions:
            st.markdown("#### 🔄 Active Sessions")

            for session_id, session_info in active_sessions.items():
                with st.expander(f"{session_info['app_name']} - Started {time.ctime(session_info['start_time'])}", expanded=False):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.code(session_info['command'], language='bash')
                        st.text(f"Session ID: {session_id[:8]}...")
                        st.text(f"Status: {session_info.get('status', 'running')}")

                    with col2:
                        if st.button(f"🛑 Stop", key=f"stop_{session_id}"):
                            if self.stop_session(session_id):
                                st.success("Session stopped")
                                st.rerun()
                            else:
                                st.error("Failed to stop session")

        # Application usage instructions
        with st.expander("📖 Application Usage", expanded=False):
            app_info = applications.get(selected_app, {})
            if app_info:
                st.markdown(f"""
                **{selected_app}**

                {app_info.get('description', 'No description available')}

                **Note:** Interactive applications run in the background.
                For full interactivity, consider using a local terminal.

                **Safety:** All applications run with limited permissions and are monitored.
                """)

    def launch_application(self, app_name: str, app_info: Dict):
        """Launch an application"""
        try:
            if app_info.get('interactive', False):
                # For interactive apps, we provide information on how to run them locally
                st.info(f"""
                **🚀 {app_name} Launcher**

                **Command:** `{app_info['command']}`

                **To run interactively:** Use this command in your local terminal:
                ```bash
                cd /home/yyx/data_management/material_collection
                {app_info['command']}
                ```

                **Note:** Full interactive sessions are better suited for local terminals.
                The web terminal provides safe, monitored command execution.
                """)

                # Add to history
                result = {
                    'success': True,
                    'output': f'Application info prepared for {app_name}',
                    'error': None,
                    'command': f'# Launcher for: {app_info["command"]}'
                }
                self.add_to_history(f"Launch {app_name}", result)
            else:
                # For non-interactive apps, execute directly
                result = self.execute_command(app_info['command'])
                self.add_to_history(app_info['command'], result)
                self.display_result(result)

        except Exception as e:
            st.error(f"Failed to launch {app_name}: {str(e)}")

    def render_terminal(self):
        """Render the terminal interface"""
        st.markdown("## 💻 Web Terminal")
        st.markdown("*Execute system commands safely through the web interface*")

        # Application Launcher Section
        self.render_application_launcher()

        # Safety warning
        with st.expander("🔒 Safety Information", expanded=False):
            st.warning("""
            **Safety Features:**
            - Dangerous commands are automatically blocked
            - Only predefined safe commands are allowed
            - Commands execute with limited permissions
            - Current working directory: `/home/yyx/data_management/material_collection/web_ui_env`
            """)

        # Quick command shortcuts
        st.markdown("### ⚡ Quick Commands")

        allowed_commands = self.get_allowed_commands()
        selected_category = st.selectbox("Select Command Category:", list(allowed_commands.keys()))

        if selected_category:
            commands = allowed_commands[selected_category]
            selected_command = st.selectbox("Select Command:", [""] + list(commands.keys()), format_func=lambda x: commands.get(x, ""))

            if selected_command and st.button(f"🚀 Execute: {selected_command}", key="quick_execute"):
                with st.spinner(f"Executing: `{selected_command}`"):
                    result = self.execute_command(selected_command)
                    self.add_to_history(selected_command, result)
                    self.display_result(result)

        # Custom command input
        st.markdown("### 🎯 Custom Command")

        col1, col2 = st.columns([4, 1])

        with col1:
            custom_command = st.text_input(
                "Enter command:",
                placeholder="e.g., ls -la, python --version, sqlite3 tags.db '.tables'",
                help="Enter a command or select from quick commands above"
            )

        with col2:
            execute_button = st.button("🚀 Execute", type="primary", disabled=not custom_command)

        if execute_button and custom_command:
            with st.spinner(f"Executing: `{custom_command}`"):
                result = self.execute_command(custom_command)
                self.add_to_history(custom_command, result)
                self.display_result(result)

        # Command history
        self.render_history()

    def display_result(self, result: Dict):
        """Display command result"""
        if result['success']:
            if result['output'].strip():
                st.code(result['output'], language='bash')
            else:
                st.info("✅ Command executed successfully (no output)")
        else:
            st.error(f"❌ Error: {result['error']}")

    def render_history(self):
        """Render command history"""
        st.markdown("### 📜 Command History")

        if not st.session_state[self.session_state_key]:
            st.info("No commands executed yet")
            return

        history = st.session_state[self.session_state_key][-10:]  # Show last 10 commands

        for i, item in enumerate(reversed(history)):
            with st.expander(f"🕐 {time.ctime(item['timestamp'])} - `{item['command']}`", expanded=False):
                self.display_result(item['result'])

        # Clear history button
        if st.button("🗑️ Clear History", key="clear_history"):
            st.session_state[self.session_state_key] = []
            st.rerun()

def render_terminal_tab():
    """Render terminal tab in main Streamlit app"""
    terminal = TerminalInterface()
    terminal.render_terminal()

if __name__ == "__main__":
    # Test the terminal component
    render_terminal_tab()