@echo off
REM Desktop GUI Launcher Script for Windows
REM Automatically sets up virtual environment and launches the GUI

echo 🌟 Enhanced Natal Chart Calculator - Desktop GUI Launcher
echo ==========================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed. Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Check if tkinter is available
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: tkinter is not available. Please reinstall Python with tkinter included
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "gui_env" (
    echo 📦 Creating virtual environment...
    python -m venv gui_env
    if errorlevel 1 (
        echo ❌ Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call gui_env\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -q customtkinter pandas pytz skyfield swisseph

REM Check for Swiss Ephemeris
echo 🔍 Checking Swiss Ephemeris...
python -c "import swisseph; swisseph.swe_set_ephe_path('C:\\swisseph\\ephe')" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Swiss Ephemeris not found. Chiron calculations may not work.
    echo    Download from: https://www.astro.com/ftp/swisseph/ephe/
    echo    Extract to C:\swisseph\ephe\
)

REM Launch the GUI
echo 🚀 Launching Desktop GUI...
python desktop_gui.py

echo ✅ GUI session ended. Thank you for using the Enhanced Natal Chart Calculator!
pause
