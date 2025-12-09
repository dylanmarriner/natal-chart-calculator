#!/usr/bin/env python3
"""
natal_chart_enhanced.py

Enhanced natal chart calculator with comprehensive astrological features.
Integrates all modules: calculations, houses, aspects, and CLI interface.

Features:
- Accurate planetary positions with retrograde detection
- North/South Nodes, Chiron, and Arabic Parts
- Multiple house systems (Placidus, Whole Sign, Equal, Koch, Campanus)
- Aspect pattern detection (T-squares, Grand Trines, Yods, Stelliums)
- CLI interface with batch processing
- Multiple output formats (JSON, CSV, text)
- PDF/SVG export capabilities
- Interactive mode for easy input
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Import our modules
from calculations import (
    get_planet_longitudes, get_nodes_chiron, calculate_part_of_fortune,
    create_observer, parse_birth_data, normalize_angle
)
from houses import get_ascendant_mc_houses, calculate_houses, get_house_system_description
from aspects import compute_aspects, detect_aspect_patterns
from cli import (parse_batch_file, generate_output_filename, save_chart_json, save_chart_csv, 
                save_chart_text, print_chart_summary)

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
    try:
        with open('.natal_chart_config.json', 'w') as f:
            json.dump(config, f, indent=2)
    except Exception:
        pass  # Silently fail if can't save config

def load_config():
    """Load last used configuration."""
    try:
        with open('.natal_chart_config.json', 'r') as f:
            return json.load(f)
    except Exception:
        return None

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

def process_single_chart(args):
    """Process a single chart from command-line arguments."""
    chart = calculate_complete_chart(
        args.date, args.time, args.tz, args.lat, args.lon,
        house_system=args.house_system,
        include_nodes=args.include_nodes,
        include_chiron=args.include_chiron,
        include_arabic_parts=args.include_arabic_parts,
        aspect_patterns=args.aspect_patterns
    )
    
    # Generate output filename
    entry = {
        'name': args.name or 'natal_chart',
        'date': args.date
    }
    filename = generate_output_filename(entry, args.format, args.output_dir)
    filepath = Path(args.output_dir) / filename
    
    # Save chart in requested format
    if args.format == 'json':
        save_chart_json(chart, filepath)
    elif args.format == 'csv':
        save_chart_csv(chart, filepath)
    elif args.format == 'text':
        save_chart_text(chart, filepath)
    
    # Print summary
    print_chart_summary(chart, args.quiet)
    print(f"✅ Chart saved: {filepath}")
    
    # Export PDF/SVG if requested
    if args.export:
        try:
            export_chart(chart, filepath, args.export)
        except Exception as e:
            print(f"⚠️  Export failed: {e}")
    
    return chart

def process_batch_charts(args):
    """Process multiple charts from a batch file."""
    entries = parse_batch_file(args.batch)
    
    if not entries:
        print("❌ No valid entries found in batch file")
        return
    
    print(f"📊 Processing {len(entries)} charts...")
    
    processed = 0
    for i, entry in enumerate(entries, 1):
        try:
            chart = calculate_complete_chart(
                entry['date'], entry['time'], entry['timezone'],
                entry['latitude'], entry['longitude'],
                house_system=args.house_system,
                include_nodes=args.include_nodes,
                include_chiron=args.include_chiron,
                include_arabic_parts=args.include_arabic_parts,
                aspect_patterns=args.aspect_patterns
            )
            
            # Generate output filename
            filename = generate_output_filename(entry, args.format, args.output_dir)
            filepath = Path(args.output_dir) / filename
            
            # Save chart
            if args.format == 'json':
                save_chart_json(chart, filepath)
            elif args.format == 'csv':
                save_chart_csv(chart, filepath)
            elif args.format == 'text':
                save_chart_text(chart, filepath)
            
            processed += 1
            
            if not args.quiet:
                print(f"  [{i}/{len(entries)}] ✅ {entry['name']}: {filepath}")
            
            # Export PDF/SVG if requested
            if args.export:
                try:
                    export_chart(chart, filepath, args.export)
                except Exception as e:
                    if not args.quiet:
                        print(f"    ⚠️  Export failed: {e}")
        
        except Exception as e:
            print(f"  [{i}/{len(entries)}] ❌ {entry.get('name', 'unknown')}: {e}")
    
    print(f"📈 Batch processing complete: {processed}/{len(entries)} charts processed")

def calculate_complete_chart(birth_date, birth_time, timezone_name, latitude, longitude, 
                           house_system='P', include_nodes=True, include_chiron=True, 
                           include_arabic_parts=True, aspect_patterns=True):
    """
    Calculate a complete natal chart with all available features.
    
    Args:
        birth_date: Birth date (YYYY-MM-DD)
        birth_time: Birth time (HH:MM:SS)
        timezone_name: Timezone name
        latitude: Geographic latitude
        longitude: Geographic longitude
        house_system: House system code
        include_nodes: Include North/South Nodes
        include_chiron: Include Chiron
        include_arabic_parts: Include Arabic Parts
        aspect_patterns: Detect aspect patterns
    
    Returns:
        dict: Complete chart data
    """
    # Load ephemeris and timescale
    from skyfield.api import load
    ts = load.timescale()
    eph = load('de421.bsp')
    
    # Parse birth data and create observer
    try:
        birth_datetime, timezone_str = parse_birth_data(birth_date, birth_time, timezone_name)
        year, month, day, hour, minute, second = birth_datetime.year, birth_datetime.month, birth_datetime.day, birth_datetime.hour, birth_datetime.minute, birth_datetime.second
        t = ts.utc(year, month, day, hour, minute, second)
        observer = create_observer(eph, latitude, longitude)
    except Exception as e:
        logger.error(f"Error parsing birth data or creating observer: {e}")
        raise
    
    # Calculate planetary positions
    planets = get_planet_longitudes(ts, eph, observer, t)
    
    # Calculate additional bodies
    all_bodies = planets.copy()
    
    if include_nodes or include_chiron:
        nodes_chiron = get_nodes_chiron(ts, eph, observer, t, include_chiron=include_chiron)
        if include_nodes:
            all_bodies.update({k: v for k, v in nodes_chiron.items() if k in ['north_node', 'south_node']})
        if include_chiron and 'chiron' in nodes_chiron:
            all_bodies['chiron'] = nodes_chiron['chiron']
    
    # Calculate angles and houses
    ascendant, midheaven, houses = get_ascendant_mc_houses(t, latitude, longitude, house_system)
    all_bodies['ascendant'] = ascendant
    all_bodies['midheaven'] = midheaven
    
    # Calculate Arabic Parts
    if include_arabic_parts:
        sun_lon = planets['sun']['ecliptic_longitude_deg']
        moon_lon = planets['moon']['ecliptic_longitude_deg']
        asc_lon = ascendant['ecliptic_longitude_deg']
        
        all_bodies['part_of_fortune'] = calculate_part_of_fortune(sun_lon, moon_lon, asc_lon)
    
    # Calculate aspects
    bodies_for_aspects = list(all_bodies.keys())
    aspects = compute_aspects(all_bodies, include_points=bodies_for_aspects)
    
    # Detect aspect patterns
    patterns = {}
    if aspect_patterns:
        patterns = detect_aspect_patterns(aspects, all_bodies)
    
    # Assemble complete chart
    chart = {
        "birth": {
            "date": birth_date,
            "time_local": birth_time,
            "timezone": timezone_name,
            "latitude": latitude,
            "longitude": longitude
        },
        "bodies": all_bodies,
        "houses": houses,
        "aspects": aspects,
        "aspect_patterns": patterns,
        "house_system": get_house_system_description(house_system),
        "house_system_code": house_system,
        "calculation_method": "Enhanced: Skyfield + Swiss Ephemeris + Pattern Detection",
        "generated_utc": birth_datetime.isoformat()
    }
    
    return chart

def process_single_chart(args):
    """Process a single chart from command-line arguments."""
    chart = calculate_complete_chart(
        args.date, args.time, args.tz, args.lat, args.lon,
        house_system=args.house_system,
        include_nodes=args.include_nodes,
        include_chiron=args.include_chiron,
        include_arabic_parts=args.include_arabic_parts,
        aspect_patterns=args.aspect_patterns
    )
    
    # Generate output filename
    entry = {
        'name': args.name or 'natal_chart',
        'date': args.date
    }
    filename = generate_output_filename(entry, args.format, args.output_dir)
    filepath = Path(args.output_dir) / filename
    
    # Save chart in requested format
    if args.format == 'json':
        save_chart_json(chart, filepath)
    elif args.format == 'csv':
        save_chart_csv(chart, filepath)
    elif args.format == 'text':
        save_chart_text(chart, filepath)
    
    # Print summary
    print_chart_summary(chart, args.quiet)
    print(f"✅ Chart saved: {filepath}")
    
    # Export PDF/SVG if requested
    if args.export:
        try:
            export_chart(chart, filepath, args.export)
        except Exception as e:
            print(f"⚠️  Export failed: {e}")
    
    return chart

def process_batch_charts(args):
    """Process multiple charts from a batch file."""
    entries = parse_batch_file(args.batch)
    
    if not entries:
        print("❌ No valid entries found in batch file")
        return
    
    print(f"📊 Processing {len(entries)} charts...")
    
    processed = 0
    for i, entry in enumerate(entries, 1):
        try:
            chart = calculate_complete_chart(
                entry['date'], entry['time'], entry['timezone'],
                entry['latitude'], entry['longitude'],
                house_system=args.house_system,
                include_nodes=args.include_nodes,
                include_chiron=args.include_chiron,
                include_arabic_parts=args.include_arabic_parts,
                aspect_patterns=args.aspect_patterns
            )
            
            # Generate output filename
            filename = generate_output_filename(entry, args.format, args.output_dir)
            filepath = Path(args.output_dir) / filename
            
            # Save chart
            if args.format == 'json':
                save_chart_json(chart, filepath)
            elif args.format == 'csv':
                save_chart_csv(chart, filepath)
            elif args.format == 'text':
                save_chart_text(chart, filepath)
            
            processed += 1
            
            if not args.quiet:
                print(f"  [{i}/{len(entries)}] ✅ {entry['name']}: {filepath}")
            
            # Export PDF/SVG if requested
            if args.export:
                try:
                    export_chart(chart, filepath, args.export)
                except Exception as e:
                    if not args.quiet:
                        print(f"    ⚠️  Export failed: {e}")
        
        except Exception as e:
            print(f"  [{i}/{len(entries)}] ❌ {entry.get('name', 'unknown')}: {e}")
    
    print(f"📈 Batch processing complete: {processed}/{len(entries)} charts processed")

def export_chart(chart, filepath, export_format):
    """Export chart as PDF or SVG (placeholder for future implementation)."""
    # This is a placeholder - PDF/SVG export would require additional libraries
    # like matplotlib, reportlab, or svgwrite
    export_path = filepath.with_suffix(f'.{export_format}')
    
    if export_format == 'pdf':
        # TODO: Implement PDF export with matplotlib
        print(f"📄 PDF export would be saved to: {export_path}")
    elif export_format == 'svg':
        # TODO: Implement SVG export with svgwrite
        print(f"🎨 SVG export would be saved to: {export_path}")
    
    # For now, just create a placeholder file
    with open(export_path, 'w') as f:
        f.write(f"# Chart Export Placeholder\n")
        f.write(f"# Chart for {chart['birth']['date']} {chart['birth']['time_local']}\n")
        f.write(f"# Export format: {export_format}\n")
        f.write(f"# TODO: Implement actual {export_format.upper()} generation\n")

def main():
    """Main entry point with interactive mode support."""
    try:
        # Create parser and parse arguments
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
        
        # Add all arguments
        parser.add_argument('--date', '-d', type=str, help='Birth date (YYYY-MM-DD)')
        parser.add_argument('--time', '-t', type=str, help='Birth time (HH:MM:SS)')
        parser.add_argument('--tz', '--timezone', type=str, help='Timezone (e.g., Pacific/Auckland)')
        parser.add_argument('--lat', '--latitude', type=float, help='Latitude (decimal degrees)')
        parser.add_argument('--lon', '--longitude', type=float, help='Longitude (decimal degrees)')
        parser.add_argument('--name', '-n', type=str, help='Person name (for output filename)')
        parser.add_argument('--batch', '-b', type=str, help='CSV file with batch birth data')
        parser.add_argument('--output-dir', '-o', type=str, default='.', help='Output directory')
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
        
        args = parser.parse_args()
        
        # Handle interactive mode
        if len(sys.argv) == 1 or (len(sys.argv) == 2 and args.interactive):
            print("🎯 Running in interactive mode...")
            
            # Try to load last config for defaults
            last_config = load_config()
            if last_config:
                print(f"📝 Using last configuration for {last_config.get('name', 'unknown')}")
            
            # Get interactive input
            config = interactive_input()
            
            # Save current config for next time
            save_config(config)
            
            # Create a mock args object for processing
            class MockArgs:
                def __init__(self, config):
                    self.name = config['name']
                    self.date = config['date']
                    self.time = config['time']
                    self.tz = config['timezone']
                    self.lat = config['latitude']
                    self.lon = config['longitude']
                    self.house_system = config['house_system']
                    self.format = config['format']
                    self.batch = None
                    self.output_dir = '.'
                    self.include_nodes = True
                    self.include_chiron = True
                    self.include_arabic_parts = True
                    self.aspect_patterns = True
                    self.export = None
                    self.quiet = False
                    self.validate = False
            
            args = MockArgs(config)
        
        # Validate arguments
        errors = validate_arguments(args)
        if errors:
            print("❌ Validation errors:")
            for error in errors:
                print(f"   - {error}")
            sys.exit(1)
        
        if args.validate:
            print("✅ Arguments validated successfully")
            return
        
        # Process charts
        if args.batch:
            process_batch_charts(args)
        else:
            process_single_chart(args)
    
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
