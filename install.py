#!/usr/bin/env python3
"""
CoomerDL Universal Installer
Works on Windows, macOS, and Linux
"""
import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

# Color codes for terminal output
class Colors:
    if platform.system() == "Windows":
        # Windows color codes (ANSI)
        try:
            import colorama
            colorama.init()
            GREEN = '\033[92m'
            YELLOW = '\033[93m'
            RED = '\033[91m'
            BLUE = '\033[94m'
            RESET = '\033[0m'
        except ImportError:
            GREEN = YELLOW = RED = BLUE = RESET = ''
    else:
        # Unix color codes
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BLUE = '\033[94m'
        RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*50}{Colors.RESET}")
    print(f"{Colors.BLUE}{text:^50}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*50}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ required, but found {version.major}.{version.minor}")
        print("\nPlease install Python 3.8 or higher from:")
        print("https://www.python.org/downloads/")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_command(cmd, name=None):
    """Check if a command is available."""
    if name is None:
        name = cmd
    return shutil.which(cmd) is not None

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    print("\nChecking for FFmpeg...")
    if check_command('ffmpeg'):
        print_success("FFmpeg is installed")
        return True
    else:
        print_warning("FFmpeg not found (optional)")
        print("  FFmpeg is needed for video merging. You can install it:")
        if platform.system() == "Windows":
            print("  - winget install ffmpeg")
            print("  - Or download from: https://ffmpeg.org/download.html")
        elif platform.system() == "Darwin":
            print("  - brew install ffmpeg")
        else:
            print("  - sudo apt install ffmpeg (Ubuntu/Debian)")
            print("  - sudo dnf install ffmpeg (Fedora)")
            print("  - sudo pacman -S ffmpeg (Arch)")
        return False

def create_venv():
    """Create virtual environment."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("\nVirtual environment already exists.")
        response = input("Recreate it? (y/N): ").strip().lower()
        if response == 'y':
            print("Removing old virtual environment...")
            shutil.rmtree(venv_path)
        else:
            print_success("Using existing virtual environment")
            return True
    
    print("\nCreating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to create virtual environment")
        print("\nTry installing venv:")
        if platform.system() == "Linux":
            print("  sudo apt install python3-venv")
        return False

def get_pip_path():
    """Get path to pip in virtual environment."""
    if platform.system() == "Windows":
        return Path("venv/Scripts/pip.exe")
    else:
        return Path("venv/bin/pip")

def get_python_path():
    """Get path to python in virtual environment."""
    if platform.system() == "Windows":
        return Path("venv/Scripts/python.exe")
    else:
        return Path("venv/bin/python")

def install_requirements():
    """Install Python requirements."""
    pip_path = get_pip_path()
    
    if not pip_path.exists():
        print_error("Virtual environment pip not found")
        return False
    
    print("\nUpgrading pip...")
    try:
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print_success("pip upgraded")
    except subprocess.CalledProcessError as e:
        print_warning("Failed to upgrade pip (continuing anyway)")
    
    print("\nInstalling CoomerDL dependencies...")
    print("This may take a few minutes...")
    
    try:
        # Install main requirements
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"],
                      check=True)
        print_success("Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies")
        print("\nTry running manually:")
        print(f"  {pip_path} install -r requirements.txt")
        return False

def test_installation():
    """Test if installation was successful."""
    print("\nTesting installation...")
    python_path = get_python_path()
    
    test_code = "import requests, yt_dlp; print('OK')"
    try:
        result = subprocess.run([str(python_path), "-c", test_code],
                              check=True, capture_output=True, text=True)
        if "OK" in result.stdout:
            print_success("Core modules working")
            return True
    except subprocess.CalledProcessError:
        pass
    
    # Test GUI modules (may fail on headless systems)
    test_gui = "import customtkinter; print('OK')"
    try:
        result = subprocess.run([str(python_path), "-c", test_gui],
                              check=True, capture_output=True, text=True)
        if "OK" in result.stdout:
            print_success("GUI modules working")
    except subprocess.CalledProcessError:
        print_warning("GUI modules not available (headless mode only)")
    
    return True

def create_launcher():
    """Create a launcher script."""
    print("\nCreating launcher script...")
    
    if platform.system() == "Windows":
        launcher = Path("start_coomerdl.bat")
        content = """@echo off
call venv\\Scripts\\activate.bat
python main.py %*
pause
"""
    else:
        launcher = Path("start_coomerdl.sh")
        content = """#!/bin/bash
source venv/bin/activate
python main.py "$@"
"""
    
    with open(launcher, 'w') as f:
        f.write(content)
    
    if platform.system() != "Windows":
        os.chmod(launcher, 0o755)
    
    print_success(f"Created {launcher}")

def print_instructions():
    """Print post-installation instructions."""
    print_header("Installation Complete!")
    
    print("To run CoomerDL:\n")
    
    if platform.system() == "Windows":
        print("  Option 1: Double-click start_coomerdl.bat")
        print("  Option 2: Run in terminal:")
        print("    venv\\Scripts\\activate")
        print("    python main.py")
    else:
        print("  Option 1: ./start_coomerdl.sh")
        print("  Option 2: Run in terminal:")
        print("    source venv/bin/activate")
        print("    python main.py")
    
    print("\nFor help and documentation:")
    print("  - README.md")
    print("  - https://github.com/primoscope/CoomerDL")
    print()

def main():
    """Main installation function."""
    print_header("CoomerDL Universal Installer")
    
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check optional dependencies
    check_ffmpeg()
    
    # Check for tkinter (Linux only)
    if platform.system() == "Linux":
        print("\nChecking for tkinter...")
        try:
            import tkinter
            print_success("tkinter is installed")
        except ImportError:
            print_warning("tkinter not found (needed for GUI)")
            print("  Install with: sudo apt install python3-tk")
    
    # Create virtual environment
    if not create_venv():
        return 1
    
    # Install requirements
    if not install_requirements():
        return 1
    
    # Test installation
    if not test_installation():
        print_warning("Installation may not be complete")
    
    # Create launcher
    create_launcher()
    
    # Print instructions
    print_instructions()
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
