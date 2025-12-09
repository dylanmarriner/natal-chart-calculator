#!/usr/bin/env python3
"""
build_installer.py
PyInstaller script to create distributable installer for the natal chart calculator.
Creates standalone executables for Windows, Mac, and Linux.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully")

def create_spec_file():
    """Create PyInstaller spec file for optimal packaging"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['desktop_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('de421.bsp', '.'),
        ('theme.py', '.'),
        ('*.py', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'tkinter',
        'sqlite3',
        'pandas',
        'pytz',
        'skyfield',
        'swisseph',
        'numpy',
        'matplotlib',
        'PIL',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NatalChartCalculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('natal_chart_calculator.spec', 'w') as f:
        f.write(spec_content)
    print("✅ Created PyInstaller spec file")

def build_executable():
    """Build the standalone executable"""
    print("🔨 Building standalone executable...")
    
    # Clean previous builds
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Build executable
    try:
        subprocess.check_call([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--onefile',
            '--windowed',
            '--name=NatalChartCalculator',
            '--add-data=de421.bsp:.',
            '--add-data=theme.py:.',
            '--hidden-import=customtkinter',
            '--hidden-import=swisseph',
            '--hidden-import=skyfield',
            '--hidden-import=pandas',
            '--hidden-import=pytz',
            'desktop_gui.py'
        ])
        print("✅ Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_installer_scripts():
    """Create platform-specific installer scripts"""
    
    # Windows batch script
    windows_script = '''@echo off
echo Installing Natal Chart Calculator...
echo.
echo This will install the Natal Chart Calculator on your system.
echo.
pause

if not exist "%PROGRAMFILES%\\NatalChartCalculator" mkdir "%PROGRAMFILES%\\NatalChartCalculator"
copy "NatalChartCalculator.exe" "%PROGRAMFILES%\\NatalChartCalculator\\"

echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Natal Chart Calculator.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\\NatalChartCalculator\\NatalChartCalculator.exe'; $Shortcut.Save()"

echo Creating Start Menu shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Natal Chart Calculator.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\\NatalChartCalculator\\NatalChartCalculator.exe'; $Shortcut.Save()"

echo.
echo ✅ Installation complete!
echo You can now run the Natal Chart Calculator from your desktop or Start Menu.
pause
'''
    
    with open('install_windows.bat', 'w') as f:
        f.write(windows_script)
    
    # Linux/Mac shell script
    unix_script = '''#!/bin/bash
echo "Installing Natal Chart Calculator..."
echo
echo "This will install the Natal Chart Calculator on your system."
echo

# Check if running as root for system-wide installation
if [ "$EUID" -eq 0 ]; then
    INSTALL_DIR="/usr/local/bin"
    echo "Installing system-wide to $INSTALL_DIR"
else
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
    echo "Installing to $INSTALL_DIR"
fi

# Copy executable
cp NatalChartCalculator "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/NatalChartCalculator"

# Create desktop entry for Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    mkdir -p "$HOME/.local/share/applications"
    cat > "$HOME/.local/share/applications/natal-chart-calculator.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Natal Chart Calculator
Comment=Professional natal chart calculator with compatibility analysis
Exec=$INSTALL_DIR/NatalChartCalculator
Icon=applications-utilities
Terminal=false
Categories=Science;Education;
EOF
    echo "Desktop entry created"
fi

echo
echo "✅ Installation complete!"
echo "Run 'NatalChartCalculator' from your terminal or find it in your applications menu."
'''
    
    with open('install_unix.sh', 'w') as f:
        f.write(unix_script)
    
    os.chmod('install_unix.sh', 0o755)
    print("✅ Created installer scripts")

def create_release_package():
    """Create a complete release package"""
    print("📦 Creating release package...")
    
    release_dir = "NatalChartCalculator_Release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    
    os.makedirs(release_dir)
    
    # Copy executable
    if os.path.exists('dist/NatalChartCalculator.exe'):
        shutil.copy('dist/NatalChartCalculator.exe', release_dir)
        executable_name = 'NatalChartCalculator.exe'
    elif os.path.exists('dist/NatalChartCalculator'):
        shutil.copy('dist/NatalChartCalculator', release_dir)
        executable_name = 'NatalChartCalculator'
    else:
        print("❌ No executable found in dist/ directory")
        return False
    
    # Copy essential files
    files_to_copy = [
        'de421.bsp',
        'README.md',
        'LICENSE',
        'install_windows.bat',
        'install_unix.sh'
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy(file, release_dir)
    
    # Create installation guide
    install_guide = '''# Natal Chart Calculator - Installation Guide

## Quick Installation

### Windows
1. Double-click `install_windows.bat`
2. Follow the prompts
3. Launch from desktop or Start Menu

### Mac/Linux
1. Open terminal and run: `./install_unix.sh`
2. Launch from terminal or applications menu

## Manual Installation
1. Run the executable directly:
   - Windows: `NatalChartCalculator.exe`
   - Mac/Linux: `./NatalChartCalculator`

## Requirements
- No additional dependencies required
- Swiss Ephemeris files included
- Offline capable

## Features
- 🪐 Complete natal chart calculations
- 💕 Compatibility analysis between charts
- 🔮 Daily astrology readings and horoscopes
- 🗄️ Chart history and database storage
- 🎨 Professional sci-fi themed interface

## Support
For issues and updates, visit: https://github.com/dylanmarriner/natal-chart-calculator
'''
    
    with open(f'{release_dir}/INSTALL.md', 'w') as f:
        f.write(install_guide)
    
    print(f"✅ Release package created in {release_dir}/")
    return True

def main():
    """Main build process"""
    print("🚀 Starting Natal Chart Calculator Installer Build")
    print("=" * 60)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    if not build_executable():
        print("❌ Build failed - aborting")
        sys.exit(1)
    
    # Create installer scripts
    create_installer_scripts()
    
    # Create release package
    if not create_release_package():
        print("❌ Package creation failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Build completed successfully!")
    print("\n📦 Release package created: NatalChartCalculator_Release/")
    print("🔨 Executable: dist/NatalChartCalculator")
    print("📝 Installation scripts: install_windows.bat, install_unix.sh")
    print("\n🚀 Ready for distribution!")

if __name__ == "__main__":
    main()
