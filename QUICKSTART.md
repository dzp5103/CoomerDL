# CoomerDL Quick Start Guide

Get up and running with CoomerDL in 5 minutes! 🚀

## The Fastest Way

### One-Command Installation

```bash
git clone https://github.com/primoscope/CoomerDL.git && cd CoomerDL && python install.py
```

That's it! The installer will handle everything automatically.

---

## Step-by-Step (First Time Users)

### 1. Check Prerequisites

Make sure you have Python 3.8 or higher:

```bash
python --version
```

Don't have Python? Download it from [python.org](https://www.python.org/downloads/)

### 2. Get CoomerDL

Download the code:

```bash
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL
```

Or download the ZIP from GitHub and extract it.

### 3. Run the Installer

```bash
python install.py
```

The installer will:
- ✅ Check your system
- ✅ Install dependencies
- ✅ Set everything up
- ✅ Create a launcher

### 4. Launch CoomerDL

**Windows**:
```cmd
start_coomerdl.bat
```

**Mac/Linux**:
```bash
./start_coomerdl.sh
```

**Or manually**:
```bash
python main.py
```

### 5. Download Something!

1. Paste a URL into the input box
2. Choose what to download (images, videos, etc.)
3. Click "Download"
4. Watch it work! ✨

---

## Common URLs to Try

Test CoomerDL with these sites:

- **YouTube**: `https://www.youtube.com/watch?v=...`
- **Twitter/X**: `https://twitter.com/user/status/...`
- **Reddit**: `https://www.reddit.com/r/.../comments/...`
- **Coomer**: `https://coomer.su/onlyfans/user/...`
- **Erome**: `https://www.erome.com/a/...`

---

## Quick Tips

### Batch Downloads

Paste multiple URLs (one per line) to download them all at once:

```
https://example.com/video1
https://example.com/video2
https://example.com/video3
```

### Settings

Click the gear icon (⚙️) to configure:
- Download location
- File filters (skip images/videos)
- Proxy settings
- Network options

### Command Line

You can also use CoomerDL from the command line:

```bash
python main.py "https://example.com/video"
python main.py --batch-file urls.txt
python main.py --help
```

---

## Need Help?

### Installation Issues?

Run the validator to check your setup:

```bash
python validate_install.py
```

### Still Stuck?

1. Check [INSTALL.md](INSTALL.md) for detailed instructions
2. Read [TROUBLESHOOTING.md](docs/user/TROUBLESHOOTING.md)
3. Check [FAQ.md](docs/user/FAQ.md)
4. Open an [issue](https://github.com/primoscope/CoomerDL/issues) on GitHub

---

## Next Steps

Once you're comfortable with the basics:

- 📖 Read the [Full Features Guide](docs/user/FEATURES.md)
- 🌐 Learn about [Web Deployment](DEPLOYMENT.md)
- ⚙️ Explore [Advanced Settings](docs/user/FEATURES.md#settings-reference)
- 🔧 Check out [Developer Docs](README.md#for-developers)

---

## Quick Reference Card

| Action | How |
|--------|-----|
| **Install** | `python install.py` |
| **Run** | `python main.py` |
| **Validate** | `python validate_install.py` |
| **Update** | `git pull && pip install -r requirements.txt --upgrade` |
| **Help** | `python main.py --help` |
| **GUI Mode** | `python main.py` |
| **CLI Mode** | `python main.py "URL"` |
| **Batch** | `python main.py --batch-file urls.txt` |
| **Headless** | `export HEADLESS=true && python main.py` |

---

## Platform-Specific Quick Starts

### Windows

```cmd
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL
python install.py
start_coomerdl.bat
```

### macOS

```bash
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL
python3 install.py
./start_coomerdl.sh
```

### Linux

```bash
sudo apt install python3 python3-tk git  # Ubuntu/Debian
git clone https://github.com/primoscope/CoomerDL.git
cd CoomerDL
python3 install.py
./start_coomerdl.sh
```

---

**Happy downloading! 🎉**

If you find CoomerDL useful, please ⭐ star the repository on GitHub!
