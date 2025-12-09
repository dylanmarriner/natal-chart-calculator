# Desktop GUI Installation Guide

## 🌟 Enhanced Natal Chart Calculator - Standalone Desktop Application

A professional desktop application with Dylan's custom sci-fi theme, featuring natal chart calculations, synastry compatibility analysis, and comprehensive astrology readings with daily horoscopes.

### ✨ Features

- **🪐 Single Natal Chart**: Complete astrological calculations with multiple house systems
- **💕 Compatibility Calculator**: Synastry analysis between two birth charts
- **🔮 Astrology Readings**: Daily horoscopes, transit analysis, and lunar phase interpretations
- **🎨 Sci-fi Theme**: Dylan's custom holographic UI with stunning visual effects
- **📊 Multiple Outputs**: Save charts and readings in JSON, CSV, or formatted text
- **⚡ Real-time Calculations**: Fast, accurate Swiss Ephemeris integration
- **🔮 Pattern Detection**: Advanced aspect pattern analysis (T-squares, Grand Trines, etc.)
- **🌌 Transit Analysis**: Personalized daily insights based on current planetary positions
- **🌙 Lunar Guidance**: Current moon phase interpretations and timing advice

### 📋 System Requirements

- **Python 3.8+** (recommended 3.10+)
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum
- **Storage**: 100MB free space
- **Swiss Ephemeris**: Required for Chiron calculations (see installation)

### 🔧 Installation

#### Step 1: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk
sudo apt install swe-basic-data  # For Chiron calculations
```

**macOS:**
```bash
# Install Python 3.8+ if not already installed
brew install python-tk
brew install swisseph  # For Chiron calculations
```

**Windows:**
```bash
# Install Python 3.8+ from python.org (ensure tkinter is included)
# Download Swiss Ephemeris from https://www.astro.com/ftp/swisseph/ephe/
# Extract to C:\swisseph\ or add to PATH
```

#### Step 2: Create Virtual Environment

```bash
# Navigate to the project directory
cd natal-chart-calculator

# Create virtual environment
python3 -m venv gui_env

# Activate virtual environment
# Linux/macOS:
source gui_env/bin/activate
# Windows:
gui_env\Scripts\activate
```

#### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Launch the Desktop GUI

```bash
python desktop_gui.py
```

### 🚀 Quick Start

1. **Launch the application**: `python desktop_gui.py`
2. **Natal Chart Tab**: Enter birth information and click "🌟 Calculate Natal Chart"
3. **Compatibility Tab**: Enter two people's birth information and click "💕 Calculate Compatibility"
4. **Save Results**: Use the export buttons to save charts in your preferred format

### 📱 Using the Desktop GUI

#### Single Natal Chart

1. **Personal Information**: Enter name, birth date, time, and location
2. **House System**: Choose from Placidus, Whole Sign, Equal, Koch, or Campanus
3. **Calculate**: Click "🌟 Calculate Natal Chart" for instant results
4. **Export**: Save as JSON (complete data), CSV (planetary positions), or text report

#### Compatibility Calculator

1. **Person 1**: Enter first person's complete birth information
2. **Person 2**: Enter second person's complete birth information  
3. **Calculate**: Click "💕 Calculate Compatibility" for synastry analysis
4. **Results**: View compatibility score, key aspects, and relationship themes

#### Astrology Readings & Daily Horoscopes

1. **Birth Information**: Enter your complete birth data for personalized readings
2. **Target Date**: Select the date for your reading (defaults to today)
3. **Reading Type**: Choose from:
   - **Comprehensive**: Daily horoscope + transit analysis + lunar guidance
   - **Transits Only**: Focus on current planetary influences and aspects
   - **Horoscope Only**: Sun sign-based daily guidance and themes
4. **Generate**: Click "🔮 Generate Astrology Reading" for personalized insights
5. **Results**: View detailed analysis including:
   - Sun sign information and energy levels
   - Current lunar phase and timing advice
   - Major transits and their influences
   - Daily themes and guidance
   - Lucky areas and challenges to watch

### 🎨 Theme Customization

The desktop app features Dylan's custom sci-fi theme with:

- **Color Palette**: Cyan, Violet, Red, Amber, Green, Rose accents
- **Holographic Effects**: Glass morphism, subtle glows, and gradients
- **Typography**: Monospace fonts for technical precision
- **Layout**: Clean, organized interface with intuitive navigation

### 🔧 Troubleshooting

#### Common Issues

**"No module named 'customtkinter'"**
```bash
# Ensure virtual environment is activated
source gui_env/bin/activate  # Linux/macOS
# or
gui_env\Scripts\activate     # Windows

# Install CustomTkinter
pip install customtkinter
```

**"Could not calculate Chiron"**
```bash
# Install Swiss Ephemeris data
sudo apt install swe-basic-data  # Ubuntu/Debian
brew install swisseph            # macOS
# Or download from https://www.astro.com/ftp/swisseph/ephe/
```

**GUI doesn't start / Tkinter errors**
```bash
# Install tkinter support
sudo apt install python3-tk      # Ubuntu/Debian
brew install python-tk           # macOS
# Reinstall Python on Windows with tkinter included
```

**Permission errors**
```bash
# Use virtual environment instead of system-wide installation
python3 -m venv gui_env
source gui_env/bin/activate
pip install -r requirements.txt
```

#### Performance Tips

- **Close other applications** for faster calculations
- **Use SSD storage** for better file I/O performance
- **Ensure adequate RAM** (4GB+ recommended)
- **Update Python** to latest version for best performance

### 📊 Output Formats

#### JSON Format
Complete chart data including:
- Planetary positions with retrograde status
- House cusps and angles
- Complete aspect list with orbs and strengths
- Aspect patterns and configurations
- Birth data and calculation parameters

#### CSV Format
Tabular planetary data:
- Planet name, sign, degree, longitude
- Retrograde status
- Suitable for spreadsheet analysis

#### Text Format
Human-readable report:
- Formatted planetary positions
- House placements
- Key aspects and patterns
- Easy to read and share

### 🌐 Network Requirements

- **Optional**: Internet connection for initial dependency installation
- **Offline Use**: Once installed, the application works completely offline
- **No Data Collection**: All calculations are performed locally

### 📝 License

MIT License - See LICENSE file for details.

### 🤝 Contributing

Contributions welcome! Please ensure:
- Code follows the existing style guide
- Desktop GUI features are tested
- Theme consistency is maintained
- Documentation is updated

### 📞 Support

For issues and support:
1. Check this installation guide
2. Review the troubleshooting section
3. Check the GitHub repository issues
4. Ensure all system dependencies are installed

---

**Enjoy your professional natal chart calculations with Dylan's sci-fi themed desktop application! 🌟**
