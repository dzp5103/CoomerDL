# CoomerDL Installation Guide

Complete guide for installing CoomerDL on any platform.

## Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation Methods](#installation-methods)
4. [Platform-Specific Instructions](#platform-specific-instructions)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Updating](#updating)
8. [Uninstalling](#uninstalling)

---

## Quick Start

### Fastest Method (All Platforms)

```bash
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL
python install.py
```

This automated installer handles everything for you!

---

## System Requirements

### Minimum Requirements

- **Python**: 3.8 or higher
- **RAM**: 512 MB
- **Disk Space**: 500 MB (more for downloads)
- **Operating System**: Windows 7+, macOS 10.12+, or Linux (any modern distro)

### Recommended Requirements

- **Python**: 3.10 or higher
- **RAM**: 2 GB
- **Disk Space**: 2 GB+
- **FFmpeg**: For video merging (optional but recommended)

### Optional Components

- **FFmpeg**: Required for merging video/audio streams
- **tkinter**: Required for GUI (usually included with Python)
- **Redis/PostgreSQL**: Only for web application deployment

---

## Installation Methods

CoomerDL offers multiple installation methods to suit different needs:

### 1. Easy Installer (Recommended) ⭐

**Best for**: Everyone, especially beginners

```bash
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL
python install.py
```

**What it does**:
- ✅ Checks system requirements
- ✅ Creates virtual environment
- ✅ Installs all dependencies
- ✅ Tests installation
- ✅ Creates launcher scripts

**Run after installation**:
- Windows: `start_coomerdl.bat`
- Mac/Linux: `./start_coomerdl.sh`

### 2. Pre-built Executable (Windows Only)

**Best for**: Windows users who don't want to install Python

1. Download `CoomerDL-Windows.zip` from [Releases](https://github.com/primoscope/CoomerDL/releases)
2. Extract to a folder
3. Run `CoomerDL.exe`

**Note**: Windows Defender may show a warning. This is normal for unsigned executables.

### 3. Manual Installation

**Best for**: Advanced users who want full control

```bash
# Clone repository
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### 4. pip Install (Development)

**Best for**: Developers or system-wide installation

```bash
# Clone repository
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL

# Install as package
pip install -e .

# Run from anywhere
coomerdl "https://example.com/video"
```

### 5. Docker (Coming Soon)

**Best for**: Containerized deployments

```bash
docker run -v $(pwd)/downloads:/downloads primoscope/coomerdl
```

---

## Platform-Specific Instructions

### Windows

#### Prerequisites

1. **Install Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during installation
   - Verify: `python --version`

2. **Install Git** (optional)
   - Download from [git-scm.com](https://git-scm.com/download/win)
   - Or use GitHub Desktop

3. **Install FFmpeg** (optional)
   ```cmd
   winget install ffmpeg
   ```
   Or download from [ffmpeg.org](https://ffmpeg.org/download.html)

#### Installation Steps

**Option A: Easy Installer**
```cmd
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL
python install.py
```

**Option B: Windows Batch Script**
```cmd
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL
install_windows.bat
```

**Option C: Pre-built Executable**
- Download and extract `CoomerDL-Windows.zip`
- Run `CoomerDL.exe`

#### Running

- Double-click `start_coomerdl.bat`
- Or run in CMD: `python main.py`

---

### macOS

#### Prerequisites

1. **Install Homebrew** (package manager)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python 3.8+**
   ```bash
   brew install python@3.11
   ```
   Verify: `python3 --version`

3. **Install Git**
   ```bash
   brew install git
   ```

4. **Install FFmpeg** (optional)
   ```bash
   brew install ffmpeg
   ```

#### Installation Steps

```bash
# Clone repository
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL

# Run installer
python3 install.py
```

#### Running

```bash
./start_coomerdl.sh
```

---

### Linux

#### Prerequisites

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip python3-tk git ffmpeg
```

**Fedora**:
```bash
sudo dnf install python3 python3-tkinter git ffmpeg
```

**Arch Linux**:
```bash
sudo pacman -S python python-pip tk git ffmpeg
```

#### Installation Steps

**Option A: Easy Installer**
```bash
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL
python3 install.py
```

**Option B: Linux Script**
```bash
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL
./scripts/install_linux.sh
```

#### Running

```bash
./start_coomerdl.sh
```

#### Headless/Server Mode

For servers without GUI:

```bash
# Install without GUI components
sudo apt install python3 python3-venv python3-pip git ffmpeg

# Clone and setup
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run in headless mode
export HEADLESS=true
python main.py
```

---

## Verification

After installation, verify everything works:

### Automated Verification

```bash
python validate_install.py
```

This checks:
- ✅ Python version
- ✅ Core dependencies
- ✅ Downloader engines
- ✅ GUI components
- ✅ Project files

### Manual Verification

```bash
# Test imports
python -c "import requests, yt_dlp, gallery_dl; print('OK')"

# Test GUI (if not headless)
python -c "import customtkinter; print('GUI OK')"

# Run help
python main.py --help

# Test download
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

---

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'tkinter'"

**Linux**: Install tkinter
```bash
sudo apt install python3-tk      # Ubuntu/Debian
sudo dnf install python3-tkinter # Fedora
sudo pacman -S tk               # Arch
```

**Windows/macOS**: Reinstall Python from [python.org](https://www.python.org/)

#### "python: command not found"

- Ensure Python is installed
- Check it's in PATH: `echo $PATH`
- Try `python3` instead of `python`

#### "pip: command not found"

```bash
python -m pip install --upgrade pip
```

#### "FFmpeg not found"

FFmpeg is optional but recommended:
- Windows: `winget install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

#### "Permission denied" on Linux/macOS

Make scripts executable:
```bash
chmod +x install.py start_coomerdl.sh
```

#### Virtual environment not activating

**Windows**:
```cmd
# Allow scripts to run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
venv\Scripts\activate
```

**Mac/Linux**:
```bash
source venv/bin/activate
```

#### Installation fails with "externally-managed-environment"

Use virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Getting More Help

If you still have issues:

1. Check [GitHub Issues](https://github.com/primoscope/CoomerDL/issues)
2. Read the [Troubleshooting Guide](docs/user/TROUBLESHOOTING.md)
3. Create a new issue with:
   - Your OS and version
   - Python version: `python --version`
   - Full error message
   - Steps to reproduce

---

## Updating

### Update CoomerDL

```bash
cd CoomerDL

# Pull latest changes
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Or re-run installer
python install.py
```

### Update Only Dependencies

```bash
cd CoomerDL
source venv/bin/activate  # if using venv
pip install -r requirements.txt --upgrade
```

---

## Uninstalling

### Remove CoomerDL

```bash
# Delete the entire folder
rm -rf CoomerDL  # Mac/Linux
rmdir /s CoomerDL  # Windows
```

### Remove Python Packages

If you installed system-wide:
```bash
pip uninstall coomerdl
```

### Clean Uninstall

```bash
# Remove application data
rm -rf ~/.coomerdl  # Mac/Linux
del /s %APPDATA%\coomerdl  # Windows

# Remove downloads (optional)
rm -rf ~/Downloads/CoomerDL  # or your download folder
```

---

## Next Steps

After installation:

1. **Read the [Getting Started Guide](docs/user/GETTING_STARTED.md)**
2. **Explore [Features](docs/user/FEATURES.md)**
3. **Check [FAQ](docs/user/FAQ.md)**
4. **Join the community and star the repo! ⭐**

---

**Need help?** Open an [issue](https://github.com/primoscope/CoomerDL/issues) on GitHub!
