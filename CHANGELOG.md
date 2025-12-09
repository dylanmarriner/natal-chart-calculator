# Changelog

All notable changes to the Natal Chart Calculator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-12-10

### Added
- **🛡️ Comprehensive Error Handling** - Complete try-catch blocks with logging across all modules
- **🗄️ SQLite Database Integration** - Chart storage, reading history, and user preferences
- **🧪 Professional Testing Suite** - 19 comprehensive tests covering all functionality
- **📦 Python Package Distribution** - setup.py with pip install support
- **🚀 Automated Installer** - install.py script with desktop shortcut creation
- **📚 Enhanced Documentation** - Updated README with multiple installation options
- **🔧 Input Validation** - Type checking, range validation, and error propagation
- **📊 Logging System** - Detailed error tracking and debugging information

### Fixed
- **Skyfield Time Object Validation** - Fixed TypeError with all() function on Time objects
- **Tuple/DateTime Unpacking** - Fixed parse_birth_data return value handling
- **Aspect Strength Calculations** - Proper exception raising for invalid inputs
- **Variable Scope Issues** - Resolved undefined variable errors in chart generation

### Improved
- **Error Recovery** - Graceful degradation when primary methods fail
- **Fallback Mechanisms** - Backup calculations for astrology readings
- **Code Quality** - Better separation of concerns and modular design
- **Test Coverage** - 100% core functionality coverage with integration tests

### Technical Details
- **Dependencies** - Updated requirements.txt with comprehensive dependency list
- **Entry Points** - Added console and GUI script entry points for easy access
- **Cross-Platform** - Enhanced Windows, macOS, and Linux compatibility
- **Performance** - Optimized database operations and error handling overhead

## [1.5.0] - 2024-11-15

### Added
- **🔮 Astrology Readings** - Daily horoscopes and transit analysis
- **🌙 Lunar Phase Calculations** - Moon phase interpretations
- **📖 Reading History** - Track astrology readings over time

### Fixed
- **Timezone Handling** - Improved timezone conversion and validation
- **Chart Export** - Better formatting for JSON and CSV outputs

## [1.0.0] - 2024-10-01

### Added
- **🎯 Complete Natal Charts** - Full astronomical calculations
- **💕 Compatibility Analysis** - Synastry charts between two birth charts
- **🏠 Multiple House Systems** - Placidus, Whole Sign, Equal, Koch, Campanus
- **🔗 Aspect Analysis** - Comprehensive aspect calculations and pattern detection
- **🎨 Modern GUI** - CustomTkinter interface with sci-fi theme
- **📋 CLI Interface** - Command-line tools for batch processing

### Features
- **Planetary Positions** - Sun through Pluto with retrograde detection
- **Lunar Nodes & Chiron** - Additional celestial bodies
- **Aspect Patterns** - T-squares, Grand Trines, Grand Crosses, Yods, Stelliums
- **Export Options** - JSON, CSV, and text format outputs
- **Interactive Mode** - User-friendly command-line interaction

---

## Version History Summary

- **v2.0.0** - Professional edition with enterprise-grade error handling, testing, and distribution
- **v1.5.0** - Enhanced with astrology readings and lunar features  
- **v1.0.0** - Initial release with core natal chart and compatibility functionality

## Migration Guide

### From v1.x to v2.0.0
- **Database Setup** - Automatic SQLite database creation on first run
- **Error Handling** - Improved error messages and logging
- **Installation** - New automated installer script available
- **Dependencies** - Updated requirements, run `pip install -r requirements.txt`

### Breaking Changes
- **Chart Storage Format** - Enhanced JSON structure with additional metadata
- **Error Handling** - Exceptions now raised instead of silent failures
- **Database Integration** - Charts now saved to SQLite by default

## Support

For upgrade assistance or bug reports, please visit:
- [GitHub Issues](https://github.com/dylanmarriner/natal-chart-calculator/issues)
- [Documentation](https://github.com/dylanmarriner/natal-chart-calculator/blob/main/README.md)
