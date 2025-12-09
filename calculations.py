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

# Set Swiss Ephemeris path to include system installation locations
swe.set_ephe_path('/usr/share/libswe/ephe:/usr/share/swisseph:/usr/local/share/swisseph/')

ZODIAC_SIGNS = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]

def normalize_angle(deg):
    """Normalize angle to 0-360 degrees."""
    return deg % 360.0

def deg_to_sign_deg(lon):
    """Convert ecliptic longitude to zodiac sign and degree."""
    lon = normalize_angle(lon)
    idx = int(lon // 30)
    deg = lon % 30
    return ZODIAC_SIGNS[idx], deg

def get_planet_longitudes(ts, eph, observer, t):
    """Calculate planetary positions with retrograde detection."""
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
    t_plus_day = ts.utc(t.utc_datetime().year, t.utc_datetime().month, t.utc_datetime().day + 1,
                       t.utc_datetime().hour, t.utc_datetime().minute, t.utc_datetime().second)
    
    for name, body in planets.items():
        pos = observer.at(t).observe(body).apparent()
        ecliptic = pos.ecliptic_latlon()
        lon = ecliptic[1].degrees
        
        # Check for retrograde motion (proper angular difference calculation)
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
        
        sign, deg = deg_to_sign_deg(lon)
        result[name] = {
            "ecliptic_longitude_deg": normalize_angle(lon),
            "sign": sign,
            "degree_in_sign": deg,
            "retrograde": is_retrograde
        }
    return result

def get_nodes_chiron(ts, eph, observer, t, include_chiron=True):
    """Calculate North Node, South Node, and Chiron positions."""
    result = {}
    
    # Convert Skyfield time to Julian Day for Swiss Ephemeris
    utc_dt = t.utc_datetime()
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                   utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)
    
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
    except Exception as e:
        print(f"⚠️  Could not calculate nodes: {e}")
    
    # Calculate Chiron - requires asteroid ephemeris files
    if include_chiron:
        try:
            chiron_result = swe.calc(jd, swe.CHIRON)
            chiron_lon = normalize_angle(chiron_result[0][0])
            sign, deg = deg_to_sign_deg(chiron_lon)
            
            # Check Chiron retrograde
            jd_plus = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day + 1,
                                utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)
            chiron_result_plus = swe.calc(jd_plus, swe.CHIRON)
            chiron_lon_plus = normalize_angle(chiron_result_plus[0][0])
            
            diff = chiron_lon_plus - chiron_lon
            if diff > 180:
                diff -= 360
            elif diff < -180:
                diff += 360
            
            result["chiron"] = {
                "ecliptic_longitude_deg": chiron_lon,
                "sign": sign,
                "degree_in_sign": deg,
                "retrograde": bool(diff < 0)
            }
        except Exception as e:
            print(f"⚠️  Could not calculate Chiron (missing asteroid ephemeris files): {e}")
    
    return result

def calculate_part_of_fortune(sun_lon, moon_lon, ascendant_lon):
    """Calculate Part of Fortune (Pars Fortunae)."""
    # Formula: Part of Fortune = Moon + Ascendant - Sun (in longitude)
    # Need to handle the circular nature of zodiac
    part_of_fortune_lon = normalize_angle(moon_lon + ascendant_lon - sun_lon)
    sign, deg = deg_to_sign_deg(part_of_fortune_lon)
    
    return {
        "ecliptic_longitude_deg": part_of_fortune_lon,
        "sign": sign,
        "degree_in_sign": deg,
        "retrograde": False
    }

def create_observer(eph, latitude, longitude):
    """Create observer object for given coordinates."""
    earth = eph['earth']
    return earth + Topos(latitude_degrees=latitude, longitude_degrees=longitude)

def parse_birth_data(birth_date, birth_time, timezone_name):
    """Parse and convert birth data to UTC datetime."""
    tz = pytz.timezone(timezone_name)
    birth_local = tz.localize(datetime.fromisoformat(birth_date + "T" + birth_time))
    birth_utc = birth_local.astimezone(pytz.UTC)
    return birth_utc
