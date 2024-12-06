"""
Janito - Language-Driven Software Development Assistant
"""
from .version import __version__
from .console import JanitoConsole
import sys

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['--version', '-v']:
        print(f"Janito version {__version__}")
        return
    
    console = JanitoConsole()
    console.run()
