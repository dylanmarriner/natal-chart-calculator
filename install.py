#!/usr/bin/env python3
"""
install.py
Automated installation script for the natal chart calculator.
Handles dependency installation and setup for all platforms.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def download_ephemeris():
    """Download required ephemeris files"""
    print("🌌 Downloading ephemeris files...")
    
    try:
        from skyfield.api import load
        print("   Downloading DE421 ephemeris (this may take a moment)...")
        eph = load('de421.bsp')
        print("✅ Ephemeris files downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to download ephemeris: {e}")
        print("   You can download manually from: https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/")
        return False

def create_desktop_shortcut():
    """Create desktop shortcut for easy access"""
    print("🖥️  Creating desktop shortcut...")
    
    try:
        import platform
        
        if platform.system() == "Windows":
            # Create Windows shortcut (basic approach)
            try:
                import winshell
                from win32com.client import Dispatch
                
                desktop = winshell.desktop()
                path = os.path.join(desktop, "Natal Chart Calculator.lnk")
                target = sys.executable
                wDir = os.path.dirname(os.path.abspath(__file__))
                icon = os.path.join(wDir, "icon.ico") if os.path.exists("icon.ico") else target
                
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.Arguments = f'"{os.path.join(wDir, "desktop_gui.py")}"'
                shortcut.WorkingDirectory = wDir
                shortcut.IconLocation = icon
                shortcut.save()
                
            except ImportError:
                print("⚠️  Windows shortcut creation requires pywin32. Install with: pip install pywin32")
                print("   You can still run the application manually with: python3 desktop_gui.py")
            
        elif platform.system() == "Darwin":  # macOS
            # Create macOS app
            app_dir = os.path.expanduser("~/Desktop/NatalChartCalculator.app")
            os.makedirs(f"{app_dir}/Contents/MacOS", exist_ok=True)
            os.makedirs(f"{app_dir}/Contents/Resources", exist_ok=True)
            
            # Create Info.plist
            info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>launch.sh</string>
    <key>CFBundleName</key>
    <string>Natal Chart Calculator</string>
    <key>CFBundleVersion</key>
    <string>2.0.0</string>
</dict>
</plist>'''
            
            with open(f"{app_dir}/Contents/Info.plist", "w") as f:
                f.write(info_plist)
            
            # Create launch script
            launch_script = f'''#!/bin/bash
cd "{os.path.dirname(os.path.abspath(__file__))}"
python3 desktop_gui.py
'''
            with open(f"{app_dir}/Contents/MacOS/launch.sh", "w") as f:
                f.write(launch_script)
            os.chmod(f"{app_dir}/Contents/MacOS/launch.sh", 0o755)
            
        else:  # Linux
            # Create desktop entry
            desktop_entry = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=Natal Chart Calculator
Comment=Professional natal chart calculator with compatibility analysis
Exec=python3 {os.path.abspath("desktop_gui.py")}
Icon=applications-utilities
Terminal=false
Categories=Science;Education;
'''
            
            desktop_dir = os.path.expanduser("~/.local/share/applications")
            os.makedirs(desktop_dir, exist_ok=True)
            
            with open(f"{desktop_dir}/natal-chart-calculator.desktop", "w") as f:
                f.write(desktop_entry)
            
        print("✅ Desktop shortcut created")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")
        print("   You can still run the application manually")
        return False

def test_installation():
    """Test if the installation works"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import skyfield
        import swisseph
        import customtkinter
        import pandas
        print("✅ All modules imported successfully")
        
        # Test basic calculation
        from calculations import normalize_angle
        result = normalize_angle(450)
        assert result == 90, f"Expected 90, got {result}"
        print("✅ Basic calculations working")
        
        return True
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def main():
    """Main installation process"""
    print("🚀 Natal Chart Calculator - Installation")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed during dependency setup")
        sys.exit(1)
    
    # Download ephemeris
    if not download_ephemeris():
        print("\n⚠️  Warning: Ephemeris download failed")
        print("   The application may not work correctly")
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Installation completed successfully!")
    print("\n🎯 To run the application:")
    print("   • Desktop shortcut (if created)")
    print("   • Command line: python3 desktop_gui.py")
    print("   • Python: from desktop_gui import main(); main()")
    print("\n📚 For help and documentation:")
    print("   • README.md")
    print("   • DESKTOP_GUI.md")
    print("   • GitHub: https://github.com/dylanmarriner/natal-chart-calculator")

if __name__ == "__main__":
    main()
