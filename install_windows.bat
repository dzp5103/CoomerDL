@echo off
REM CoomerDL Windows Installer
REM Easy installation script for Windows users

echo ========================================
echo    CoomerDL Windows Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check Python version
for /f "tokens=2" %%i in ('python --version') do set PYVERSION=%%i
echo Detected Python version: %PYVERSION%
echo.

REM Ask about FFmpeg
echo FFmpeg is optional but recommended for video merging.
echo.
set /p INSTALL_FFMPEG="Do you want to install FFmpeg? (y/n, default=y): "
if "%INSTALL_FFMPEG%"=="" set INSTALL_FFMPEG=y

if /i "%INSTALL_FFMPEG%"=="y" (
    echo.
    echo Checking for FFmpeg...
    ffmpeg -version >nul 2>&1
    if %errorlevel% neq 0 (
        echo FFmpeg not found. Please install it manually:
        echo - Using winget: winget install ffmpeg
        echo - Or download from: https://ffmpeg.org/download.html
        echo.
        echo You can continue without FFmpeg, but video merging won't work.
        pause
    ) else (
        echo [OK] FFmpeg is already installed
        ffmpeg -version | findstr "ffmpeg version"
    )
)
echo.

REM Create virtual environment
echo Creating Python virtual environment...
if exist venv (
    echo Virtual environment already exists.
    set /p RECREATE="Recreate it? (y/n, default=n): "
    if /i "%RECREATE%"=="y" (
        echo Removing old virtual environment...
        rmdir /s /q venv
        python -m venv venv
        echo [OK] Virtual environment recreated
    )
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip upgraded
echo.

REM Install requirements
echo Installing CoomerDL dependencies...
echo This may take a few minutes...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Test installation
echo Testing installation...
python -c "import customtkinter, requests, yt_dlp; print('[OK] Core modules imported successfully')" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Some modules failed to import.
    echo This might be okay if you're running in headless mode.
)
echo.

echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo To run CoomerDL:
echo   1. Run: start_coomerdl.bat
echo   OR
echo   2. Activate venv: venv\Scripts\activate.bat
echo      Then run: python main.py
echo.
echo To uninstall:
echo   - Delete the entire CoomerDL folder
echo.
echo For help and documentation:
echo   - README.md
echo   - https://github.com/primoscope/CoomerDL
echo.

REM Create convenient launcher script
echo Creating launcher script...
(
echo @echo off
echo call venv\Scripts\activate.bat
echo python main.py %%*
echo pause
) > start_coomerdl.bat
echo [OK] Created start_coomerdl.bat
echo.

echo You can now run CoomerDL by double-clicking start_coomerdl.bat
echo.
pause
