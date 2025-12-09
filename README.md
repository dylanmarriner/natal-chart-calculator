# 🌟 Enhanced Natal Chart Calculator

A professional natal chart calculator with **both command-line and desktop GUI interfaces**, featuring advanced astrological calculations, multiple house systems, and synastry compatibility analysis.

## ✨ Features

- **🖥️ Desktop GUI**: Standalone application with Dylan's custom sci-fi theme
- **💕 Compatibility Calculator**: Synastry analysis between two birth charts
- **🔮 Astrology Readings**: Daily horoscopes, transit analysis, and lunar phase interpretations
- **🪐 Complete Planetary Calculations**: Sun, Moon, planets, North/South Nodes, Chiron, Part of Fortune
- **🏠 Multiple House Systems**: Placidus, Whole Sign, Equal, Koch, Campanus
- **🔮 Advanced Pattern Detection**: T-squares, Grand Trines, Yods, Stelliums
- **⚡ Interactive Mode**: User-friendly CLI prompts
- **📊 Multiple Output Formats**: JSON, CSV, formatted text
- **🎯 Batch Processing**: Handle multiple charts from CSV files
- **🎨 Sci-fi Theme**: Stunning holographic UI in desktop version
- **🌌 Transit Analysis**: Personalized daily insights based on current planetary positions
- **🌙 Lunar Guidance**: Current moon phase interpretations and timing advice

## 🚀 Quick Start

### Desktop GUI (Recommended)
```bash
# Clone and run the launcher
git clone https://github.com/dylanmarriner/natal-chart-calculator.git
cd natal-chart-calculator
./run_gui.sh          # Linux/macOS
# or
run_gui.bat           # Windows
```

### Command Line
```bash
# Interactive mode
python3 natal_chart_enhanced.py --interactive

# Direct calculation
python3 natal_chart_enhanced.py \
  --date 1998-03-03 \
  --time 14:10:00 \
  --tz Pacific/Auckland \
  --lat -37.146 \
  --lon 174.91
```

## 📱 Interface Options

### 🖥️ Desktop GUI
- **Modern Interface**: CustomTkinter with Dylan's sci-fi theme
- **Tabbed Navigation**: Single charts and compatibility analysis
- **Real-time Calculations**: Instant results with visual feedback
- **Export Options**: Save charts as JSON, CSV, or text
- **Cross-platform**: Windows, macOS, Linux support

**📖 [Desktop GUI Installation Guide →](DESKTOP_GUI.md)**

### 💻 Command Line
- **Interactive Mode**: Guided input with validation
- **Batch Processing**: Handle multiple charts efficiently
- **Automation Friendly**: Perfect for scripting and workflows
- **Lightweight**: No GUI dependencies required

## Installation

### Dependencies
```bash
pip install skyfield pytz swisseph customtkinter pandas
```

### ⚠️ Important: Swiss Ephemeris Setup

**Chiron calculations require Swiss Ephemeris files:**

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install swe-basic-data

# macOS (Homebrew)  
brew install swisseph

# Other systems: Download from https://www.astro.com/ftp/swisseph/ephe/
```

Without these files, you'll see:
```
⚠️ Could not calculate Chiron (missing asteroid ephemeris files)
```

**All other features work without this dependency.**

### Batch Processing
Create a CSV file with birth data:

```csv
name,date,time,timezone,latitude,longitude
John Doe,1998-03-03,14:10:00,Pacific/Auckland,-37.146,174.91
Jane Smith,1990-07-15,09:30:00,America/New_York,40.7128,-74.0060
```

Process the batch:
```bash
python3 natal_chart_enhanced.py --batch births.csv --output-dir charts/
```

### Output Formats
```bash
# JSON (default)
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.146 --lon 174.91 --format json

# CSV (planetary positions only)
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.146 --lon 174.91 --format csv

# Formatted text report
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.146 --lon 174.91 --format text
```

### Command Line Options
```
--date, -d           Birth date (YYYY-MM-DD)
--time, -t           Birth time (HH:MM:SS)
--tz, --timezone     Timezone name (e.g., Pacific/Auckland)
--lat, --latitude    Latitude in decimal degrees
--lon, --longitude   Longitude in decimal degrees
--name, -n           Person name (for output filename)
--batch, -b          CSV file for batch processing
--output-dir, -o     Output directory (default: current)
--house-system, -hs  House system: P=Placidus, W=Whole Sign, A=Equal, K=Koch, C=Campanus
--format, -f         Output format: json, csv, text
--export             Export as PDF or SVG (placeholder)
--quiet, -q          Suppress verbose output
--validate           Validate input and exit
```

## Output Structure

### JSON Format
```json
{
  "birth": {
    "date": "1998-03-03",
    "time_local": "14:10:00", 
    "timezone": "Pacific/Auckland",
    "latitude": -37.146,
    "longitude": 174.91
  },
  "bodies": {
    "sun": {
      "ecliptic_longitude_deg": 342.28,
      "sign": "Pisces",
      "degree_in_sign": 12.28,
      "retrograde": false
    },
    "moon": { ... },
    "north_node": { ... },
    "south_node": { ... },
    "part_of_fortune": { ... },
    "ascendant": { ... },
    "midheaven": { ... }
  },
  "houses": {
    "house_1": { "sign": "Cancer", "degree_in_sign": 9.62 },
    "house_2": { "sign": "Leo", "degree_in_sign": 16.41 },
    ...
  },
  "aspects": [
    {
      "between": ["sun", "moon"],
      "aspect": "sextile", 
      "angle": 60.75,
      "orb": 0.75,
      "strength": 0.875
    }
  ],
  "aspect_patterns": {
    "t_squares": [...],
    "grand_trines": [...],
    "grand_crosses": [...],
    "yods": [...],
    "stelliums": [...]
  },
  "house_system": "Placidus (default)",
  "calculation_method": "Enhanced: Skyfield + Swiss Ephemeris + Pattern Detection"
}
```

## Architecture

The calculator is organized into modular components:

- **`calculations.py`**: Core astronomical calculations, planetary positions, nodes, Chiron
- **`houses.py`**: House system calculations for all supported systems  
- **`aspects.py`**: Aspect calculations and pattern detection algorithms
- **`cli.py`**: Command-line interface and batch processing
- **`natal_chart_enhanced.py`**: Main orchestrator integrating all modules

## Accuracy

- **Planetary Positions**: Uses NASA JPL DE421 ephemeris via Skyfield
- **House Calculations**: Swiss Ephemeris for professional accuracy
- **Time Zones**: Full timezone support via pytz
- **Retrograde Calculation**: Proper angular difference method

## House Systems

| System | Code | Description |
|--------|------|-------------|
| Placidus | P | Default system, most widely used |
| Whole Sign | W | Each house = 30°, starting from Ascendant sign |
| Equal | A | Each house = 30°, starting from Ascendant degree |
| Koch | K | Time-based system, popular in German-speaking countries |
| Campanus | C | Space-based system, divided by great circles |

## Aspect Patterns Detected

- **T-square**: Two squares with an opposition (focal tension)
- **Grand Trine**: Three planets in trine (harmony flow)  
- **Grand Cross**: Four planets in square with two oppositions (major challenge)
- **Yod**: Two quincunxes with a sextile base (special purpose)
- **Stellium**: Three+ planets in conjunction (focus area)

## Troubleshooting

### Chiron Not Calculated
```
⚠️ Could not calculate Chiron (missing asteroid ephemeris files)
```
Download asteroid ephemeris files as described in installation.

### Invalid Timezone
Ensure timezone names are valid IANA timezone identifiers (e.g., "America/New_York", "Europe/London").

### Coordinate Range
- Latitude: -90 to +90 degrees
- Longitude: -180 to +180 degrees

## Examples

### Quick Chart
```bash
python3 natal_chart_enhanced.py --date 1990-07-15 --time 09:30:00 --tz America/New_York --lat 40.7128 --lon -74.0060
```

### Batch with Custom Output
```bash
python3 natal_chart_enhanced.py --batch clients.csv --output-dir reports/ --format text --house-system W
```

### Validate Input
```bash
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.146 --lon 174.91 --validate
```

## Development

### Adding New Features
The modular architecture makes it easy to add:
- New house systems in `houses.py`
- Additional Arabic Parts in `calculations.py`  
- New aspect patterns in `aspects.py`
- Export formats in main orchestrator

### Testing
Test against known chart data to validate accuracy:
```bash
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.146 --lon 174.91 --name validation_test
```

## License

This project uses open-source astronomical libraries and follows their respective licenses.
