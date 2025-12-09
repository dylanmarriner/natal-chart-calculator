#!/usr/bin/env python3
"""
aspects.py

Aspect calculations and pattern detection for natal charts.
Includes aspect analysis, pattern detection (T-squares, Grand Trines, Yods),
and aspect strength scoring.
"""

import logging
from calculations import normalize_angle

# Configure logging
logger = logging.getLogger(__name__)

ASPECTS = {
    "conjunction": 0,
    "semi-sextile": 30,
    "semi-square": 45,
    "sextile": 60,
    "square": 90,
    "trine": 120,
    "quincunx": 150,
    "opposition": 180
}

ASPECT_ORBS = {
    "conjunction": 8,
    "semi-sextile": 2,
    "semi-square": 2,
    "sextile": 6,
    "square": 7,
    "trine": 8,
    "quincunx": 2,
    "opposition": 8
}

def angle_difference(a, b):
    """Calculate the smallest angular distance between two points."""
    try:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("Both angles must be numeric")
        
        diff = abs(a - b) % 360
        if diff > 180:
            diff = 360 - diff
        return diff
        
    except Exception as e:
        logger.error(f"Error calculating angle difference between {a} and {b}: {e}")
        raise

def compute_aspects(bodies, aspect_orbs=None, include_points=None):
    """
    Calculate aspects between all bodies in the chart.
    
    Args:
        bodies: Dictionary of celestial bodies with positions
        aspect_orbs: Custom orb dictionary (optional)
        include_points: List of additional points to include (e.g., nodes, chiron)
    
    Returns:
        list: List of aspect dictionaries
    """
    try:
        if not bodies or not isinstance(bodies, dict):
            raise ValueError("Bodies must be a non-empty dictionary")
        
        if aspect_orbs is None:
            aspect_orbs = ASPECT_ORBS
        elif not isinstance(aspect_orbs, dict):
            raise ValueError("Aspect orbs must be a dictionary")
        
        aspects = []
        names = list(bodies.keys())
        
        # Validate that all bodies have required position data
        for name in names:
            if name not in bodies or "ecliptic_longitude_deg" not in bodies[name]:
                raise ValueError(f"Body '{name}' missing ecliptic_longitude_deg data")
        
        # Filter bodies if specific points requested
        if include_points:
            if not isinstance(include_points, list):
                raise ValueError("include_points must be a list")
            names = [name for name in names if name in include_points]
        
        if len(names) < 2:
            logger.warning("Less than 2 bodies available for aspect calculation")
            return aspects
        
        for i in range(len(names)):
            for j in range(i+1, len(names)):
                try:
                    n1 = names[i]
                    n2 = names[j]
                    lon1 = bodies[n1]["ecliptic_longitude_deg"]
                    lon2 = bodies[n2]["ecliptic_longitude_deg"]
                    
                    if not isinstance(lon1, (int, float)) or not isinstance(lon2, (int, float)):
                        logger.warning(f"Invalid longitude values for {n1} or {n2}")
                        continue
                    
                    diff = angle_difference(lon1, lon2)
                    
                    for asp, angle in ASPECTS.items():
                        orb = aspect_orbs.get(asp, 5)
                        if abs(diff - angle) <= orb:
                            try:
                                strength = calculate_aspect_strength(abs(diff - angle), orb, asp)
                                aspects.append({
                                    "between": [n1, n2],
                                    "aspect": asp,
                                    "angle": diff,
                                    "orb": abs(diff - angle),
                                    "strength": strength
                                })
                            except Exception as e:
                                logger.warning(f"Error calculating strength for {asp} between {n1} and {n2}: {e}")
                                continue
                            break
                except Exception as e:
                    logger.warning(f"Error processing aspect between {names[i]} and {names[j]}: {e}")
                    continue
        
        logger.info(f"Successfully calculated {len(aspects)} aspects")
        return aspects
        
    except Exception as e:
        logger.error(f"Critical error in compute_aspects: {e}")
        raise

def calculate_aspect_strength(actual_orb, max_orb, aspect_type):
    """
    Calculate aspect strength based on orb tightness and aspect importance.
    
    Args:
        actual_orb: How far from exact aspect
        max_orb: Maximum allowed orb for this aspect
        aspect_type: Type of aspect
    
    Returns:
        float: Strength score (0-1)
    """
    # Input validation - raise exceptions for invalid inputs
    if not all(isinstance(val, (int, float)) for val in [actual_orb, max_orb]):
        raise ValueError("Orb values must be numeric")
    
    if not isinstance(aspect_type, str):
        raise ValueError("Aspect type must be a string")
    
    if max_orb <= 0:
        raise ValueError("Max orb must be positive")
    
    if actual_orb < 0:
        actual_orb = abs(actual_orb)
    
    # Base strength from orb tightness
    orb_strength = 1 - (actual_orb / max_orb)
    
    # Aspect importance weights
    aspect_weights = {
        "conjunction": 1.0,
        "opposition": 0.9,
        "trine": 0.8,
        "square": 0.8,
        "sextile": 0.6,
        "quincunx": 0.4,
        "semi-square": 0.3,
        "semi-sextile": 0.2
    }
    
    aspect_weight = aspect_weights.get(aspect_type, 0.5)
    
    strength = orb_strength * aspect_weight
    
    # Ensure strength is within valid range
    if strength < 0:
        strength = 0
    elif strength > 1:
        strength = 1
    
    return round(strength, 3)

def detect_aspect_patterns(aspects, bodies):
    """
    Detect major aspect patterns: T-squares, Grand Trines, Grand Crosses, Yods.
    
    Args:
        aspects: List of aspect dictionaries
        bodies: Dictionary of celestial bodies
    
    Returns:
        dict: Dictionary of detected patterns
    """
    try:
        if not aspects or not isinstance(aspects, list):
            raise ValueError("Aspects must be a non-empty list")
        
        if not bodies or not isinstance(bodies, dict):
            raise ValueError("Bodies must be a non-empty dictionary")
        
        patterns = {
            "t_squares": [],
            "grand_trines": [],
            "grand_crosses": [],
            "yods": [],
            "stelliums": []
        }
        
        # Get all aspect relationships for pattern detection
        try:
            aspect_graph = build_aspect_graph(aspects)
        except Exception as e:
            logger.warning(f"Error building aspect graph: {e}")
            aspect_graph = {}
        
        try:
            patterns["t_squares"] = detect_t_squares(aspect_graph, bodies)
        except Exception as e:
            logger.warning(f"Error detecting T-squares: {e}")
        
        try:
            patterns["grand_trines"] = detect_grand_trines(aspect_graph, bodies)
        except Exception as e:
            logger.warning(f"Error detecting Grand Trines: {e}")
        
        try:
            patterns["grand_crosses"] = detect_grand_crosses(aspect_graph, bodies)
        except Exception as e:
            logger.warning(f"Error detecting Grand Crosses: {e}")
        
        try:
            patterns["yods"] = detect_yods(aspect_graph, bodies)
        except Exception as e:
            logger.warning(f"Error detecting Yods: {e}")
        
        try:
            patterns["stelliums"] = detect_stelliums(bodies)
        except Exception as e:
            logger.warning(f"Error detecting Stelliums: {e}")
        
        total_patterns = sum(len(patterns[key]) for key in patterns)
        logger.info(f"Successfully detected {total_patterns} aspect patterns")
        return patterns
        
    except Exception as e:
        logger.error(f"Critical error in detect_aspect_patterns: {e}")
        # Return empty patterns on error
        return {"t_squares": [], "grand_trines": [], "grand_crosses": [], "yods": [], "stelliums": []}

def build_aspect_graph(aspects):
    """Build a graph representation of aspects for pattern detection."""
    try:
        if not aspects or not isinstance(aspects, list):
            return {}
        
        graph = {}
        for aspect in aspects:
            try:
                if "aspect" not in aspect or "between" not in aspect:
                    continue
                
                if aspect["aspect"] in ["square", "trine", "opposition", "quincunx", "conjunction"]:
                    body1, body2 = aspect["between"]
                    
                    if not isinstance(body1, str) or not isinstance(body2, str):
                        continue
                    
                    if body1 not in graph:
                        graph[body1] = []
                    if body2 not in graph:
                        graph[body2] = []
                    
                    graph[body1].append({"to": body2, "aspect": aspect["aspect"]})
                    graph[body2].append({"to": body1, "aspect": aspect["aspect"]})
            except Exception as e:
                logger.warning(f"Error processing aspect in graph building: {e}")
                continue
        
        return graph
        
    except Exception as e:
        logger.error(f"Error building aspect graph: {e}")
        return {}

def detect_t_squares(graph, bodies):
    """Detect T-square patterns (two squares with an opposition)."""
    t_squares = []
    reported_configs = set()  # Track already-reported configurations
    
    # Only consider main planets and nodes for patterns
    valid_bodies = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn", 
                   "uranus", "neptune", "pluto", "north_node", "south_node"]
    
    # Filter graph to only include valid bodies
    filtered_graph = {}
    for body, connections in graph.items():
        if body in valid_bodies:
            filtered_connections = [conn for conn in connections if conn["to"] in valid_bodies]
            if filtered_connections:
                filtered_graph[body] = filtered_connections
    
    # Find oppositions first
    oppositions = []
    for body, connections in filtered_graph.items():
        for conn in connections:
            if conn["aspect"] == "opposition":
                oppositions.append((body, conn["to"]))
    
    # For each opposition, look for squares to both ends
    for opp in oppositions:
        body1, body2 = opp
        squares_to_body1 = [conn["to"] for conn in filtered_graph.get(body1, []) if conn["aspect"] == "square"]
        squares_to_body2 = [conn["to"] for conn in filtered_graph.get(body2, []) if conn["aspect"] == "square"]
        
        # Find common planet squaring both ends
        common_squares = set(squares_to_body1) & set(squares_to_body2)
        for focal_planet in common_squares:
            # Create canonical representation (sorted tuple of all three planets)
            config = tuple(sorted([focal_planet, body1, body2]))
            
            if config not in reported_configs:
                reported_configs.add(config)
                t_squares.append({
                    "type": "T-square",
                    "focal_planet": focal_planet,
                    "opposition": [body1, body2],
                    "strength": calculate_pattern_strength(focal_planet, [body1, body2], bodies)
                })
    
    return t_squares

def detect_grand_trines(graph, bodies):
    """Detect Grand Trine patterns (three planets in trine)."""
    grand_trines = []
    
    # Look for triangles of trines
    planets = list(bodies.keys())
    
    for i in range(len(planets)):
        for j in range(i+1, len(planets)):
            for k in range(j+1, len(planets)):
                p1, p2, p3 = planets[i], planets[j], planets[k]
                
                # Check if all three are in trine
                trine_count = 0
                for pair in [(p1, p2), (p1, p3), (p2, p3)]:
                    if has_aspect_between(graph, pair[0], pair[1], "trine"):
                        trine_count += 1
                
                if trine_count == 3:
                    grand_trines.append({
                        "type": "Grand Trine",
                        "planets": [p1, p2, p3],
                        "element": get_trine_element(bodies[p1]["ecliptic_longitude_deg"]),
                        "strength": calculate_grand_trine_strength([p1, p2, p3], bodies)
                    })
    
    return grand_trines

def is_grand_cross(graph, planets):
    """Check if four planets form a Grand Cross pattern."""
    # Grand Cross: 4 planets where each planet squares two others
    # and there are two oppositions
    if len(planets) != 4:
        return False
    
    # Count squares and oppositions
    square_count = 0
    opposition_count = 0
    
    for i, p1 in enumerate(planets):
        for p2 in planets[i+1:]:
            if has_aspect_between(graph, p1, p2, "square"):
                square_count += 1
            elif has_aspect_between(graph, p1, p2, "opposition"):
                opposition_count += 1
    
    # Grand Cross needs exactly 4 squares and 2 oppositions
    return square_count == 4 and opposition_count == 2

def detect_grand_crosses(graph, bodies):
    """Detect Grand Cross patterns (four planets in square, two oppositions)."""
    grand_crosses = []
    
    planets = list(bodies.keys())
    
    for i in range(len(planets)):
        for j in range(i+1, len(planets)):
            for k in range(j+1, len(planets)):
                for l in range(k+1, len(planets)):
                    cross_planets = [planets[i], planets[j], planets[k], planets[l]]
                    
                    # Check for Grand Cross: 4 squares in a cross pattern
                    if is_grand_cross(graph, cross_planets):
                        grand_crosses.append({
                            "type": "Grand Cross",
                            "planets": cross_planets,
                            "cardinality": get_cross_cardinality(cross_planets, bodies),
                            "strength": calculate_cross_strength(cross_planets, bodies)
                        })
    
    return grand_crosses

def detect_yods(graph, bodies):
    """Detect Yod patterns (two quincunxes with a sextile)."""
    yods = []
    
    planets = list(bodies.keys())
    
    for focal in planets:
        quincunx_to = [conn["to"] for conn in graph.get(focal, []) if conn["aspect"] == "quincunx"]
        
        if len(quincunx_to) >= 2:
            # Check if any two quincunxed planets are sextile
            for i in range(len(quincunx_to)):
                for j in range(i+1, len(quincunx_to)):
                    p1, p2 = quincunx_to[i], quincunx_to[j]
                    if has_aspect_between(graph, p1, p2, "sextile"):
                        yods.append({
                            "type": "Yod",
                            "focal_planet": focal,
                            "base_planets": [p1, p2],
                            "strength": calculate_yod_strength(focal, [p1, p2], bodies)
                        })
    
    return yods

def detect_stelliums(bodies, orb=8):
    """Detect stelliums (3+ planets in close conjunction)."""
    stelliums = []
    processed_planets = set()  # Track planets already in stelliums
    
    planets = list(bodies.keys())
    positions = [(name, bodies[name]["ecliptic_longitude_deg"]) for name in planets]
    
    # Sort by longitude
    positions.sort(key=lambda x: x[1])
    
    # Look for clusters
    for i in range(len(positions)):
        if positions[i][0] in processed_planets:
            continue  # Skip planets already in a stellium
            
        cluster = [positions[i]]
        for j in range(i+1, len(positions)):
            if positions[j][0] in processed_planets:
                continue
                
            if angle_difference(positions[i][1], positions[j][1]) <= orb:
                cluster.append(positions[j])
            else:
                break
        
        if len(cluster) >= 3:
            # Add all planets in cluster to processed set
            for planet_name, _ in cluster:
                processed_planets.add(planet_name)
                
            stelliums.append({
                "type": "Stellium",
                "planets": [p[0] for p in cluster],
                "sign": bodies[cluster[0][0]]["sign"],
                "orb_range": angle_difference(cluster[0][1], cluster[-1][1])
            })
    
    return stelliums

def has_aspect_between(graph, body1, body2, aspect_type):
    """Check if two bodies have a specific aspect."""
    for conn in graph.get(body1, []):
        if conn["to"] == body2 and conn["aspect"] == aspect_type:
            return True
    return False

def get_trine_element(longitude):
    """Get the element of a trine based on longitude."""
    deg = longitude % 360
    if 0 <= deg < 120:
        return "Fire"
    elif 120 <= deg < 240:
        return "Earth"
    else:
        return "Air/Water"

def get_cross_cardinality(planets, bodies):
    """Get the cardinality of a Grand Cross."""
    longitudes = [bodies[p]["ecliptic_longitude_deg"] for p in planets]
    # Check if they're in cardinal, fixed, or mutable signs
    mod_counts = {"cardinal": 0, "fixed": 0, "mutable": 0}
    
    for lon in longitudes:
        sign_num = int(lon // 30) % 12
        if sign_num in [0, 3, 6, 9]:  # Cardinal signs
            mod_counts["cardinal"] += 1
        elif sign_num in [1, 4, 7, 10]:  # Fixed signs
            mod_counts["fixed"] += 1
        else:  # Mutable signs
            mod_counts["mutable"] += 1
    
    return max(mod_counts, key=mod_counts.get)

def calculate_pattern_strength(focal_planet, base_planets, bodies):
    """Calculate strength of T-square or Yod pattern."""
    # Strength based on personal planets involvement
    personal_planets = ["sun", "moon", "mercury", "venus", "mars"]
    all_planets = [focal_planet] + base_planets
    
    personal_count = sum(1 for p in all_planets if p in personal_planets)
    return round(0.5 + (personal_count * 0.1), 3)

def calculate_grand_trine_strength(planets, bodies):
    """Calculate strength of Grand Trine."""
    personal_planets = ["sun", "moon", "mercury", "venus", "mars"]
    personal_count = sum(1 for p in planets if p in personal_planets)
    return round(0.6 + (personal_count * 0.08), 3)

def calculate_cross_strength(planets, bodies):
    """Calculate strength of Grand Cross."""
    personal_planets = ["sun", "moon", "mercury", "venus", "mars"]
    personal_count = sum(1 for p in planets if p in personal_planets)
    return round(0.7 + (personal_count * 0.075), 3)

def calculate_yod_strength(focal_planet, base_planets, bodies):
    """Calculate strength of Yod pattern."""
    personal_planets = ["sun", "moon", "mercury", "venus", "mars"]
    all_planets = [focal_planet] + base_planets
    
    personal_count = sum(1 for p in all_planets if p in personal_planets)
    return round(0.4 + (personal_count * 0.12), 3)
