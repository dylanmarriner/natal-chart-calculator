#!/bin/bash
# Desktop GUI Launcher Script for Linux/macOS
# Automatically sets up virtual environment and launches the GUI

set -e

echo "🌟 Enhanced Natal Chart Calculator - Desktop GUI Launcher"
echo "=========================================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if tkinter is available
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "❌ Error: tkinter is not installed. Please install python3-tk:"
    echo "   sudo apt install python3-tk  # Ubuntu/Debian"
    echo "   brew install python-tk       # macOS"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "gui_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv gui_env
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to create virtual environment. Please install python3-venv:"
        echo "   sudo apt install python3-venv  # Ubuntu/Debian"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source gui_env/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q customtkinter pandas pytz skyfield swisseph

# Check for Swiss Ephemeris
echo "🔍 Checking Swiss Ephemeris..."
if python3 -c "import swisseph; swisseph.swe_set_ephe_path('/usr/share/libswe/ephe:/usr/share/swisseph:/usr/local/share/swisseph/')" 2>/dev/null; then
    echo "✅ Swiss Ephemeris configured"
else
    echo "⚠️  Swiss Ephemeris not found. Chiron calculations may not work."
    echo "   Install with: sudo apt install swe-basic-data  # Ubuntu/Debian"
    echo "   Or: brew install swisseph                       # macOS"
fi

# Launch the GUI
echo "🚀 Launching Desktop GUI..."
python desktop_gui.py

echo "✅ GUI session ended. Thank you for using the Enhanced Natal Chart Calculator!"
