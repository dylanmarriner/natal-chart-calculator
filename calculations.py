#!/usr/bin/env python3
"""
calculations.py
Core astronomical calculations for natal chart positions.
Handles planetary positions, nodes, Chiron, and Arabic Parts.
"""

import pytz
from datetime import datetime
from skyfield.api import load, Topos, EarthSatellite
import swisseph as swe
import math
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set Swiss Ephemeris path to include system installation locations
try:
    swe.set_ephe_path('/usr/share/libswe/ephe:/usr/share/swisseph:/usr/local/share/swisseph/')
    logger.info("Swiss Ephemeris path configured")
except Exception as e:
    logger.warning(f"Failed to set Swiss Ephemeris path: {e}")
    # Continue with default path

ZODIAC_SIGNS = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]

def normalize_angle(deg):
    """Normalize angle to 0-360 degrees."""
    try:
        if not isinstance(deg, (int, float)):
            raise ValueError(f"Angle must be numeric, got {type(deg)}")
        return deg % 360.0
    except Exception as e:
        logger.error(f"Error normalizing angle {deg}: {e}")
        raise

def deg_to_sign_deg(lon):
    """Convert ecliptic longitude to zodiac sign and degree."""
    try:
        lon = normalize_angle(lon)
        idx = int(lon // 30)
        if idx < 0 or idx >= len(ZODIAC_SIGNS):
            raise IndexError(f"Sign index {idx} out of range for longitude {lon}")
        deg = lon % 30
        return ZODIAC_SIGNS[idx], deg
    except Exception as e:
        logger.error(f"Error converting longitude {lon} to sign/degree: {e}")
        raise

def get_planet_longitudes(ts, eph, observer, t):
    """Calculate planetary positions with retrograde detection."""
    try:
        if ts is None or eph is None or observer is None or t is None:
            raise ValueError("Missing required parameters for planetary calculations")
        
        planets = {
            "sun": eph["sun"],
            "moon": eph["moon"],
            "mercury": eph["mercury"],
            "venus": eph["venus"],
            "mars": eph["mars"],
            "jupiter": eph["jupiter barycenter"],
            "saturn": eph["saturn barycenter"],
            "uranus": eph["uranus barycenter"],
            "neptune": eph["neptune barycenter"],
            "pluto": eph["pluto barycenter"]
        }
        result = {}
        
        # Calculate positions for retrograde detection
        try:
            t_plus_day = ts.utc(t.utc_datetime().year, t.utc_datetime().month, t.utc_datetime().day + 1,
                               t.utc_datetime().hour, t.utc_datetime().minute, t.utc_datetime().second)
        except Exception as e:
            logger.warning(f"Could not calculate t_plus_day for retrograde detection: {e}")
            # Use current time as fallback
            t_plus_day = t
        
        for name, body in planets.items():
            try:
                pos = observer.at(t).observe(body).apparent()
                ecliptic = pos.ecliptic_latlon()
                lon = ecliptic[1].degrees
                
                # Check for retrograde motion (proper angular difference calculation)
                try:
                    pos_plus = observer.at(t_plus_day).observe(body).apparent()
                    ecliptic_plus = pos_plus.ecliptic_latlon()
                    lon_plus = ecliptic_plus[1].degrees
                    
                    # Calculate proper angular difference accounting for 0°/360° boundary
                    diff = lon_plus - lon
                    if diff > 180:
                        diff -= 360
                    elif diff < -180:
                        diff += 360
                        
                    is_retrograde = bool(diff < 0)
                except Exception as e:
                    logger.warning(f"Could not calculate retrograde for {name}: {e}")
                    is_retrograde = False  # Default to not retrograde if calculation fails
                
                sign, deg = deg_to_sign_deg(lon)
                result[name] = {
                    "ecliptic_longitude_deg": normalize_angle(lon),
                    "sign": sign,
                    "degree_in_sign": deg,
                    "retrograde": is_retrograde
                }
            except Exception as e:
                logger.error(f"Error calculating position for {name}: {e}")
                # Skip this planet but continue with others
                continue
        
        if not result:
            raise RuntimeError("Failed to calculate any planetary positions")
        
        logger.info(f"Successfully calculated {len(result)} planetary positions")
        return result
        
    except Exception as e:
        logger.error(f"Critical error in get_planet_longitudes: {e}")
        raise

def get_nodes_chiron(ts, eph, observer, t, include_chiron=True):
    """Calculate North Node, South Node, and Chiron positions."""
    try:
        if ts is None or eph is None or observer is None or t is None:
            raise ValueError("Missing required parameters for nodes/chiron calculations")
        
        result = {}
        
        # Convert Skyfield time to Julian Day for Swiss Ephemeris
        try:
            utc_dt = t.utc_datetime()
            jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                           utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)
        except Exception as e:
            logger.error(f"Error converting time to Julian Day: {e}")
            raise
        
        # Calculate North Node (True Node) - this should always work
        try:
            node_result = swe.calc(jd, swe.MEAN_NODE)
            north_node_lon = normalize_angle(node_result[0][0])
            sign, deg = deg_to_sign_deg(north_node_lon)
            
            result["north_node"] = {
                "ecliptic_longitude_deg": north_node_lon,
                "sign": sign,
                "degree_in_sign": deg,
                "retrograde": False  # Nodes are always retrograde in mean calculation
            }
            
            # South Node is opposite North Node
            south_node_lon = normalize_angle(north_node_lon + 180)
            sign, deg = deg_to_sign_deg(south_node_lon)
            
            result["south_node"] = {
                "ecliptic_longitude_deg": south_node_lon,
                "sign": sign,
                "degree_in_sign": deg,
                "retrograde": False
            }
            logger.info("Successfully calculated North and South Nodes")
        except Exception as e:
            logger.error(f"Could not calculate nodes: {e}")
            # Continue without nodes if calculation fails
        
        # Calculate Chiron - requires asteroid ephemeris files
        if include_chiron:
            try:
                chiron_result = swe.calc(jd, swe.CHIRON)
                chiron_lon = normalize_angle(chiron_result[0][0])
                sign, deg = deg_to_sign_deg(chiron_lon)
                
                # Check Chiron retrograde
                try:
                    jd_plus = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day + 1,
                                        utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)
                    chiron_result_plus = swe.calc(jd_plus, swe.CHIRON)
                    chiron_lon_plus = normalize_angle(chiron_result_plus[0][0])
                    
                    diff = chiron_lon_plus - chiron_lon
                    if diff > 180:
                        diff -= 360
                    elif diff < -180:
                        diff += 360
                    
                    is_retrograde = bool(diff < 0)
                except Exception as e:
                    logger.warning(f"Could not calculate Chiron retrograde: {e}")
                    is_retrograde = False
                
                result["chiron"] = {
                    "ecliptic_longitude_deg": chiron_lon,
                    "sign": sign,
                    "degree_in_sign": deg,
                    "retrograde": is_retrograde
                }
                logger.info("Successfully calculated Chiron")
                
            except Exception as e:
                logger.warning(f"⚠️ Could not calculate Chiron (missing asteroid ephemeris files): {e}")
                # Continue without Chiron if ephemeris files are missing
        
        if not result:
            raise RuntimeError("Failed to calculate any nodes or Chiron positions")
        
        return result
        
    except Exception as e:
        logger.error(f"Critical error in get_nodes_chiron: {e}")
        raise

def calculate_part_of_fortune(sun_lon, moon_lon, ascendant_lon):
    """Calculate Part of Fortune (Pars Fortunae)."""
    try:
        if not all(isinstance(lon, (int, float)) for lon in [sun_lon, moon_lon, ascendant_lon]):
            raise ValueError("All longitude values must be numeric")
        
        # Formula: Part of Fortune = Moon + Ascendant - Sun (in longitude)
        # Need to handle the circular nature of zodiac
        part_of_fortune_lon = normalize_angle(moon_lon + ascendant_lon - sun_lon)
        sign, deg = deg_to_sign_deg(part_of_fortune_lon)
        
        result = {
            "ecliptic_longitude_deg": part_of_fortune_lon,
            "sign": sign,
            "degree_in_sign": deg,
            "retrograde": False  # Part of Fortune doesn't have retrograde motion
        }
        
        logger.info("Successfully calculated Part of Fortune")
        return result
        
    except Exception as e:
        logger.error(f"Error calculating Part of Fortune: {e}")
        raise

def create_observer(eph, latitude, longitude):
    """Create observer for given location."""
    try:
        if not all(isinstance(val, (int, float)) for val in [latitude, longitude]):
            raise ValueError("Latitude and longitude must be numeric")
        
        if not -90 <= latitude <= 90:
            raise ValueError(f"Latitude {latitude} out of valid range [-90, 90]")
        
        if not -180 <= longitude <= 180:
            raise ValueError(f"Longitude {longitude} out of valid range [-180, 180]")
        
        observer = eph['earth'] + Topos(latitude_degrees=latitude, longitude_degrees=longitude)
        logger.info(f"Created observer for lat={latitude}, lon={longitude}")
        return observer
        
    except Exception as e:
        logger.error(f"Error creating observer for lat={latitude}, lon={longitude}: {e}")
        raise

def parse_birth_data(birth_date, birth_time, timezone_name):
    """Parse and validate birth data inputs."""
    try:
        # Parse date
        try:
            date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Invalid date format '{birth_date}'. Expected YYYY-MM-DD: {e}")
        
        # Parse time
        try:
            time_obj = datetime.strptime(birth_time, "%H:%M:%S")
        except ValueError as e:
            raise ValueError(f"Invalid time format '{birth_time}'. Expected HH:MM:SS: {e}")
        
        # Validate timezone
        try:
            import pytz
            if timezone_name not in pytz.all_timezones:
                raise ValueError(f"Invalid timezone '{timezone_name}'. Use pytz timezone names.")
        except ImportError:
            logger.warning("pytz not available, skipping timezone validation")
        except ValueError as e:
            raise
        
        # Combine date and time
        birth_datetime = datetime.combine(date_obj.date(), time_obj.time())
        
        logger.info(f"Parsed birth data: {birth_datetime} {timezone_name}")
        return birth_datetime, timezone_name
        
    except Exception as e:
        logger.error(f"Error parsing birth data: {e}")
        raise
