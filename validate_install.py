#!/usr/bin/env python3
"""
CoomerDL Installation Validator
Checks if all dependencies are properly installed
"""
import sys
import platform
import importlib.util
from pathlib import Path

# Color codes
if platform.system() == "Windows":
    try:
        import colorama
        colorama.init()
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        RESET = '\033[0m'
    except ImportError:
        GREEN = YELLOW = RED = RESET = ''
else:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def check_module(module_name, optional=False):
    """Check if a Python module can be imported."""
    spec = importlib.util.find_spec(module_name)
    if spec is not None:
        print(f"{GREEN}✓{RESET} {module_name}")
        return True
    else:
        marker = f"{YELLOW}⚠{RESET}" if optional else f"{RED}✗{RESET}"
        status = "(optional)" if optional else "(required)"
        print(f"{marker} {module_name} {status}")
        return not optional

def check_file(filepath, description):
    """Check if a file exists."""
    path = Path(filepath)
    if path.exists():
        print(f"{GREEN}✓{RESET} {description}: {filepath}")
        return True
    else:
        print(f"{RED}✗{RESET} {description}: {filepath} (not found)")
        return False

def main():
    """Run all validation checks."""
    print("="*60)
    print("CoomerDL Installation Validator")
    print("="*60)
    
    print(f"\nPython Version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print()
    
    all_ok = True
    
    # Check Python version
    print("Checking Python Version...")
    if sys.version_info >= (3, 8):
        print(f"{GREEN}✓{RESET} Python 3.8+ (found {sys.version_info.major}.{sys.version_info.minor})")
    else:
        print(f"{RED}✗{RESET} Python 3.8+ required (found {sys.version_info.major}.{sys.version_info.minor})")
        all_ok = False
    print()
    
    # Check core dependencies
    print("Checking Core Dependencies...")
    core_modules = [
        ('requests', False),
        ('urllib3', False),
        ('bs4', False),  # beautifulsoup4
        ('PIL', False),  # Pillow
        ('psutil', False),
    ]
    
    for module, optional in core_modules:
        if not check_module(module, optional):
            all_ok = False
    print()
    
    # Check downloader engines
    print("Checking Downloader Engines...")
    downloader_modules = [
        ('yt_dlp', False),
        ('gallery_dl', False),
        ('cloudscraper', False),
        ('selenium', True),
    ]
    
    for module, optional in downloader_modules:
        if not check_module(module, optional):
            all_ok = False
    print()
    
    # Check GUI dependencies
    print("Checking GUI Dependencies...")
    gui_modules = [
        ('tkinter', False),
        ('customtkinter', False),
        ('tkinterdnd2', False),
        ('tkinterweb', True),
        ('markdown2', True),
    ]
    
    gui_available = True
    for module, optional in gui_modules:
        if not check_module(module, optional):
            if not optional:
                gui_available = False
    
    if not gui_available:
        print(f"\n{YELLOW}⚠{RESET} GUI not available - can run in headless mode only")
    print()
    
    # Check web backend dependencies
    print("Checking Web Backend Dependencies...")
    web_modules = [
        ('fastapi', True),
        ('uvicorn', True),
        ('pydantic', True),
        ('websockets', True),
        ('sqlalchemy', True),
    ]
    
    web_available = True
    for module, optional in web_modules:
        if not check_module(module, True):
            web_available = False
    
    if not web_available:
        print(f"\n{YELLOW}⚠{RESET} Web backend not fully available")
    print()
    
    # Check important files
    print("Checking Project Files...")
    files = [
        ('main.py', 'Main entry point'),
        ('requirements.txt', 'Requirements file'),
        ('README.md', 'Documentation'),
        ('downloader/factory.py', 'Downloader factory'),
        ('app/ui.py', 'UI module'),
    ]
    
    for filepath, description in files:
        if not check_file(filepath, description):
            all_ok = False
    print()
    
    # Check virtual environment
    print("Checking Virtual Environment...")
    venv_exists = Path("venv").exists()
    if venv_exists:
        print(f"{GREEN}✓{RESET} Virtual environment found")
    else:
        print(f"{YELLOW}⚠{RESET} No virtual environment (venv) found")
        print(f"   Consider running: python -m venv venv")
    print()
    
    # Final summary
    print("="*60)
    if all_ok:
        print(f"{GREEN}✓ All checks passed!{RESET}")
        print("\nCoomerDL is ready to use. Run it with:")
        print("  python main.py")
    else:
        print(f"{RED}✗ Some checks failed{RESET}")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
        
        if platform.system() == "Linux" and not gui_available:
            print("\nFor GUI support on Linux, install tkinter:")
            print("  sudo apt install python3-tk")
    print("="*60)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nValidation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Error during validation: {e}{RESET}")
        sys.exit(1)
