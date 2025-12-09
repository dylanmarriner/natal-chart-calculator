# Usage Examples

## Interactive Mode (Easiest)
```bash
python3 natal_chart_enhanced.py
```
Follow the prompts to enter birth data interactively.

## Single Chart - Command Line
```bash
# Basic chart
python3 natal_chart_enhanced.py \
  --date 1998-03-03 \
  --time 14:10:00 \
  --tz Pacific/Auckland \
  --lat -37.203 \
  --lon 174.934 \
  --name "Dylan"

# With Whole Sign houses and text output
python3 natal_chart_enhanced.py \
  --date 1998-03-03 \
  --time 14:10:00 \
  --tz Pacific/Auckland \
  --lat -37.203 \
  --lon 174.934 \
  --name "Dylan" \
  --house-system W \
  --format text
```

## Batch Processing
```bash
# Process multiple charts from CSV file
python3 natal_chart_enhanced.py \
  --batch examples/sample_births.csv \
  --output-dir charts/ \
  --format json

# Batch with Whole Sign houses
python3 natal_chart_enhanced.py \
  --batch examples/sample_births.csv \
  --output-dir charts/ \
  --house-system W \
  --format text
```

## Different House Systems
```bash
# Placidus (default)
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.203 --lon 174.934 --house-system P

# Whole Sign
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.203 --lon 174.934 --house-system W

# Equal houses
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.203 --lon 174.934 --house-system A

# Koch houses
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.203 --lon 174.934 --house-system K

# Campanus houses
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.203 --lon 174.934 --house-system C
```

## Output Formats
```bash
# JSON (default) - Complete chart data
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.203 --lon 174.934 --format json

# CSV - Planetary positions only
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.203 --lon 174.934 --format csv

# Text - Formatted report
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.203 --lon 174.934 --format text
```

## Validation
```bash
# Validate input data without generating chart
python3 natal_chart_enhanced.py --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.203 --lon 174.934 --validate
```

## Help
```bash
# Show all available options
python3 natal_chart_enhanced.py --help
```
