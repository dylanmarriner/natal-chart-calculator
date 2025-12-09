#!/usr/bin/env python3
"""
cli.py

Command-line interface for natal chart calculations.
Supports batch processing, multiple output formats, and configuration options.
"""

import argparse
import json
import csv
import sys
from datetime import datetime
from pathlib import Path

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate natal charts with comprehensive astrological calculations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.146 --lon 174.91
  %(prog)s --batch births.csv --output-dir charts/
  %(prog)s --date 1998-03-03 --time 14:10:00 --tz Pacific/Auckland --lat -37.146 --lon 174.91 --house-system W --export pdf
        """
    )
    
    # Single chart options
    parser.add_argument('--date', '-d', type=str, help='Birth date (YYYY-MM-DD)')
    parser.add_argument('--time', '-t', type=str, help='Birth time (HH:MM:SS)')
    parser.add_argument('--tz', '--timezone', type=str, help='Timezone (e.g., Pacific/Auckland)')
    parser.add_argument('--lat', '--latitude', type=float, help='Latitude (decimal degrees)')
    parser.add_argument('--lon', '--longitude', type=float, help='Longitude (decimal degrees)')
    parser.add_argument('--name', '-n', type=str, help='Person name (for output filename)')
    
    # Batch processing
    parser.add_argument('--batch', '-b', type=str, help='CSV file with batch birth data')
    parser.add_argument('--output-dir', '-o', type=str, default='.', help='Output directory')
    
    # Calculation options
    parser.add_argument('--house-system', '-hs', type=str, default='P',
                       choices=['P', 'W', 'A', 'K', 'C'],
                       help='House system: P=Placidus, W=Whole Sign, A=Equal, K=Koch, C=Campanus')
    parser.add_argument('--include-nodes', action='store_true', default=True,
                       help='Include North/South Nodes (default)')
    parser.add_argument('--include-chiron', action='store_true', default=True,
                       help='Include Chiron (default)')
    parser.add_argument('--include-arabic-parts', action='store_true', default=True,
                       help='Include Arabic Parts (default)')
    parser.add_argument('--aspect-patterns', action='store_true', default=True,
                       help='Detect aspect patterns (default)')
    
    # Output options
    parser.add_argument('--format', '-f', type=str, default='json',
                       choices=['json', 'csv', 'text'],
                       help='Output format')
    parser.add_argument('--export', type=str, choices=['pdf', 'svg'],
                       help='Export chart wheel as PDF or SVG')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress verbose output')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run in interactive mode (prompts for input)')
    parser.add_argument('--validate', action='store_true',
                       help='Validate input data and exit')
    
    return parser.parse_args()

def validate_arguments(args):
    """Validate command-line arguments."""
    errors = []
    
    # Check for either single chart or batch
    if not args.batch and not (args.date and args.time and args.tz and args.lat is not None and args.lon is not None):
        errors.append("Either batch file OR all single chart parameters required")
    
    if args.batch and any([args.date, args.time, args.tz, args.lat is not None, args.lon is not None]):
        errors.append("Cannot specify both batch file and single chart parameters")
    
    # Validate date format
    if args.date:
        try:
            datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            errors.append("Date must be in YYYY-MM-DD format")
    
    # Validate time format
    if args.time:
        try:
            datetime.strptime(args.time, '%H:%M:%S')
        except ValueError:
            errors.append("Time must be in HH:MM:SS format")
    
    # Validate coordinates
    if args.lat is not None and not (-90 <= args.lat <= 90):
        errors.append("Latitude must be between -90 and 90 degrees")
    
    if args.lon is not None and not (-180 <= args.lon <= 180):
        errors.append("Longitude must be between -180 and 180 degrees")
    
    # Validate batch file
    if args.batch:
        batch_path = Path(args.batch)
        if not batch_path.exists():
            errors.append(f"Batch file not found: {args.batch}")
        elif batch_path.suffix != '.csv':
            errors.append("Batch file must be CSV format")
    
    # Validate output directory
    output_path = Path(args.output_dir)
    if not output_path.exists():
        try:
            output_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Cannot create output directory: {e}")
    
    return errors

def parse_batch_file(batch_file):
    """Parse CSV batch file and return list of birth data entries."""
    entries = []
    
    try:
        with open(batch_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required_fields = ['date', 'time', 'timezone', 'latitude', 'longitude']
            
            for row_num, row in enumerate(reader, start=2):
                # Check required fields
                missing = [field for field in required_fields if not row.get(field)]
                if missing:
                    print(f"Warning: Row {row_num} missing fields: {missing}", file=sys.stderr)
                    continue
                
                try:
                    entry = {
                        'name': row.get('name', f'person_{row_num-1}'),
                        'date': row['date'],
                        'time': row['time'],
                        'timezone': row['timezone'],
                        'latitude': float(row['latitude']),
                        'longitude': float(row['longitude'])
                    }
                    entries.append(entry)
                except (ValueError, TypeError) as e:
                    print(f"Warning: Row {row_num} invalid data: {e}", file=sys.stderr)
                    continue
    
    except Exception as e:
        print(f"Error reading batch file: {e}", file=sys.stderr)
        return []
    
    return entries

def generate_output_filename(entry, format_type, output_dir):
    """Generate output filename based on entry data and format."""
    name = entry.get('name', 'natal_chart').replace(' ', '_').lower()
    date = entry.get('date', 'unknown').replace('-', '')
    
    if format_type == 'json':
        return f"{name}_{date}_chart.json"
    elif format_type == 'csv':
        return f"{name}_{date}_chart.csv"
    elif format_type == 'text':
        return f"{name}_{date}_chart.txt"
    elif format_type in ['pdf', 'svg']:
        return f"{name}_{date}_chart.{format_type}"
    else:
        return f"{name}_{date}_chart"

def save_chart_json(chart_data, filepath):
    """Save chart data as JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(chart_data, f, indent=2, ensure_ascii=False)

def save_chart_csv(chart_data, filepath):
    """Save chart data as CSV (planetary positions only)."""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Body', 'Longitude', 'Sign', 'Degree', 'Retrograde'])
        
        for body, data in chart_data['bodies'].items():
            writer.writerow([
                body,
                f"{data['ecliptic_longitude_deg']:.6f}",
                data['sign'],
                f"{data['degree_in_sign']:.6f}",
                data.get('retrograde', False)
            ])

def save_chart_text(chart_data, filepath):
    """Save chart data as formatted text."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("NATAL CHART REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        # Birth data
        birth = chart_data['birth']
        f.write("BIRTH DATA:\n")
        f.write(f"  Date: {birth['date']}\n")
        f.write(f"  Time: {birth['time_local']} ({birth['timezone']})\n")
        f.write(f"  Location: {birth['latitude']:.3f}°, {birth['longitude']:.3f}°\n\n")
        
        # Planetary positions
        f.write("PLANETARY POSITIONS:\n")
        f.write("-" * 30 + "\n")
        
        for body, data in chart_data['bodies'].items():
            retro = " R" if data.get('retrograde', False) else ""
            f.write(f"{body:12s}: {data['sign']:11s} {data['degree_in_sign']:6.2f}°{retro}\n")
        
        # Houses
        if 'houses' in chart_data:
            f.write(f"\nHOUSES ({chart_data.get('house_system', 'Placidus')}):\n")
            f.write("-" * 30 + "\n")
            
            for i in range(1, 13):
                house_key = f"house_{i}"
                if house_key in chart_data['houses']:
                    house = chart_data['houses'][house_key]
                    f.write(f"House {i:2d}: {house['sign']:11s} {house['degree_in_sign']:6.2f}°\n")
        
        # Major aspects
        if 'aspects' in chart_data:
            f.write(f"\nMAJOR ASPECTS:\n")
            f.write("-" * 30 + "\n")
            
            major_aspects = [a for a in chart_data['aspects'] 
                           if a['aspect'] in ['conjunction', 'opposition', 'trine', 'square']]
            
            for aspect in sorted(major_aspects, key=lambda x: x['orb'])[:10]:  # Top 10 tightest
                f.write(f"{aspect['between'][0]:10s} - {aspect['between'][1]:10s}: "
                       f"{aspect['aspect']:12s} ({aspect['orb']:.1f}°)\n")
        
        # Aspect patterns
        if 'aspect_patterns' in chart_data:
            patterns = chart_data['aspect_patterns']
            f.write(f"\nASPECT PATTERNS:\n")
            f.write("-" * 30 + "\n")
            
            for pattern_type, pattern_list in patterns.items():
                if pattern_list:
                    f.write(f"{pattern_type.replace('_', ' ').title()}: {len(pattern_list)}\n")

def print_chart_summary(chart_data, quiet=False):
    """Print a brief summary of the chart to console."""
    if quiet:
        return
    
    birth = chart_data['birth']
    print(f"\n🌟 Natal Chart for {birth['date']} {birth['time_local']}")
    print(f"   Location: {birth['latitude']:.3f}°, {birth['longitude']:.3f}°")
    
    # Key positions
    bodies = chart_data['bodies']
    if 'sun' in bodies:
        print(f"   Sun: {bodies['sun']['sign']} {bodies['sun']['degree_in_sign']:.1f}°")
    if 'moon' in bodies:
        print(f"   Moon: {bodies['moon']['sign']} {bodies['moon']['degree_in_sign']:.1f}°")
    if 'ascendant' in bodies:
        print(f"   Ascendant: {bodies['ascendant']['sign']} {bodies['ascendant']['degree_in_sign']:.1f}°")
    
    # Aspect patterns
    if 'aspect_patterns' in chart_data:
        patterns = chart_data['aspect_patterns']
        pattern_count = sum(len(p) for p in patterns.values())
        if pattern_count > 0:
            print(f"   Patterns detected: {pattern_count}")

def create_sample_batch_file(filename):
    """Create a sample CSV batch file."""
    sample_data = [
        ['name', 'date', 'time', 'timezone', 'latitude', 'longitude'],
        ['Sample Person', '1998-03-03', '14:10:00', 'Pacific/Auckland', '-37.146', '174.91'],
        ['Another Person', '1990-07-15', '09:30:00', 'America/New_York', '40.7128', '-74.0060']
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)
    
    print(f"Sample batch file created: {filename}")

def interactive_input():
    """Get birth data through interactive prompts."""
    print("\n🌟 Interactive Natal Chart Calculator")
    print("=" * 40)
    
    # Get person's name
    name = input("Enter person's name (or press Enter for 'natal_chart'): ").strip()
    if not name:
        name = "natal_chart"
    
    # Get birth date
    while True:
        date_str = input("Enter birth date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD (e.g., 1998-03-03)")
    
    # Get birth time
    while True:
        time_str = input("Enter birth time (HH:MM:SS): ").strip()
        try:
            datetime.strptime(time_str, '%H:%M:%S')
            break
        except ValueError:
            print("❌ Invalid time format. Please use HH:MM:SS (e.g., 14:10:00)")
    
    # Get timezone
    print("\nCommon timezones:")
    print("  Pacific/Auckland, America/New_York, Europe/London")
    print("  America/Los_Angeles, Asia/Tokyo, Australia/Sydney")
    timezone = input("Enter timezone (e.g., Pacific/Auckland): ").strip()
    if not timezone:
        timezone = "UTC"
    
    # Get location
    print("\nLocation coordinates:")
    while True:
        try:
            lat_str = input("Enter latitude (-90 to 90, e.g., -37.146): ").strip()
            latitude = float(lat_str)
            if -90 <= latitude <= 90:
                break
            else:
                print("❌ Latitude must be between -90 and 90 degrees")
        except ValueError:
            print("❌ Invalid latitude. Please enter a number (e.g., -37.146)")
    
    while True:
        try:
            lon_str = input("Enter longitude (-180 to 180, e.g., 174.91): ").strip()
            longitude = float(lon_str)
            if -180 <= longitude <= 180:
                break
            else:
                print("❌ Longitude must be between -180 and 180 degrees")
        except ValueError:
            print("❌ Invalid longitude. Please enter a number (e.g., 174.91)")
    
    # House system
    print("\nHouse systems:")
    print("  P = Placidus (default)")
    print("  W = Whole Sign")
    print("  A = Equal")
    print("  K = Koch")
    print("  C = Campanus")
    house_system = input("Enter house system (P/W/A/K/C, default P): ").strip().upper()
    if not house_system or house_system not in ['P', 'W', 'A', 'K', 'C']:
        house_system = 'P'
    
    # Output format
    print("\nOutput formats:")
    print("  json = JSON file (default)")
    print("  csv  = CSV file (planetary positions)")
    print("  text = Formatted text report")
    output_format = input("Enter output format (json/csv/text, default json): ").strip().lower()
    if not output_format or output_format not in ['json', 'csv', 'text']:
        output_format = 'json'
    
    return {
        'name': name,
        'date': date_str,
        'time': time_str,
        'timezone': timezone,
        'latitude': latitude,
        'longitude': longitude,
        'house_system': house_system,
        'format': output_format
    }

def save_config(config):
    """Save last used configuration for next time."""
    import json
    try:
        with open('.natal_chart_config.json', 'w') as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass  # Silently fail if can't save config

def load_config():
    """Load last used configuration."""
    import json
    try:
        with open('.natal_chart_config.json', 'r') as f:
            return json.load(f)
    except Exception:
        return None

# CLI utility functions - main entry point is in natal_chart_enhanced.py
