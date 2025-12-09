#!/usr/bin/env python3
"""
houses.py

House system calculations for natal charts.
Supports Placidus, Whole Sign, Equal, Koch, and Campanus house systems.
"""

import swisseph as swe
import logging
from calculations import normalize_angle, deg_to_sign_deg

# Configure logging
logger = logging.getLogger(__name__)

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
    try:
        # Validate inputs
        if t is None or latitude is None or longitude is None:
            raise ValueError("Missing required parameters for house calculations")
        
        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            raise ValueError("Latitude and longitude must be numeric")
        
        if not -90 <= latitude <= 90:
            raise ValueError(f"Latitude {latitude} out of valid range [-90, 90]")
        
        if not -180 <= longitude <= 180:
            raise ValueError(f"Longitude {longitude} out of valid range [-180, 180]")
        
        if house_system not in ['P', 'W', 'A', 'K', 'C']:
            raise ValueError(f"Invalid house system '{house_system}'. Use P, W, A, K, or C")
        
        # Convert Skyfield time to Julian Day for Swiss Ephemeris
        try:
            utc_dt = t.utc_datetime()
            jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                           utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)
        except Exception as e:
            logger.error(f"Error converting time to Julian Day: {e}")
            raise
        
        # Calculate house cusps and angles using Swiss Ephemeris
        try:
            house_system_bytes = house_system.encode('ascii')
            houses_long = swe.houses(jd, latitude, longitude, house_system_bytes)[0]
            ascmc = swe.houses(jd, latitude, longitude, house_system_bytes)[1]
        except Exception as e:
            logger.error(f"Error calculating houses with Swiss Ephemeris: {e}")
            raise
        
        # Extract ascendant and MC
        try:
            asc_deg = normalize_angle(ascmc[0])
            mc_deg = normalize_angle(ascmc[1])
            
            asc_sign, asc_deg_in_sign = deg_to_sign_deg(asc_deg)
            mc_sign, mc_deg_in_sign = deg_to_sign_deg(mc_deg)
            
            ascendant = {
                "ecliptic_longitude_deg": asc_deg,
                "sign": asc_sign,
                "degree_in_sign": asc_deg_in_sign
            }
            
            midheaven = {
                "ecliptic_longitude_deg": mc_deg,
                "sign": mc_sign,
                "degree_in_sign": mc_deg_in_sign
            }
        except Exception as e:
            logger.error(f"Error processing ascendant/MC data: {e}")
            raise
        
        # Format all house cusps - Swiss Ephemeris returns 12 values where index 0 is Ascendant
        # Houses 1-11 are at indices 1-11, house_12 wraps around or needs special handling
        try:
            houses = {}
            
            # Houses 1-11: indices 1-11
            for i in range(1, min(12, len(houses_long))):
                house_deg = normalize_angle(houses_long[i])
                house_sign, house_deg_in_sign = deg_to_sign_deg(house_deg)
                houses[f"house_{i}"] = {
                    "ecliptic_longitude_deg": house_deg,
                    "sign": house_sign,
                    "degree_in_sign": house_deg_in_sign
                }
            
            # House 12: If we have a 12th cusp, use it
            if len(houses_long) > 11:
                house_deg = normalize_angle(houses_long[11])
                house_sign, house_deg_in_sign = deg_to_sign_deg(house_deg)
                houses["house_12"] = {
                    "ecliptic_longitude_deg": house_deg,
                    "sign": house_sign,
                    "degree_in_sign": house_deg_in_sign
                }
            
            logger.info(f"Successfully calculated {len(houses)} houses using {house_system} system")
            return ascendant, midheaven, houses
            
        except Exception as e:
            logger.error(f"Error formatting house data: {e}")
            raise
        
    except Exception as e:
        logger.error(f"Critical error in get_ascendant_mc_houses: {e}")
        raise

def calculate_whole_sign_houses(ascendant):
    """
    Calculate Whole Sign houses.
    Each house is exactly 30 degrees, starting from the Ascendant sign.
    """
    try:
        if not ascendant or "ecliptic_longitude_deg" not in ascendant:
            raise ValueError("Invalid ascendant data provided")
        
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
        
        logger.info("Successfully calculated Whole Sign houses")
        return houses
        
    except Exception as e:
        logger.error(f"Error calculating Whole Sign houses: {e}")
        raise

def calculate_equal_houses(ascendant):
    """
    Calculate Equal houses.
    Each house is exactly 30 degrees, starting from the Ascendant degree.
    """
    try:
        if not ascendant or "ecliptic_longitude_deg" not in ascendant:
            raise ValueError("Invalid ascendant data provided")
        
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
        
        logger.info("Successfully calculated Equal houses")
        return houses
        
    except Exception as e:
        logger.error(f"Error calculating Equal houses: {e}")
        raise

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
