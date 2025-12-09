# 🌟 Enhanced Natal Chart Calculator

A professional-grade natal chart calculator with comprehensive astrological calculations, compatibility analysis, and daily readings. Built with Python using Swiss Ephemeris and Skyfield for astronomical accuracy.

## ✨ Features

- **🎯 Complete Natal Charts** - Full astronomical calculations with planetary positions, houses, and aspects
- **💕 Compatibility Analysis** - Synastry charts comparing two birth charts for relationship compatibility
- **🔮 Astrology Readings** - Daily horoscopes, transit analysis, and lunar phase interpretations
- **🗄️ Database Storage** - SQLite database for chart history and user preferences
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
