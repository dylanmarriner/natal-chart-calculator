#!/usr/bin/env python3
"""
Enhanced Relationship Compatibility Calculator
Provides deep analysis including numerical scoring, destiny indicators, 
twin flame/soulmate analysis, and spiritual connection metrics.

This is a clean, publishable version suitable for GitHub distribution.
"""

import math
import json
import argparse
from typing import Dict, List, Tuple, Any
from pathlib import Path

class EnhancedCompatibilityCalculator:
    """Advanced compatibility analysis with spiritual insights."""
    
    def __init__(self):
        self.aspect_weights = {
            'conjunction': 15,
            'opposition': -8,
            'trine': 12,
            'square': -6,
            'sextile': 10,
            'quincunx': -3,
            'semi-sextile': 3,
            'semi-square': -2
        }
        
        self.destiny_weights = {
            'node_connections': 20,
            'vertex_connections': 15,
            '7th_house_synastry': 12,
            'composite_sun_moon': 18,
            'karma_connections': 15
        }
        
        self.spiritual_weights = {
            'twin_flame_indicators': 25,
            'soulmate_indicators': 20,
            'past_life_connections': 15,
            'life_path_alignment': 20,
            'harmonic_resonance': 20
        }

    def calculate_angle_difference(self, pos1: float, pos2: float) -> float:
        """Calculate the angular difference between two positions."""
        diff = abs(pos1 - pos2)
        if diff > 180:
            diff = 360 - diff
        return diff

    def determine_aspect(self, angle: float, orb: float = 8) -> Tuple[str, float]:
        """Determine the aspect between two positions."""
        aspects = [
            ('conjunction', 0, 8),
            ('opposition', 180, 8),
            ('trine', 120, 6),
            ('square', 90, 6),
            ('sextile', 60, 4),
            ('quincunx', 150, 2),
            ('semi-sextile', 30, 2),
            ('semi-square', 45, 2)
        ]
        
        for aspect_name, target_angle, max_orb in aspects:
            orb_diff = abs(angle - target_angle)
            if orb_diff <= max_orb:
                return aspect_name, orb_diff
        
        return None, None

    def calculate_synastry_aspects(self, chart1: Dict, chart2: Dict) -> Dict:
        """Calculate all synastry aspects between two charts."""
        synastry = {}
        
        bodies1 = chart1['bodies']
        bodies2 = chart2['bodies']
        
        # Calculate all planetary aspects
        for planet1, data1 in bodies1.items():
            for planet2, data2 in bodies2.items():
                angle = self.calculate_angle_difference(data1['ecliptic_longitude_deg'], 
                                                       data2['ecliptic_longitude_deg'])
                aspect, orb = self.determine_aspect(angle, orb=8)
                
                if aspect:
                    aspect_key = f"{planet1}_{planet2}_{aspect}"
                    synastry[aspect_key] = {
                        'planets': (planet1, planet2),
                        'aspect': aspect,
                        'orb': orb,
                        'angle': angle,
                        'score': self.aspect_weights.get(aspect, 0),
                        'strength': max(0, 1 - (orb / 8))
                    }
        
        return synastry

    def analyze_destiny_connections(self, chart1: Dict, chart2: Dict) -> Dict:
        """Analyze destiny indicators and fated connections."""
        destiny = {
            'node_connections': [],
            'vertex_connections': [],
            '7th_house_synastry': [],
            'part_of_fortune_connections': [],
            'score': 0,
            'max_score': 60
        }
        
        bodies1 = chart1['bodies']
        bodies2 = chart2['bodies']
        houses1 = chart1['houses']
        houses2 = chart2['houses']
        
        # North Node connections (major destiny indicator) - standard 3° orb
        significant_planets = ['sun', 'moon', 'venus', 'mars', 'jupiter', 'saturn', 'ascendant', 'midheaven']
        
        for planet in significant_planets:
            if planet in bodies1:
                angle = self.calculate_angle_difference(bodies1[planet]['ecliptic_longitude_deg'], 
                                                       bodies2['north_node']['ecliptic_longitude_deg'])
                aspect, orb = self.determine_aspect(angle, orb=5)  # Standard orb
                if aspect and orb <= 3:  # Standard destiny orb
                    destiny['node_connections'].append({
                        'planet': planet,
                        'aspect': aspect,
                        'orb': orb,
                        'significance': 'Strong destiny connection'
                    })
                    destiny['score'] += 6
        
        for planet in significant_planets:
            if planet in bodies2:
                angle = self.calculate_angle_difference(bodies2[planet]['ecliptic_longitude_deg'], 
                                                       bodies1['north_node']['ecliptic_longitude_deg'])
                aspect, orb = self.determine_aspect(angle, orb=5)
                if aspect and orb <= 3:
                    destiny['node_connections'].append({
                        'planet': planet,
                        'aspect': aspect,
                        'orb': orb,
                        'significance': 'Strong destiny connection'
                    })
                    destiny['score'] += 6
        
        # Part of Fortune connections (destiny/luck)
        for planet in significant_planets:
            if planet in bodies1:
                angle = self.calculate_angle_difference(bodies1[planet]['ecliptic_longitude_deg'], 
                                                       bodies2['part_of_fortune']['ecliptic_longitude_deg'])
                aspect, orb = self.determine_aspect(angle, orb=4)
                if aspect and orb <= 2:
                    destiny['part_of_fortune_connections'].append({
                        'planet': planet,
                        'aspect': aspect,
                        'orb': orb,
                        'significance': 'Fated luck connection'
                    })
                    destiny['score'] += 4
        
        for planet in significant_planets:
            if planet in bodies2:
                angle = self.calculate_angle_difference(bodies2[planet]['ecliptic_longitude_deg'], 
                                                       bodies1['part_of_fortune']['ecliptic_longitude_deg'])
                aspect, orb = self.determine_aspect(angle, orb=4)
                if aspect and orb <= 2:
                    destiny['part_of_fortune_connections'].append({
                        'planet': planet,
                        'aspect': aspect,
                        'orb': orb,
                        'significance': 'Fated luck connection'
                    })
                    destiny['score'] += 4
        
        # 7th House connections (relationship destiny) - standard 3° orb
        house7_cusp1 = houses1['house_7']['ecliptic_longitude_deg']
        house7_cusp2 = houses2['house_7']['ecliptic_longitude_deg']
        
        personal_planets = ['sun', 'moon', 'venus', 'mars', 'ascendant', 'midheaven']
        
        for planet in personal_planets:
            if planet in bodies1:
                angle = self.calculate_angle_difference(bodies1[planet]['ecliptic_longitude_deg'], house7_cusp2)
                aspect, orb = self.determine_aspect(angle, orb=4)
                if aspect and orb <= 3:
                    destiny['7th_house_synastry'].append({
                        'planet': planet,
                        'aspect': aspect,
                        'orb': orb,
                        'significance': 'Relationship destiny'
                    })
                    destiny['score'] += 5
        
        for planet in personal_planets:
            if planet in bodies2:
                angle = self.calculate_angle_difference(bodies2[planet]['ecliptic_longitude_deg'], house7_cusp1)
                aspect, orb = self.determine_aspect(angle, orb=4)
                if aspect and orb <= 3:
                    destiny['7th_house_synastry'].append({
                        'planet': planet,
                        'aspect': aspect,
                        'orb': orb,
                        'significance': 'Relationship destiny'
                    })
                    destiny['score'] += 5
        
        # Cap the score at maximum
        destiny['score'] = min(destiny['score'], destiny['max_score'])
        
        return destiny

    def analyze_spiritual_connections(self, chart1: Dict, chart2: Dict) -> Dict:
        """Analyze spiritual indicators including twin flame and soulmate markers."""
        spiritual = {
            'twin_flame_indicators': [],
            'soulmate_indicators': [],
            'past_life_connections': [],
            'life_path_alignment': [],
            'elemental_harmony': [],
            'score': 0,
            'max_score': 150
        }
        
        bodies1 = chart1['bodies']
        bodies2 = chart2['bodies']
        
        # Twin Flame Indicators (intense, challenging connections) - standard 3° orb
        twin_aspects = [
            ('sun', 'moon'), ('venus', 'mars'), ('ascendant', 'midheaven'),
            ('pluto', 'venus'), ('pluto', 'mars'), ('sun', 'pluto'),
            ('moon', 'pluto'), ('venus', 'pluto'), ('north_node', 'pluto'),
            ('south_node', 'pluto')
        ]
        
        for planet1, planet2 in twin_aspects:
            if planet1 in bodies1 and planet2 in bodies2:
                angle = self.calculate_angle_difference(bodies1[planet1]['ecliptic_longitude_deg'],
                                                       bodies2[planet2]['ecliptic_longitude_deg'])
                aspect, orb = self.determine_aspect(angle, orb=4)  # Standard orb
                if aspect in ['conjunction', 'opposition', 'square'] and orb <= 3:
                    spiritual['twin_flame_indicators'].append({
                        'connection': f"{planet1}-{planet2}",
                        'aspect': aspect,
                        'orb': orb,
                        'intensity': 'High'
                    })
                    spiritual['score'] += 18
        
        # Soulmate Indicators (harmonious, flowing connections) - standard 5° orb
        soulmate_aspects = [
            ('sun', 'venus'), ('moon', 'venus'), ('venus', 'jupiter'),
            ('sun', 'moon'), ('mercury', 'venus'), ('jupiter', 'north_node'),
            ('sun', 'north_node'), ('moon', 'north_node'), ('venus', 'north_node'),
            ('mars', 'venus'), ('sun', 'jupiter')
        ]
        
        for planet1, planet2 in soulmate_aspects:
            if planet1 in bodies1 and planet2 in bodies2:
                angle = self.calculate_angle_difference(bodies1[planet1]['ecliptic_longitude_deg'],
                                                       bodies2[planet2]['ecliptic_longitude_deg'])
                aspect, orb = self.determine_aspect(angle, orb=6)  # Standard orb
                if aspect in ['trine', 'sextile', 'conjunction'] and orb <= 5:
                    spiritual['soulmate_indicators'].append({
                        'connection': f"{planet1}-{planet2}",
                        'aspect': aspect,
                        'orb': orb,
                        'harmony': 'High'
                    })
                    spiritual['score'] += 15
        
        # Enhanced Elemental Harmony (same element connections) - SPIRITUALLY WEIGHTED
        # Check for Pisces-Pisces connections (MAJOR spiritual indicator)
        if bodies1['sun']['sign'] == 'Pisces' and bodies2['ascendant']['sign'] == 'Pisces':
            spiritual['elemental_harmony'].append({
                'connection': 'Sun-Pisces to Ascendant-Pisces',
                'significance': 'PROFOUND spiritual resonance - soul recognition'
            })
            spiritual['score'] += 35  # Increased from 20
        
        if bodies1['moon']['sign'] == 'Pisces' and bodies2['ascendant']['sign'] == 'Pisces':
            spiritual['elemental_harmony'].append({
                'connection': 'Moon-Pisces to Ascendant-Pisces',
                'significance': 'DEEP emotional spiritual connection'
            })
            spiritual['score'] += 25  # Increased from 15
        
        # Water element harmony - ENHANCED
        water_signs = ['cancer', 'scorpio', 'pisces']
        water_connections = 0
        
        # Count ALL water connections, not just personal planets
        all_planets = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn']
        
        for planet1 in all_planets:
            if planet1 in bodies1 and bodies1[planet1]['sign'].lower() in water_signs:
                for planet2 in all_planets:
                    if planet2 in bodies2 and bodies2[planet2]['sign'].lower() in water_signs:
                        water_connections += 1
        
        if water_connections >= 6:  # Lowered threshold for recognition
            spiritual['elemental_harmony'].append({
                'connection': f'{water_connections} water sign connections',
                'significance': 'PROFOUND emotional and spiritual harmony - soul family'
            })
            spiritual['score'] += 20  # Increased from 10
        elif water_connections >= 4:
            spiritual['elemental_harmony'].append({
                'connection': f'{water_connections} water sign connections',
                'significance': 'Strong emotional and spiritual harmony'
            })
            spiritual['score'] += 12
        
        # Past Life Connections (Saturn, South Node, Chiron) - ENHANCED WEIGHTING
        past_life_planets = ['saturn', 'south_node', 'chiron']
        significant_planets = ['sun', 'moon', 'venus', 'mars', 'jupiter']
        
        for planet1 in past_life_planets:
            if planet1 in bodies1:
                for planet2 in significant_planets:
                    if planet2 in bodies2:
                        angle = self.calculate_angle_difference(bodies1[planet1]['ecliptic_longitude_deg'],
                                                               bodies2[planet2]['ecliptic_longitude_deg'])
                        aspect, orb = self.determine_aspect(angle, orb=4)
                        if aspect and orb <= 3:
                            # EXACT aspects get major bonus
                            if orb <= 0.5:
                                spiritual['past_life_connections'].append({
                                    'connection': f"{planet1}-{planet2}",
                                    'aspect': aspect,
                                    'orb': orb,
                                    'karma': 'PROFOUND soul contract - EXACT'
                                })
                                spiritual['score'] += 20  # Major bonus for exact
                            else:
                                spiritual['past_life_connections'].append({
                                    'connection': f"{planet1}-{planet2}",
                                    'aspect': aspect,
                                    'orb': orb,
                                    'karma': 'Significant'
                                })
                                spiritual['score'] += 10
        
        # Life Path Alignment (North Node directions) - ENHANCED
        node1_sign = bodies1['north_node']['sign']
        node2_sign = bodies2['north_node']['sign']
        
        if node1_sign == node2_sign:
            spiritual['life_path_alignment'].append({
                'alignment': f"Both North Nodes in {node1_sign}",
                'significance': 'IDENTICAL life purpose - destined journey together'
            })
            spiritual['score'] += 20  # Increased from 15
        elif self.calculate_angle_difference(bodies1['north_node']['ecliptic_longitude_deg'],
                                            bodies2['north_node']['ecliptic_longitude_deg']) <= 30:
            spiritual['life_path_alignment'].append({
                'alignment': f"North Nodes in compatible signs",
                'significance': 'Harmonious life paths'
            })
            spiritual['score'] += 12  # Increased from 8
        
        # BONUS: Check for Pluto-Node connections (major twin flame indicator)
        if 'pluto' in bodies1:
            angle = self.calculate_angle_difference(bodies1['pluto']['ecliptic_longitude_deg'],
                                                   bodies2['north_node']['ecliptic_longitude_deg'])
            aspect, orb = self.determine_aspect(angle, orb=3)
            if aspect and orb <= 2:
                spiritual['twin_flame_indicators'].append({
                    'connection': 'Pluto-North Node',
                    'aspect': aspect,
                    'orb': orb,
                    'intensity': 'TRANSFORMATIONAL twin flame destiny'
                })
                spiritual['score'] += 25
        
        if 'pluto' in bodies2:
            angle = self.calculate_angle_difference(bodies2['pluto']['ecliptic_longitude_deg'],
                                                   bodies1['north_node']['ecliptic_longitude_deg'])
            aspect, orb = self.determine_aspect(angle, orb=3)
            if aspect and orb <= 2:
                spiritual['twin_flame_indicators'].append({
                    'connection': 'Pluto-North Node',
                    'aspect': aspect,
                    'orb': orb,
                    'intensity': 'TRANSFORMATIONAL twin flame destiny'
                })
                spiritual['score'] += 25
        
        # Cap the score at maximum
        spiritual['score'] = min(spiritual['score'], spiritual['max_score'])
        
        return spiritual

    def calculate_composite_chart(self, chart1: Dict, chart2: Dict) -> Dict:
        """Calculate composite chart midpoint positions."""
        composite = {}
        bodies1 = chart1['bodies']
        bodies2 = chart2['bodies']
        
        for planet in bodies1:
            if planet in bodies2:
                pos1 = bodies1[planet]['ecliptic_longitude_deg']
                pos2 = bodies2[planet]['ecliptic_longitude_deg']
                
                # Calculate midpoint
                midpoint = (pos1 + pos2) / 2
                if midpoint > 360:
                    midpoint -= 360
                
                composite[planet] = {
                    'longitude': midpoint,
                    'sign': self.get_sign_from_longitude(midpoint)
                }
        
        return composite

    def get_sign_from_longitude(self, longitude: float) -> str:
        """Get zodiac sign from longitude."""
        signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        sign_index = int(longitude / 30)
        return signs[sign_index]

    def calculate_compatibility_score(self, synastry: Dict, destiny: Dict, spiritual: Dict) -> Dict:
        """Calculate overall compatibility score out of 100 with proper normalization."""
        scores = {
            'synastry_score': 0,
            'destiny_score': 0,
            'spiritual_score': 0,
            'overall_score': 0,
            'grade': '',
            'interpretation': '',
            'synastry_details': {'positive': 0, 'negative': 0, 'neutral': 0, 'net': 0}
        }
        
        # Calculate synastry score properly
        synastry_positive = sum(aspect['score'] for aspect in synastry.values() if aspect['score'] > 0)
        synastry_negative = sum(aspect['score'] for aspect in synastry.values() if aspect['score'] < 0)
        synastry_net = synastry_positive + synastry_negative
        
        scores['synastry_details']['positive'] = synastry_positive
        scores['synastry_details']['negative'] = synastry_negative
        scores['synastry_details']['net'] = synastry_net
        
        # Normalize synastry using realistic ranges
        # Typical range: -200 to +400 based on most chart comparisons
        min_possible = -200
        max_possible = 400
        
        if synastry_net <= 0:
            # Negative or zero scores map to 0-40 range
            synastry_normalized = (synastry_net / min_possible) * 40
        else:
            # Positive scores map to 40-100 range
            synastry_normalized = 40 + (synastry_net / max_possible) * 60
        
        scores['synastry_score'] = max(0, min(100, synastry_normalized))
        
        # Destiny score (already capped at 60, normalize to 0-100)
        scores['destiny_score'] = (destiny['score'] / destiny['max_score']) * 100
        
        # Spiritual score with proper capping
        max_spiritual = 150  # Maximum possible spiritual score
        spiritual_score = min(spiritual['score'], max_spiritual)
        scores['spiritual_score'] = spiritual_score
        
        # Calculate weighted overall score
        scores['overall_score'] = (
            scores['synastry_score'] * 0.4 +
            scores['destiny_score'] * 0.3 +
            scores['spiritual_score'] * 0.3
        )
        
        # Determine grade with more realistic thresholds
        if scores['overall_score'] >= 85:
            scores['grade'] = 'A+'
            scores['interpretation'] = 'Exceptional Connection - Rare and profound'
        elif scores['overall_score'] >= 75:
            scores['grade'] = 'A'
            scores['interpretation'] = 'Outstanding Connection - Highly compatible'
        elif scores['overall_score'] >= 65:
            scores['grade'] = 'B+'
            scores['interpretation'] = 'Strong Connection - Very compatible'
        elif scores['overall_score'] >= 55:
            scores['grade'] = 'B'
            scores['interpretation'] = 'Good Connection - Compatible with growth'
        elif scores['overall_score'] >= 45:
            scores['grade'] = 'C+'
            scores['interpretation'] = 'Moderate Connection - Some challenges'
        elif scores['overall_score'] >= 35:
            scores['grade'] = 'C'
            scores['interpretation'] = 'Fair Connection - Requires work'
        else:
            scores['grade'] = 'D'
            scores['interpretation'] = 'Challenging Connection - Significant obstacles'
        
        return scores

    def get_score_description(self, score: float) -> str:
        """Get descriptive text for compatibility score."""
        if score >= 85:
            return "an exceptionally rare and profound connection"
        elif score >= 75:
            return "an outstanding and deeply meaningful connection"
        elif score >= 65:
            return "a strong and highly compatible connection"
        elif score >= 55:
            return "a good connection with solid compatibility"
        elif score >= 45:
            return "a moderate connection requiring conscious effort"
        elif score >= 35:
            return "a fair connection that needs dedicated work"
        else:
            return "a challenging connection with significant obstacles"

    def get_final_recommendation(self, scores: Dict, spiritual: Dict, destiny: Dict) -> str:
        """Generate final recommendation based on scores."""
        if scores['overall_score'] >= 75:
            return "This cosmic blessing should be cherished and nurtured. Trust that you were meant to meet - there's a higher purpose to your connection."
        elif scores['overall_score'] >= 60:
            return "With conscious effort and mutual understanding, this relationship can develop into something beautiful and lasting. The foundation is solid."
        elif scores['overall_score'] >= 45:
            return "This relationship requires patience and communication but can grow into something meaningful. Focus on understanding differences."
        else:
            return "This relationship faces significant obstacles but may offer important lessons. Requires exceptional commitment and self-awareness."

    def generate_compatibility_report(self, chart1: Dict, chart2: Dict, 
                                    name1: str, name2: str) -> str:
        """Generate comprehensive compatibility report."""
        
        # Calculate all analyses
        synastry = self.calculate_synastry_aspects(chart1, chart2)
        destiny = self.analyze_destiny_connections(chart1, chart2)
        spiritual = self.analyze_spiritual_connections(chart1, chart2)
        composite = self.calculate_composite_chart(chart1, chart2)
        scores = self.calculate_compatibility_score(synastry, destiny, spiritual)
        
        # Debug: Show synastry breakdown
        harmonious_count = len([a for a in synastry.values() if a['score'] > 0])
        challenging_count = len([a for a in synastry.values() if a['score'] < 0])
        total_aspects = len(synastry)
        
        report = f"""
# 🔮 Enhanced Relationship Compatibility Report
## {name1} & {name2}

---

## 📊 COMPATIBILITY SCORES

### **Overall Score: {scores['overall_score']:.1f}/100** 
**Grade: {scores['grade']} - {scores['interpretation']}**

| Category | Score | Weight |
|----------|-------|--------|
| **Synastry Harmony** | {scores['synastry_score']:.1f}/100 | 40% |
| **Destiny Connection** | {scores['destiny_score']:.1f}/100 | 30% |
| **Spiritual Bond** | {scores['spiritual_score']:.1f}/100 | 30% |

**Synastry Breakdown:** {total_aspects} total aspects ({harmonious_count} harmonious, {challenging_count} challenging)
**Raw Score:** {scores['synastry_details']['positive']:.1f} positive, {scores['synastry_details']['negative']:.1f} negative

---

## 🌟 DESTINY & FATED CONNECTIONS

### **Were You Destined to Meet? {'✅ YES' if destiny['score'] >= 20 else '❌ NO'}**
**Destiny Score: {destiny['score']}/{destiny['max_score']}**

**Node Connections (Life Path Alignment):**
"""
        
        for connection in destiny['node_connections']:
            report += f"- {connection['planet']} {connection['aspect']} North Node (orb: {connection['orb']:.1f}°) - {connection['significance']}\n"
        
        report += f"\n**7th House Synastry (Relationship Destiny):**\n"
        for connection in destiny['7th_house_synastry']:
            report += f"- {connection['planet']} in 7th House {connection['aspect']} (orb: {connection['orb']:.1f}°) - {connection['significance']}\n"
        
        report += f"\n**Part of Fortune Connections:**\n"
        for connection in destiny['part_of_fortune_connections']:
            report += f"- {connection['planet']} {connection['aspect']} Part of Fortune (orb: {connection['orb']:.1f}°) - {connection['significance']}\n"
        
        report += f"""

---

## 🔥 SPIRITUAL CONNECTION ANALYSIS

### **Twin Flame Indicators: {'⚡ STRONG' if len(spiritual['twin_flame_indicators']) >= 2 else '⚡ MODERATE' if len(spiritual['twin_flame_indicators']) == 1 else '💫 MINIMAL'}**
**Twin Flame Score: {len(spiritual['twin_flame_indicators']) * 18}/180**

"""
        
        for indicator in spiritual['twin_flame_indicators']:
            report += f"- {indicator['connection']} {indicator['aspect']} (orb: {indicator['orb']:.1f}°) - {indicator['intensity']} intensity\n"
        
        report += f"\n### **Soulmate Indicators: {'💕 STRONG' if len(spiritual['soulmate_indicators']) >= 3 else '💕 MODERATE' if len(spiritual['soulmate_indicators']) >= 1 else '💫 MINIMAL'}**\n"
        for indicator in spiritual['soulmate_indicators']:
            report += f"- {indicator['connection']} {indicator['aspect']} (orb: {indicator['orb']:.1f}°) - {indicator['harmony']} harmony\n"
        
        report += f"\n**Past Life Connections:**\n"
        for connection in spiritual['past_life_connections']:
            report += f"- {connection['connection']} {connection['aspect']} (orb: {connection['orb']:.1f}°) - {connection['karma']} karma\n"
        
        report += f"\n**Elemental Harmony:**\n"
        for harmony in spiritual['elemental_harmony']:
            report += f"- {harmony['connection']} - {harmony['significance']}\n"
        
        report += f"\n**Life Path Alignment:**\n"
        for alignment in spiritual['life_path_alignment']:
            report += f"- {alignment['alignment']} - {alignment['significance']}\n"
        
        report += f"""

---

## 💫 SYNASTRY HIGHLIGHTS

### **Top 5 Strongest Aspects:**
"""
        
        # Sort synastry by strength
        sorted_synastry = sorted(synastry.items(), key=lambda x: x[1]['strength'], reverse=True)[:5]
        
        for aspect_name, aspect_data in sorted_synastry:
            planet1, planet2 = aspect_data['planets']
            score_type = "✨" if aspect_data['score'] > 0 else "⚡" if aspect_data['score'] < 0 else "➖"
            report += f"- {score_type} **{planet1.capitalize()} {aspect_data['aspect']} {planet2.capitalize()}** (orb: {aspect_data['orb']:.1f}°, score: {aspect_data['score']:+.1f})\n"
        
        report += f"\n### **Harmonious Aspects (Supportive):**\n"
        harmonious = [a for a in synastry.values() if a['score'] > 0]
        for aspect in harmonious[:5]:
            planet1, planet2 = aspect['planets']
            report += f"- {planet1.capitalize()} {aspect['aspect']} {planet2.capitalize()} - Flowing energy (score: {aspect['score']:+.1f})\n"
        
        report += f"\n### **Challenging Aspects (Growth Areas):**\n"
        challenging = [a for a in synastry.values() if a['score'] < 0]
        if challenging:
            for aspect in challenging[:5]:
                planet1, planet2 = aspect['planets']
                report += f"- {planet1.capitalize()} {aspect['aspect']} {planet2.capitalize()} - Tension for growth (score: {aspect['score']:+.1f})\n"
        else:
            report += "- No significant challenging aspects detected\n"
        
        report += f"""

---

## 🌈 COMPOSITE CHART INSIGHTS

**Relationship Essence:**
"""
        
        if 'sun' in composite:
            report += f"- **Composite Sun:** {composite['sun']['sign']} - Relationship identity and purpose\n"
        if 'moon' in composite:
            report += f"- **Composite Moon:** {composite['moon']['sign']} - Emotional foundation of the relationship\n"
        if 'venus' in composite:
            report += f"- **Composite Venus:** {composite['venus']['sign']} - How love and harmony are expressed\n"
        if 'mars' in composite:
            report += f"- **Composite Mars:** {composite['mars']['sign']} - Shared drive and passion\n"
        
        report += f"""

---

## 💖 RELATIONSHIP RECOMMENDATIONS

### **Strengths to Nurture:**
"""
        
        if scores['spiritual_score'] >= 70:
            report += "- **Deep Spiritual Connection** - Nurture shared spiritual practices and intuitive understanding\n"
        if scores['destiny_score'] >= 60:
            report += "- **Fated Connection** - Trust the timing and purpose of your meeting\n"
        if scores['synastry_score'] >= 60:
            report += "- **Natural Harmony** - Build on your easy flow and mutual understanding\n"
        
        report += f"\n### **Areas for Growth:**\n"
        if challenging_count >= 3:
            report += "- **Embrace Tension** - Use challenging aspects as opportunities for deeper understanding\n"
        if destiny['score'] < 15:
            report += "- **Create Shared Purpose** - Consciously build meaning and direction together\n"
        if len(spiritual['soulmate_indicators']) < 2:
            report += "- **Cultivate Harmony** - Practice patience and develop flowing communication\n"
        
        report += f"""

### **Long-Term Potential:**
"""
        
        if scores['overall_score'] >= 75:
            report += "✨ **Exceptional Potential** - This relationship has the ingredients for profound, lasting love and mutual growth. The cosmic alignment supports a deeply meaningful connection.\n"
        elif scores['overall_score'] >= 60:
            report += "💫 **Strong Potential** - With conscious effort and mutual understanding, this relationship can develop into something beautiful and lasting. The foundation is solid.\n"
        elif scores['overall_score'] >= 45:
            report += "🌱 **Moderate Potential** - This relationship requires patience and communication but can grow into something meaningful. Focus on understanding differences.\n"
        else:
            report += "⚠️ **Challenging Potential** - This relationship faces significant obstacles but may offer important lessons. Requires exceptional commitment and self-awareness.\n"
        
        report += f"""

---

## 🎯 FINAL VERDICT

**{name1} & {name2}:** {scores['interpretation']}

Your compatibility score of **{scores['overall_score']:.1f}/100** indicates {self.get_score_description(scores['overall_score'])}.

{self.get_final_recommendation(scores, spiritual, destiny)}

---

*Generated with advanced synastry calculations and spiritual compatibility analysis*
*Calculation Method: Enhanced Swiss Ephemeris + Spiritual Indicators*
"""
        
        return report

def load_chart_from_json(file_path: str) -> Dict:
    """Load natal chart data from JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Chart file not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in chart file: {file_path}")
        print(f"JSON Error: {e}")
        return {}

def main():
    """Main function for command line usage."""
    parser = argparse.ArgumentParser(description='Enhanced Relationship Compatibility Calculator')
    parser.add_argument('chart1', help='Path to first person\'s chart JSON file')
    parser.add_argument('chart2', help='Path to second person\'s chart JSON file')
    parser.add_argument('--name1', default='Person A', help='Name of first person')
    parser.add_argument('--name2', default='Person B', help='Name of second person')
    parser.add_argument('--output', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    # Load charts
    chart1 = load_chart_from_json(args.chart1)
    chart2 = load_chart_from_json(args.chart2)
    
    if not chart1 or not chart2:
        print("Error: Could not load chart files")
        return
    
    # Calculate compatibility
    calculator = EnhancedCompatibilityCalculator()
    report = calculator.generate_compatibility_report(chart1, chart2, args.name1, args.name2)
    
    # Save or print report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"✅ Enhanced compatibility report generated!")
        print(f"📄 Saved as: {args.output}")
    else:
        print(report)

if __name__ == "__main__":
    main()
