import os
from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
from typing import Callable, Optional

"""
File watching system for Janito.
Monitors Python files for changes and triggers callbacks when modifications occur.
Provides debouncing and filtering capabilities to handle file system events efficiently.
"""

class PackageFileHandler(FileSystemEventHandler):
    """Watches for changes in Python package files and triggers restart callbacks"""
    def __init__(self, callback: Callable[[str, str], None], base_path: str = '.'):
        super().__init__()
        self.callback = callback
        self.last_modified = time.time()
        self.package_dir = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
        self.watched_extensions = {'.py'}
        self.debounce_time = 1
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        current_time = time.time()
        if current_time - self.last_modified < self.debounce_time:
            return
            
        file_path = Path(event.src_path)
        if file_path.suffix not in self.watched_extensions:
            return
            
        event_path = os.path.normpath(os.path.abspath(event.src_path))
        try:
            rel_path = os.path.relpath(event_path, self.package_dir)
            if not rel_path.startswith('..'):  # File is within package
                self.last_modified = current_time
                print(f"\nJanito package file modified: {rel_path}")
                self.callback(event.src_path, file_path.read_text())
        except Exception as e:
            print(f"\nError processing file {event_path}: {e}")

class FileWatcher:
    """File system watcher for auto-restart functionality"""
    def __init__(self, callback: Callable[[str, str], None], base_path: str = '.'):
        self.observer: Optional[Observer] = None
        self.handler = PackageFileHandler(callback, base_path)
        self.base_path = os.path.abspath(base_path)
        self.is_running = False  # Add state tracking
        
    def start(self):
        """Start watching for file changes"""
        try:
            if not self.is_running:
                self.is_running = True
                print(f"🔍 Monitoring Janito package in: {self.base_path}")
                print("⚡ Auto-restart enabled for package modifications")
                print()  # Add empty print for spacing
                self.observer = Observer()
                self.observer.schedule(self.handler, self.base_path, recursive=True)
                self.observer.start()
        except Exception as e:
            print(f"Failed to start file watcher: {e}")
        
    def stop(self):
        if self.observer and self.is_running:
            try:
                self.is_running = False
                self.observer.stop()
                # Add timeout to prevent hanging
                self.observer.join(timeout=1.0)
            except RuntimeError as e:
                if "cannot join current thread" not in str(e):
                    print(f"Warning: Error stopping file watcher: {e}")
            except Exception as e:
                print(f"Failed to stop file watcher: {e}")
            finally:
                self.observer = None