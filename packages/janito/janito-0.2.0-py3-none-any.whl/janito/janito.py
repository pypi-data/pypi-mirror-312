from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.document import Document
from prompt_toolkit.completion.base import CompleteEvent
import anthropic
import os
from pathlib import Path
import json
from typing import List, Optional, AsyncGenerator, Iterable, Tuple
import asyncio
from hashlib import sha256
from datetime import datetime, timedelta
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import traceback  # Add import at the top with other imports
from rich.markdown import Markdown
from rich.console import Console
import subprocess  # Add at the top with other imports
import re  # Add to imports at top
import ast  # Add to imports at top
import tempfile
from janito.change import FileChangeHandler  # Remove unused imports
from janito.watcher import FileWatcher
from janito.claude import ClaudeAPIAgent
from rich.progress import Progress, SpinnerColumn, TextColumn  # Add to imports at top
from threading import Event
import threading
from rich.syntax import Syntax
from rich.text import Text
import typer
from typing import Optional
import readline  # Add to imports at top
import signal   # Add to imports at top
from rich.traceback import install
from janito.workspace import Workspace  # Update import
from janito.prompts import build_change_prompt, build_info_prompt, build_general_prompt, SYSTEM_PROMPT  # Add to imports

# Install rich traceback handler
install(show_locals=True)

"""
Main module for Janito - Language-Driven Software Development Assistant.
Provides the core CLI interface and command handling functionality.
Manages user interactions, file operations, and API communication with Claude.
"""

class JanitoCommands:  # Renamed from ClaudeCommands
    def __init__(self, api_key: Optional[str] = None):
        try:
            self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable is required")
            self.claude = ClaudeAPIAgent(api_key=self.api_key)
            self.change_handler = FileChangeHandler()
            self.console = Console()
            self.debug = False
            self.stop_progress = Event()
            self.system_message = SYSTEM_PROMPT
            self.workspace = Workspace()  # Add workspace instance
        except Exception as e:
            raise ValueError(f"Failed to initialize Janito: {e}")

    def _get_files_content(self) -> str:
        return self.workspace.get_files_content()

    def _build_context(self, request: str, request_type: str = "general") -> str:
        """Build context with workspace status and files content"""
        workspace_status = self.get_workspace_status()
        files_content = self._get_files_content()
        
        return f"""=== WORKSPACE STRUCTURE ===
{workspace_status}

=== FILES CONTENT ===
{files_content}

=== {request_type.upper()} REQUEST ===
{request}"""

    def send_message(self, message: str) -> str:
        try:
            if self.debug:
                print("\n[Debug] Sending request to Claude")
            
            # Build general context prompt
            prompt = build_general_prompt(
                self.get_workspace_status(),
                self._get_files_content(),
                message
            )
            
            # Use claude agent to send message
            response_text = self.claude.send_message(prompt)
            self.last_response = response_text
            return response_text
            
        except Exception as e:
            raise RuntimeError(f"Failed to process message: {e}")

    def _display_file_content(self, filepath: Path) -> None:
        """Display file content with syntax highlighting"""
        try:
            with open(filepath) as f:
                content = f.read()
            syntax = Syntax(content, "python", theme="monokai", line_numbers=True)
            self.console.print("\nFile content:", style="bold red")
            self.console.print(syntax)
        except Exception as e:
            self.console.print(f"Could not read file {filepath}: {e}", style="bold red")

    def handle_file_change(self, request: str) -> str:
        """Handle file modification request starting with !"""
        try:
            # Build change context prompt
            prompt = build_change_prompt(
                self.get_workspace_status(), 
                self._get_files_content(),
                request
            )
            
            # Get response from Claude
            response = self.claude.send_message(prompt)
            
            # Process changes
            success = self.change_handler.process_changes(response)
            
            if not success:
                return "Failed to process file changes. Please check the response format."
            
            return "File changes applied successfully."
            
        except Exception as e:
            raise RuntimeError(f"Failed to process file changes: {e}")

            raise RuntimeError(f"Failed to load history: {e}")

    def clear_console(self) -> str:
        """Clear the console"""
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
            return "Console cleared"
        except Exception as e:
            return f"Error clearing console: {str(e)}"

    def get_workspace_status(self) -> str:
        return self.workspace.get_workspace_status()

    def show_workspace(self) -> str:
        """Show directory structure and Python files in current workspace"""
        try:
            status = self.get_workspace_status()
            print("\nWorkspace structure:")
            print("=" * 80)
            print(status)
            return ""
        except Exception as e:
            raise RuntimeError(f"Failed to show workspace: {e}")

    def handle_info_request(self, request: str, workspace_status: str) -> str:
        """Handle information request ending with ?"""
        try:
            # Build info context prompt
            prompt = build_info_prompt(
                self._get_files_content(),
                request
            )
            
            # Get response and render markdown
            response = self.claude.send_message(prompt)
            md = Markdown(response)
            self.console.print(md)
            return ""
            
        except Exception as e:
            raise RuntimeError(f"Failed to process information request: {e}")

    def get_last_response(self) -> str:
        """Get the last sent and received message to/from Claude"""
        if not self.claude.last_response:
            return "No previous conversation available."

        output = []
        if self.claude.last_full_message:
            output.append(Text("\n=== Last Message Sent ===\n", style="bold yellow"))
            output.append(Text(self.claude.last_full_message + "\n"))
        output.append(Text("\n=== Last Response Received ===\n", style="bold green"))  
        output.append(Text(self.claude.last_response))
        
        self.console.print(*output)
        return ""

    def show_file(self, filepath: str) -> str:
        """Display file content with syntax highlighting"""
        try:
            path = Path(filepath)
            if not path.exists():
                return f"Error: File not found - {filepath}"
            if not path.is_file():
                return f"Error: Not a file - {filepath}"
            
            self._display_file_content(path)
            return ""
        except Exception as e:
            return f"Error displaying file: {str(e)}"

    def toggle_debug(self) -> str:
        """Toggle debug mode on/off"""
        self.debug = not self.debug
        # Also toggle debug on the Claude agent
        if hasattr(self, 'claude') and self.claude:
            self.claude.debug = self.debug
        return f"Debug mode {'enabled' if self.debug else 'disabled'}"

    def check_syntax(self) -> str:
        """Check all Python files in the workspace for syntax errors"""
        try:
            errors = []
            for file in self.workspace.base_path.rglob("*.py"):
                try:
                    with open(file, "r") as f:
                        content = f.read()
                    ast.parse(content)
                except SyntaxError as e:
                    errors.append(f"Syntax error in {file}: {e}")
            
            if errors:
                return "\n".join(errors)
            return "No syntax errors found."
        except Exception as e:
            return f"Error checking syntax: {e}"

    def run_python(self, filepath: str) -> str:
        """Run a Python file"""
        try:
            path = Path(filepath)
            if not path.exists():
                return f"Error: File not found - {filepath}"
            if not path.is_file():
                return f"Error: Not a file - {filepath}"
            if not filepath.endswith('.py'):
                return f"Error: Not a Python file - {filepath}"
                
            self.console.print(f"\n[cyan]Running Python file: {filepath}[/cyan]")
            self.console.print("=" * 80)
            
            result = subprocess.run([sys.executable, str(path)], 
                                  capture_output=True, 
                                  text=True)
            
            if result.stdout:
                self.console.print("\n[green]Output:[/green]")
                print(result.stdout)
            if result.stderr:
                self.console.print("\n[red]Errors:[/red]")
                print(result.stderr)
                
            return ""
        except Exception as e:
            return f"Error running file: {str(e)}"

    def edit_file(self, filepath: str) -> str:
        """Open file in system editor"""
        try:
            path = Path(filepath)
            if not path.exists():
                return f"Error: File not found - {filepath}"
            if not path.is_file():
                return f"Error: Not a file - {filepath}"

            # Get system editor - try VISUAL then EDITOR then fallback to nano
            editor = os.getenv('VISUAL') or os.getenv('EDITOR') or 'nano'
            
            try:
                result = subprocess.run([editor, str(path)])
                if result.returncode != 0:
                    return f"Editor exited with error code {result.returncode}"
                return f"Finished editing {filepath}"
            except FileNotFoundError:
                return f"Error: Editor '{editor}' not found"
                
        except Exception as e:
            return f"Error editing file: {str(e)}"

import typer
import traceback
from pathlib import Path
import os
from janito.console import JanitoConsole
from rich.console import Console

class CLI:
    """Command-line interface handler for Janito using Typer"""
    def __init__(self):
        self.console = Console()
        self.app = typer.Typer(
            help="Janito - Language-Driven Software Development Assistant",
            add_completion=False,
            no_args_is_help=False,
        )
        self._setup_commands()

    def _setup_commands(self):
        """Setup Typer commands"""
        @self.app.callback(invoke_without_command=True)
        def callback(version: bool = typer.Option(False, "--version", "-v", help="Show version and exit")):
            """Janito - Language-Driven Software Development Assistant"""
            if version:
                from janito import __version__
                self.console.print(f"Janito version {__version__}")
                raise typer.Exit()

        @self.app.command()
        def start(
            workspace: Optional[str] = typer.Argument(None, help="Optional workspace directory to change to"),
            debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
            no_watch: bool = typer.Option(False, "--no-watch", help="Disable file watching"),
        ):
            """Start Janito interactive console"""
            try:
                # Change to workspace directory if provided
                if workspace:
                    workspace_path = Path(workspace).resolve()
                    if not workspace_path.exists():
                        self.console.print(f"\nError: Workspace directory does not exist: {workspace_path}")
                        raise typer.Exit(1)
                    os.chdir(workspace_path)

                console = JanitoConsole()
                if workspace:
                    console.workspace = workspace_path  # Store workspace path
                if debug:
                    console.janito.debug = True
                if no_watch:
                    if console.watcher:
                        console.watcher.stop()
                        console.watcher = None
                
                # Print workspace info after file watcher setup
                if workspace:
                    print("\n" + "="*50)
                    print(f"🚀 Working on project: {workspace_path.name}")
                    print(f"📂 Path: {workspace_path}")
                    print("="*50 + "\n")
                    
                console.run()

            except Exception as e:
                print(f"\nFatal error: {str(e)}")
                print("\nTraceback:")
                traceback.print_exc()
                raise typer.Exit(1)

    def run(self):
        """Run the CLI application"""
        self.app()

def run_cli():
    """Main entry point"""
    cli = CLI()
    cli.run()