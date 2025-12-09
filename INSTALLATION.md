# Installation Guide

## System Requirements

- Python 3.8 or higher
- Linux/macOS/Windows
- Internet connection (for ephemeris data)

## Quick Install

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/natal-chart-calculator.git
cd natal-chart-calculator
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Swiss Ephemeris Data

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install swe-basic-data
```

**macOS (Homebrew):**
```bash
brew install swisseph
```

**Other Systems:**
Download Swiss Ephemeris files from https://www.astro.com/ftp/swisseph/ephe/
and place them in `/usr/share/swisseph/` or `~/.swisseph/`

## Verify Installation

Test the installation with a sample chart:
```bash
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.203 --lon 174.934 --name "Test"
```

If successful, you'll see output like:
```
🌟 Natal Chart for 1998-03-03 14:10:00
   Location: -37.203°, 174.934°
   Sun: Pisces 12.3°
   Moon: Taurus 13.0°
   Ascendant: Gemini 7.4°
   Patterns detected: 7
✅ Chart saved: test_19980303_chart.json
```

## Troubleshooting

### Chiron Not Available
If you see "Could not calculate Chiron (missing asteroid ephemeris files)", install the asteroid data:

**Ubuntu/Debian:**
```bash
sudo apt install swe-basic-data
```

### Permission Errors
If you can't install system packages, use a virtual environment:
```bash
python3 -m venv natal_chart_env
source natal_chart_env/bin/activate
pip install -r requirements.txt
```

### Timezone Issues
Ensure your system timezone database is current:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install tzdata

# macOS
brew update && brew install tzdata
```

## Optional: System-wide Installation

To install as a command-line tool:
```bash
# Make the main script executable
chmod +x natal_chart_enhanced.py

# Create a symbolic link (optional)
sudo ln -s $(pwd)/natal_chart_enhanced.py /usr/local/bin/natal-chart
```

Now you can run:
```bash
natal-chart --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.203 --lon 174.934
```
