#!/usr/bin/env python3
"""
houses.py

House system calculations for natal charts.
Supports Placidus, Whole Sign, Equal, Koch, and Campanus house systems.
"""

import swisseph as swe
from calculations import normalize_angle, deg_to_sign_deg

def get_ascendant_mc_houses(t, latitude, longitude, house_system='P'):
    """
    Calculate Ascendant, Midheaven, and houses using Swiss Ephemeris.
    
    Args:
        t: Skyfield time object
        latitude: Geographic latitude
        longitude: Geographic longitude  
        house_system: House system ('P'=Placidus, 'W'=Whole Sign, 'A'=Equal, 'K'=Koch, 'C'=Campanus)
    
    Returns:
        tuple: (ascendant, midheaven, houses dict)
    """
    # Convert Skyfield time to Julian Day for Swiss Ephemeris
    utc_dt = t.utc_datetime()
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                   utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)
    
    # Calculate house cusps and angles using Swiss Ephemeris
    house_system_bytes = house_system.encode('ascii')
    houses_long = swe.houses(jd, latitude, longitude, house_system_bytes)[0]
    ascmc = swe.houses(jd, latitude, longitude, house_system_bytes)[1]
    
    # Extract ascendant and MC
    asc_deg = normalize_angle(ascmc[0])
    mc_deg = normalize_angle(ascmc[1])
    
    ascendant = {
        "ecliptic_longitude_deg": asc_deg,
        "sign": deg_to_sign_deg(asc_deg)[0],
        "degree_in_sign": deg_to_sign_deg(asc_deg)[1]
    }
    
    midheaven = {
        "ecliptic_longitude_deg": mc_deg,
        "sign": deg_to_sign_deg(mc_deg)[0],
        "degree_in_sign": deg_to_sign_deg(mc_deg)[1]
    }
    
    # Format all house cusps - Swiss Ephemeris returns 12 values where index 0 is Ascendant
    # Houses 1-11 are at indices 1-11, house_12 wraps around or needs special handling
    houses = {}
    
    # Houses 1-11: indices 1-11
    for i in range(1, min(12, len(houses_long))):
        house_deg = normalize_angle(houses_long[i])
        houses[f"house_{i}"] = {
            "ecliptic_longitude_deg": house_deg,
            "sign": deg_to_sign_deg(house_deg)[0],
            "degree_in_sign": deg_to_sign_deg(house_deg)[1]
        }
    
    # House 12: If we have a 12th cusp, use it
    if len(houses_long) > 11:
        house_deg = normalize_angle(houses_long[11])
        houses["house_12"] = {
            "ecliptic_longitude_deg": house_deg,
            "sign": deg_to_sign_deg(house_deg)[0],
            "degree_in_sign": deg_to_sign_deg(house_deg)[1]
        }
    
    return ascendant, midheaven, houses

def calculate_whole_sign_houses(ascendant):
    """
    Calculate Whole Sign houses.
    Each house is exactly 30 degrees, starting from the Ascendant sign.
    """
    houses = {}
    asc_deg = ascendant["ecliptic_longitude_deg"]
    asc_sign_start = (int(asc_deg // 30) * 30)  # Start of Ascendant sign
    
    for i in range(1, 13):
        house_cusp = normalize_angle(asc_sign_start + (i - 1) * 30)
        sign, deg = deg_to_sign_deg(house_cusp)
        houses[f"house_{i}"] = {
            "ecliptic_longitude_deg": house_cusp,
            "sign": sign,
            "degree_in_sign": deg
        }
    
    return houses

def calculate_equal_houses(ascendant):
    """
    Calculate Equal houses.
    Each house is exactly 30 degrees, starting from the Ascendant degree.
    """
    houses = {}
    asc_deg = ascendant["ecliptic_longitude_deg"]
    
    for i in range(1, 13):
        house_cusp = normalize_angle(asc_deg + (i - 1) * 30)
        sign, deg = deg_to_sign_deg(house_cusp)
        houses[f"house_{i}"] = {
            "ecliptic_longitude_deg": house_cusp,
            "sign": sign,
            "degree_in_sign": deg
        }
    
    return houses

def get_house_system_description(house_system):
    """Get description of house system."""
    systems = {
        'P': 'Placidus (default)',
        'W': 'Whole Sign',
        'A': 'Equal (Ascendant)',
        'K': 'Koch',
        'C': 'Campanus'
    }
    return systems.get(house_system, 'Unknown')

def calculate_houses(t, latitude, longitude, house_system='P', ascendant=None):
    """
    Calculate houses using specified system.
    
    Args:
        t: Skyfield time object
        latitude: Geographic latitude
        longitude: Geographic longitude
        house_system: House system code
        ascendant: Pre-calculated ascendant (for Whole Sign/Equal)
    
    Returns:
        dict: Houses data
    """
    if house_system in ['W', 'A']:  # Whole Sign or Equal
        if ascendant is None:
            _, ascendant, _ = get_ascendant_mc_houses(t, latitude, longitude, 'P')
        
        if house_system == 'W':
            return calculate_whole_sign_houses(ascendant)
        else:  # Equal
            return calculate_equal_houses(ascendant)
    else:
        # Use Swiss Ephemeris for Placidus, Koch, Campanus
        _, _, houses = get_ascendant_mc_houses(t, latitude, longitude, house_system)
        return houses
