.

## ✨ Features

### 📊 **Comprehensive Scoring System**
- **Overall compatibility score out of 100** with detailed grading
- **Weighted categories:** Synastry Harmony (40%), Destiny Connection (30%), Spiritual Bond (30%)
- **Balanced mathematical approach** with spiritual weighting options

### 🌟 **Destiny & Fated Connections**
- **North Node connections** (life path alignment)
- **7th House synastry** (relationship destiny)
- **Part of Fortune connections** (fated luck indicators)
- **Vertex connections** (karmic meeting points)

### 🔥 **Spiritual Connection Analysis**
- **Twin Flame indicators** (intense, transformative connections)
- **Soulmate markers** (harmonious, flowing bonds)
- **Past Life connections** (Saturn, South Node, Chiron aspects)
- **Elemental harmony** (water, fire, air, earth resonance)
- **Life path alignment** (shared purpose and direction)

### 💫 **Advanced Synastry Analysis**
- **Complete aspect matrix** between two charts
- **Orb-based strength calculations**
- **Positive vs negative aspect balance**
- **Top 5 strongest aspects** with detailed breakdown

### 🌈 **Composite Chart Insights**
- **Relationship essence** through midpoint calculations
- **Composite Sun, Moon, Venus, Mars** placements
- **Relationship identity and purpose**

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/enhanced-compatibility-calculator.git
cd enhanced-compatibility-calculator

# No external dependencies required - uses Python standard library only!
```

### Basic Usage

```bash
# Generate compatibility report
python enhanced_compatibility_clean.py chart1.json chart2.json --name1 "Person A" --name2 "Person B" --output compatibility_report.md

# Use example data (shows idealized high compatibility - most couples score 40-70)
python enhanced_compatibility_clean.py example_chart_1.json example_chart_2.json --name1 "Alex" --name2 "Sam" --output example_report.md
```

### Python API

```python
from enhanced_compatibility_clean import EnhancedCompatibilityCalculator

# Load your chart data (JSON format)
chart1 = load_chart_from_json("person1_chart.json")
chart2 = load_chart_from_json("person2_chart.json")

# Create calculator instance
calculator = EnhancedCompatibilityCalculator()

# Generate comprehensive report
report = calculator.generate_compatibility_report(chart1, chart2, "Alex", "Sam")

# Save or print the report
with open("compatibility_report.md", "w") as f:
    f.write(report)
print(report)
```

## 📋 Chart Data Format

Your chart JSON files should follow this structure:

```json
{
  "birth_info": {
    "name": "Person Name",
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "location": "City, Country",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": "America/New_York"
  },
  "bodies": {
    "sun": {
      "ecliptic_longitude_deg": 75.2,
      "sign": "Gemini",
      "house": 3
    },
    "moon": {
      "ecliptic_longitude_deg": 180.5,
      "sign": "Libra", 
      "house": 7
    },
    "...": "other planets"
  },
  "houses": {
    "house_1": {
      "ecliptic_longitude_deg": 10.2,
      "sign": "Aries"
    },
    "...": "other houses"
  }
}
```

## 🎯 Understanding the Scores

### **Overall Compatibility Grades**

| Score Range | Grade | Interpretation |
|-------------|-------|----------------|
| 85-100 | A+ | Exceptional Connection - Rare and profound |
| 75-84 | A | Outstanding Connection - Highly compatible |
| 65-74 | B+ | Strong Connection - Very compatible |
| 55-64 | B | Good Connection - Compatible with growth |
| 45-54 | C+ | Moderate Connection - Some challenges |
| 35-44 | C | Fair Connection - Requires work |
| 0-34 | D | Challenging Connection - Significant obstacles |

### **Category Breakdowns**

- **Synastry Harmony (40%)**: Traditional aspect analysis between charts
- **Destiny Connection (30%)**: Fated meeting indicators and life path alignment
- **Spiritual Bond (30%)**: Twin flame, soulmate, and karmic connections

## 🔬 Methodology

### **Aspect Weights**

| Aspect | Positive Score | Negative Score |
|--------|----------------|----------------|
| Conjunction | +15 | - |
| Opposition | - | -8 |
| Trine | +12 | - |
| Square | - | -6 |
| Sextile | +10 | - |
| Quincunx | - | -3 |
| Semi-sextile | +3 | - |
| Semi-square | - | -2 |

### **Orb Tolerances**

- **Standard aspects**: 8° orb
- **Destiny connections**: 3° orb (North Node, 7th House)
- **Spiritual indicators**: 3-5° orb (Twin Flame, Soulmate)
- **Exact karma**: 0.5° orb (major bonus points)

## 📝 Requirements

- Python 3.7+
- Standard library modules: `math`, `json`, `argparse`, `pathlib`, `typing`

**No external dependencies required!** 🎉

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This calculator is for entertainment and educational purposes only. Astrological interpretations should not be used as the sole basis for important life decisions.

---

**Made with ❤️ for astrology enthusiasts and relationship explorers**
- **🛡️ Error Handling** - Comprehensive try-catch error handling across all modules
- **🧪 Professional Testing** - 19 comprehensive tests ensuring reliability
- **🎨 Modern UI** - Beautiful sci-fi themed interface using CustomTkinter

## 🚀 Quick Installation

### Option 1: Automated Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/dylanmarriner/natal-chart-calculator.git
cd natal-chart-calculator

# Run automated installer
python3 install.py
```

### Option 2: Manual Installation
```bash
# Clone the repository
git clone https://github.com/dylanmarriner/natal-chart-calculator.git
cd natal-chart-calculator

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 desktop_gui.py
```

### Option 3: Install as Python Package
```bash
# Install from source
pip install -e .

# Run from anywhere
natal-chart-gui
```

## 📋 Requirements

- **Python 3.8+** - Required for modern features and compatibility
- **Operating System** - Windows, macOS, or Linux
- **Dependencies** - Automatically installed via requirements.txt:
  - `skyfield` - Astronomical calculations
  - `swisseph` - Swiss Ephemeris integration
  - `customtkinter` - Modern GUI framework
  - `pandas` - Data handling and export
  - `pytz` - Timezone support

## 🎮 Usage

### Desktop Application
```bash
# Launch the GUI
python3 desktop_gui.py

# Or if installed as package
natal-chart-gui
```

### Command Line Interface
```bash
# Generate a natal chart
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.146 --lon 174.91

# Batch processing
python3 natal_chart_enhanced.py --batch births.csv --output-dir charts/

# Interactive mode
python3 natal_chart_enhanced.py --interactive
```

## 📚 Documentation

- **[DESKTOP_GUI.md](DESKTOP_GUI.md)** - Detailed GUI usage guide
- **[TESTING.md](TESTING.md)** - Testing framework and validation
- **[API_DOCS.md](API_DOCS.md)** - Programming interface documentation

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Run all tests
python3 test_calculations.py

# Run with pytest (if installed)
pytest test_calculations.py -v
```

**Test Coverage:**
- ✅ Core astronomical calculations
- ✅ House system calculations  
- ✅ Aspect analysis and patterns
- ✅ Database operations
- ✅ Error handling and validation
- ✅ Integration workflows

## 🏗️ Architecture

```
📁 natal-chart-calculator/
├── 🎨 desktop_gui.py          # Main GUI application
├── 🧮 calculations.py         # Core astronomical calculations
├── 🏠 houses.py               # House system calculations
├── 🔗 aspects.py              # Aspect analysis and patterns
├── 🗄️ database.py             # SQLite database management
├── 🔮 astrology_readings.py   # Daily horoscopes and readings
├── 📋 natal_chart_enhanced.py # CLI interface and batch processing
├── 🧪 test_calculations.py    # Comprehensive test suite
├── 📦 setup.py                # Python package setup
├── 🚀 install.py              # Automated installation script
└── 📚 requirements.txt        # Dependencies list
```

## 🌟 Key Features

### **Natal Chart Calculations**
- **Planetary Positions** - Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto
- **Lunar Nodes** - North Node and South Node positions
- **Chiron** - The wounded healer asteroid
- **House Systems** - Placidus, Whole Sign, Equal, Koch, Campanus
- **Aspects** - Conjunction, Opposition, Trine, Square, Sextile, Quincunx, and more
- **Aspect Patterns** - T-squares, Grand Trines, Grand Crosses, Yods, Stelliums

### **Compatibility Analysis**
- **Synastry Charts** - Compare two birth charts
- **Aspect Overlays** - Inter-chart aspects between partners
- **Compatibility Score** - Numerical compatibility assessment
- **Detailed Interpretation** - Relationship dynamics analysis

### **Astrology Readings**
- **Daily Horoscopes** - Sun sign based daily guidance
- **Transit Analysis** - Current planetary influences
- **Lunar Phases** - Moon phase interpretations
- **Personalized Readings** - Based on individual birth chart

### **Database Features**
- **Chart Storage** - Save unlimited birth charts
- **Reading History** - Track astrology readings over time
- **User Preferences** - Customizable settings and themes
- **Export Options** - JSON, CSV, and text format exports

## 🛠️ Development

### Setting Up Development Environment
```bash
# Clone repository
git clone https://github.com/dylanmarriner/natal-chart-calculator.git
cd natal-chart-calculator

# Install development dependencies
pip install -r requirements.txt

# Run tests
python3 test_calculations.py

# Run application
python3 desktop_gui.py
```

### Code Quality
- **Error Handling** - Comprehensive try-catch blocks with logging
- **Input Validation** - Type checking and range validation
- **Testing** - 19 tests with 100% core functionality coverage
- **Documentation** - Complete API documentation and user guides
- **Logging** - Detailed error tracking and debugging information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting

## 📞 Support

- **Issues** - [GitHub Issues](https://github.com/dylanmarriner/natal-chart-calculator/issues)
- **Documentation** - [Wiki](https://github.com/dylanmarriner/natal-chart-calculator/wiki)
- **Discussions** - [GitHub Discussions](https://github.com/dylanmarriner/natal-chart-calculator/discussions)

## 🙏 Acknowledgments

- **Swiss Ephemeris** - High-precision planetary ephemeris
- **Skyfield** - Python astronomy library
- **CustomTkinter** - Modern GUI framework
- **Astro.com** - Reference for astrological calculations

## 📈 Version History

- **v2.0.0** - Professional edition with database, error handling, and comprehensive testing
- **v1.5.0** - Added astrology readings and daily horoscopes
- **v1.0.0** - Initial release with natal charts and compatibility analysis

---

**🌟 Built with passion for astrology and astronomy**  
**🔮 Professional-grade calculations for accurate insights**
