#!/usr/bin/env python3
"""
astrology_readings.py
Astrology readings and daily horoscopes module.
Includes transit calculations, daily horoscopes, and lunar phase interpretations.
"""

import swisseph as swe
from datetime import datetime, timedelta
import math
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class AstrologyReadings:
    """Professional astrology readings and daily horoscopes"""
    
    # Planetary aspects and their meanings
    ASPECT_MEANINGS = {
        'conjunction': {
            'general': 'Powerful new beginnings, intensified energy, merging of influences',
            'harmonious': 'Strong positive focus, enhanced abilities, major opportunities',
            'challenging': 'Intense challenges, internal conflicts, need for integration'
        },
        'opposition': {
            'general': 'Balance, relationships, awareness of opposites, external conflicts',
            'harmonious': 'Harmonious partnerships, successful negotiations, balance achieved',
            'challenging': 'Relationship tensions, external conflicts, need for compromise'
        },
        'trine': {
            'general': 'Flow, harmony, ease, natural talents, fortunate circumstances',
            'harmonious': 'Excellent luck, smooth progress, creative breakthroughs',
            'challenging': 'Overconfidence, missed opportunities due to complacency'
        },
        'square': {
            'general': 'Challenge, growth, tension, obstacles, building strength',
            'harmonious': 'Productive challenges, growth through effort, dynamic action',
            'challenging': 'Frustrating obstacles, internal conflicts, stress and pressure'
        },
        'sextile': {
            'general': 'Opportunities, communication, cooperation, pleasant connections',
            'harmonious': 'Easy opportunities, helpful connections, skillful communication',
            'challenging': 'Missed connections, wasted opportunities, communication issues'
        },
        'quincunx': {
            'general': 'Adjustment, healing, transformation, unexpected changes',
            'harmonious': 'Positive transformations, healing breakthroughs, creative solutions',
            'challenging': 'Difficult adjustments, health issues, unexpected disruptions'
        }
    }
    
    # Sun sign horoscope templates
    SUN_SIGN_HOROSCOPES = {
        'aries': {
            'element': 'Fire',
            'ruler': 'Mars',
            'themes': ['leadership', 'courage', 'initiative', 'competition', 'action'],
            'positive': 'Bold moves and new ventures are favored. Your natural leadership shines.',
            'challenging': 'Patience is needed. Avoid impulsive decisions and temper flare-ups.',
            'general': 'A time for action and initiative. Trust your instincts but think before acting.'
        },
        'taurus': {
            'element': 'Earth',
            'ruler': 'Venus',
            'themes': ['stability', 'security', 'values', 'pleasure', 'determination'],
            'positive': 'Financial opportunities and relationship harmony are highlighted.',
            'challenging': 'Stubbornness may create obstacles. Stay flexible with change.',
            'general': 'Focus on building security and enjoying life\'s pleasures. Steady progress wins.'
        },
        'gemini': {
            'element': 'Air',
            'ruler': 'Mercury',
            'themes': ['communication', 'learning', 'adaptability', 'social connections', 'curiosity'],
            'positive': 'Excellent communication and social opportunities. Ideas flow freely.',
            'challenging': 'Scattered energy and misunderstandings. Focus and clarity needed.',
            'general': 'Time for learning and connecting. Share your ideas and stay open-minded.'
        },
        'cancer': {
            'element': 'Water',
            'ruler': 'Moon',
            'themes': ['emotions', 'home', 'family', 'nurturing', 'intuition'],
            'positive': 'Emotional harmony and family connections bring deep satisfaction.',
            'challenging': 'Mood swings and emotional sensitivity. Create emotional boundaries.',
            'general': 'Honor your feelings and create a nurturing environment. Trust intuition.'
        },
        'leo': {
            'element': 'Fire',
            'ruler': 'Sun',
            'themes': ['creativity', 'self-expression', 'leadership', 'recognition', 'generosity'],
            'positive': 'Creative expression and recognition are highlighted. Shine brightly!',
            'challenging': 'Ego conflicts and need for attention. Practice humility and listen.',
            'general': 'Express your unique creativity and leadership. Share your warmth generously.'
        },
        'virgo': {
            'element': 'Earth',
            'ruler': 'Mercury',
            'themes': ['service', 'analysis', 'health', 'organization', 'perfection'],
            'positive': 'Productive work and health improvements. Details fall into place.',
            'challenging': 'Over-analysis and criticism. Perfect is the enemy of good.',
            'general': 'Focus on practical improvements and service. Your attention to detail pays off.'
        },
        'libra': {
            'element': 'Air',
            'ruler': 'Venus',
            'themes': ['balance', 'relationships', 'harmony', 'justice', 'beauty'],
            'positive': 'Harmonious relationships and aesthetic pleasures. Balance achieved.',
            'challenging': 'Indecision and relationship tensions. Trust your inner guidance.',
            'general': 'Seek balance in all areas. Relationships and partnerships are key focus.'
        },
        'scorpio': {
            'element': 'Water',
            'ruler': 'Pluto',
            'themes': ['transformation', 'depth', 'power', 'intensity', 'mystery'],
            'positive': 'Deep transformation and empowerment. Hidden truths revealed.',
            'challenging': 'Power struggles and intensity. Channel emotions constructively.',
            'general': 'Embrace transformation and go beneath the surface. Trust your power.'
        },
        'sagittarius': {
            'element': 'Fire',
            'ruler': 'Jupiter',
            'themes': ['expansion', 'optimism', 'adventure', 'philosophy', 'freedom'],
            'positive': 'Adventure and learning opportunities abound. Optimism pays dividends.',
            'challenging': 'Over-optimism and restlessness. Ground your visions in reality.',
            'general': 'Expand your horizons through learning and adventure. Maintain optimism.'
        },
        'capricorn': {
            'element': 'Earth',
            'ruler': 'Saturn',
            'themes': ['ambition', 'structure', 'responsibility', 'achievement', 'discipline'],
            'positive': 'Career advancement and long-term goals progress. Structure supports success.',
            'challenging': 'Rigidity and excessive responsibility. Allow for flexibility and rest.',
            'general': 'Build toward long-term goals with discipline and patience. Achievement comes.'
        },
        'aquarius': {
            'element': 'Air',
            'ruler': 'Uranus',
            'themes': ['innovation', 'freedom', 'humanity', 'unconventionality', 'future'],
            'positive': 'Innovative ideas and social connections. Breakthrough thinking.',
            'challenging': 'Unpredictability and detachment. Stay connected to practical needs.',
            'general': 'Embrace innovation and think outside the box. Connect with your community.'
        },
        'pisces': {
            'element': 'Water',
            'ruler': 'Neptune',
            'themes': ['compassion', 'creativity', 'spirituality', 'intuition', 'sacrifice'],
            'positive': 'Creative inspiration and spiritual insights. Compassion flows freely.',
            'challenging': 'Confusion and escapism. Ground spiritual insights in practical action.',
            'general': 'Trust your intuition and creative inspiration. Practice compassion.'
        }
    }
    
    # Lunar phase interpretations
    LUNAR_PHASES = {
        'new_moon': {
            'energy': 'Beginnings, setting intentions, planting seeds',
            'advice': 'Start new projects, set clear intentions, begin fresh cycles',
            'duration': '3-4 days of dark moon energy'
        },
        'waxing_crescent': {
            'energy': 'Growth, expansion, building momentum',
            'advice': 'Take action on intentions, gather resources, build support',
            'duration': '3-4 days of growing energy'
        },
        'first_quarter': {
            'energy': 'Action, overcoming obstacles, decision points',
            'advice': 'Face challenges head-on, make important decisions, take decisive action',
            'duration': '1-2 days of crisis/opportunity energy'
        },
        'waxing_gibbous': {
            'energy': 'Refinement, adjustment, preparation',
            'advice': 'Refine plans, make adjustments, prepare for culmination',
            'duration': '3-4 days of building energy'
        },
        'full_moon': {
            'energy': 'Culmination, illumination, completion, release',
            'advice': 'Celebrate achievements, release what no longer serves, emotional clarity',
            'duration': '2-3 days of peak energy'
        },
        'waning_gibbous': {
            'energy': 'Gratitude, sharing, releasing',
            'advice': 'Share wisdom, release attachments, practice gratitude',
            'duration': '3-4 days of decreasing energy'
        },
        'last_quarter': {
            'energy': 'Reflection, re-evaluation, release',
            'advice': 'Reflect on lessons learned, release old patterns, prepare for new cycle',
            'duration': '1-2 days of crisis/release energy'
        },
        'waning_crescent': {
            'energy': 'Rest, purification, surrender',
            'advice': 'Rest and restore, cleanse and purify, surrender to the unknown',
            'duration': '3-4 days of dark moon preparation'
        }
    }
    
    @staticmethod
    def get_sun_sign(date: str, time: str, timezone: str, latitude: float, longitude: float) -> str:
        """Get sun sign for a given birth date"""
        try:
            # Calculate natal chart for the given date
            from natal_chart_enhanced import calculate_complete_chart
            chart = calculate_complete_chart(date, time, timezone, latitude, longitude)
            return chart['bodies']['sun']['sign'].lower()
        except:
            # Fallback to simple zodiac calculation
            month_day = datetime.strptime(date, "%Y-%m-%d").strftime("%m-%d")
            zodiac_dates = [
                ("03-21", "04-19", "aries"), ("04-20", "05-20", "taurus"),
                ("05-21", "06-20", "gemini"), ("06-21", "07-22", "cancer"),
                ("07-23", "08-22", "leo"), ("08-23", "09-22", "virgo"),
                ("09-23", "10-22", "libra"), ("10-23", "11-21", "scorpio"),
                ("11-22", "12-21", "sagittarius"), ("12-22", "01-19", "capricorn"),
                ("01-20", "02-18", "aquarius"), ("02-19", "03-20", "pisces")
            ]
            
            for start, end, sign in zodiac_dates:
                if start == "12-22" and month_day >= start or month_day <= end:
                    return sign
                elif start <= month_day <= end:
                    return sign
            return "aries"
    
    @staticmethod
    def calculate_transits(natal_chart: dict, target_date: str = None) -> dict:
        """Calculate transits for a specific date compared to natal chart"""
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")
        
        target_time = "12:00:00"
        target_tz = natal_chart['birth']['timezone']
        target_lat = natal_chart['birth']['latitude']
        target_lon = natal_chart['birth']['longitude']
        
        # Calculate current planetary positions
        from natal_chart_enhanced import calculate_complete_chart
        current_chart = calculate_complete_chart(target_date, target_time, target_tz, target_lat, target_lon)
        
        transits = {
            'date': target_date,
            'aspects': [],
            'major_transits': [],
            'interpretations': []
        }
        
        # Calculate transit aspects
        natal_bodies = natal_chart['bodies']
        current_bodies = current_chart['bodies']
        
        aspect_orbs = {
            'conjunction': 8, 'opposition': 8, 'trine': 8,
            'square': 8, 'sextile': 6, 'quincunx': 3
        }
        
        target_angles = {
            'conjunction': 0, 'opposition': 180, 'trine': 120,
            'square': 90, 'sextile': 60, 'quincunx': 150
        }
        
        for natal_planet, natal_pos in natal_bodies.items():
            for current_planet, current_pos in current_bodies.items():
                angle = abs(natal_pos['ecliptic_longitude_deg'] - current_pos['ecliptic_longitude_deg'])
                angle = min(angle, 360 - angle)
                
                for aspect_name, orb in aspect_orbs.items():
                    target_angle = target_angles[aspect_name]
                    orb_diff = abs(angle - target_angle)
                    
                    if orb_diff <= orb:
                        strength = max(0, 1 - (orb_diff / orb))
                        
                        transit_aspect = {
                            'natal_planet': natal_planet,
                            'transiting_planet': current_planet,
                            'aspect': aspect_name,
                            'angle': angle,
                            'orb': orb_diff,
                            'strength': strength,
                            'interpretation': AstrologyReadings.get_transit_interpretation(
                                natal_planet, current_planet, aspect_name, strength
                            )
                        }
                        
                        transits['aspects'].append(transit_aspect)
                        
                        # Identify major transits (strong aspects to personal planets)
                        if strength > 0.7 and natal_planet in ['sun', 'moon', 'mercury', 'venus', 'mars', 'ascendant']:
                            transits['major_transits'].append(transit_aspect)
        
        # Sort by strength
        transits['aspects'].sort(key=lambda x: x['strength'], reverse=True)
        transits['major_transits'].sort(key=lambda x: x['strength'], reverse=True)
        
        return transits
    
    @staticmethod
    def get_transit_interpretation(natal_planet: str, transiting_planet: str, aspect: str, strength: float) -> str:
        """Get interpretation for a specific transit"""
        planet_meanings = {
            'sun': 'identity, vitality, life purpose',
            'moon': 'emotions, instincts, needs',
            'mercury': 'communication, thinking, learning',
            'venus': 'love, values, relationships',
            'mars': 'action, desire, energy',
            'jupiter': 'growth, expansion, opportunity',
            'saturn': 'structure, responsibility, limitation',
            'uranus': 'change, innovation, awakening',
            'neptune': 'dreams, spirituality, illusion',
            'pluto': 'transformation, power, rebirth'
        }
        
        aspect_qualities = AstrologyReadings.ASPECT_MEANINGS.get(aspect, {})
        
        natal_meaning = planet_meanings.get(natal_planet, 'personal themes')
        transiting_meaning = planet_meanings.get(transiting_planet, 'current influences')
        
        if strength > 0.8:
            intensity = "Strong"
        elif strength > 0.6:
            intensity = "Moderate"
        else:
            intensity = "Mild"
        
        base_interpretation = f"{intensity} {aspect} between transiting {transiting_planet.title()} and natal {natal_planet.title()}"
        
        if aspect_qualities:
            quality = aspect_qualities.get('general', 'significant interaction')
            return f"{base_interpretation}: {quality}"
        
        return base_interpretation
    
    @staticmethod
    def generate_daily_horoscope(date: str, time: str, timezone: str, latitude: float, longitude: float) -> dict:
        """Generate a comprehensive daily horoscope"""
        sun_sign = AstrologyReadings.get_sun_sign(date, time, timezone, latitude, longitude)
        
        # Get current planetary positions
        from natal_chart_enhanced import calculate_complete_chart
        current_chart = calculate_complete_chart(date, time, timezone, latitude, longitude)
        
        # Calculate lunar phase
        lunar_phase = AstrologyReadings.get_lunar_phase(date, time, timezone, latitude, longitude)
        
        # Get sun sign data
        sign_data = AstrologyReadings.SUN_SIGN_HOROSCOPES.get(sun_sign, {})
        
        # Analyze current aspects to sun
        sun_aspects = []
        for aspect in current_chart.get('aspects', []):
            if 'sun' in aspect['between'] and aspect['strength'] > 0.5:
                sun_aspects.append(aspect)
        
        # Generate horoscope based on sun sign and current aspects
        horoscope = {
            'date': date,
            'sun_sign': sun_sign.title(),
            'element': sign_data.get('element', 'Unknown'),
            'ruler': sign_data.get('ruler', 'Unknown'),
            'lunar_phase': lunar_phase,
            'key_themes': sign_data.get('themes', []),
            'daily_message': '',
            'energy_level': '',
            'lucky_areas': [],
            'challenges': [],
            'advice': ''
        }
        
        # Determine energy level based on aspects
        harmonious_aspects = len([a for a in sun_aspects if a['aspect'] in ['trine', 'sextile']])
        challenging_aspects = len([a for a in sun_aspects if a['aspect'] in ['square', 'opposition']])
        
        if harmonious_aspects > challenging_aspects:
            horoscope['energy_level'] = 'High'
            horoscope['daily_message'] = sign_data.get('positive', 'Positive energy flows your way today.')
        elif challenging_aspects > harmonious_aspects:
            horoscope['energy_level'] = 'Challenging'
            horoscope['daily_message'] = sign_data.get('challenging', 'Challenges require your attention today.')
        else:
            horoscope['energy_level'] = 'Moderate'
            horoscope['daily_message'] = sign_data.get('general', 'A balanced day with mixed energies.')
        
        # Add lunar phase influence
        lunar_data = AstrologyReadings.LUNAR_PHASES.get(lunar_phase, {})
        if lunar_data:
            horoscope['advice'] = f"Lunar Phase: {lunar_data.get('energy', 'Mystical lunar energies')}. {lunar_data.get('advice', 'Work with moon cycles.')}"
        
        # Add specific areas based on ruling planet aspects
        horoscope['lucky_areas'] = ['Creativity', 'Communication', 'Relationships']
        horoscope['challenges'] = ['Patience', 'Timing', 'Flexibility']
        
        return horoscope
    
    @staticmethod
    def get_lunar_phase(date: str, time: str, timezone: str, latitude: float, longitude: float) -> str:
        """Calculate current lunar phase"""
        try:
            # Calculate moon position
            from natal_chart_enhanced import calculate_complete_chart
            chart = calculate_complete_chart(date, time, timezone, latitude, longitude)
            moon_longitude = chart['bodies']['moon']['ecliptic_longitude_deg']
            
            # Calculate sun position
            sun_longitude = chart['bodies']['sun']['ecliptic_longitude_deg']
            
            # Calculate phase angle
            phase_angle = (moon_longitude - sun_longitude) % 360
            
            # Determine lunar phase
            if phase_angle < 22.5 or phase_angle >= 337.5:
                return 'new_moon'
            elif 22.5 <= phase_angle < 67.5:
                return 'waxing_crescent'
            elif 67.5 <= phase_angle < 112.5:
                return 'first_quarter'
            elif 112.5 <= phase_angle < 157.5:
                return 'waxing_gibbous'
            elif 157.5 <= phase_angle < 202.5:
                return 'full_moon'
            elif 202.5 <= phase_angle < 247.5:
                return 'waning_gibbous'
            elif 247.5 <= phase_angle < 292.5:
                return 'last_quarter'
            else:
                return 'waning_crescent'
        except:
            return 'full_moon'  # Default fallback
    
    @staticmethod
    def generate_comprehensive_reading(natal_chart: dict, target_date: str = None) -> dict:
        """Generate a comprehensive astrology reading including transits and horoscope"""
        if target_date is None:
            target_date = datetime.now().strftime("%Y-%m-%d")
        
        # Get birth data
        birth_data = natal_chart['birth']
        
        # Calculate transits
        transits = AstrologyReadings.calculate_transits(natal_chart, target_date)
        
        # Generate daily horoscope
        horoscope = AstrologyReadings.generate_daily_horoscope(
            birth_data['date'], birth_data['time_local'], 
            birth_data['timezone'], birth_data['latitude'], birth_data['longitude']
        )
        
        # Combine into comprehensive reading
        reading = {
            'target_date': target_date,
            'natal_info': {
                'name': birth_data.get('name', 'Unknown'),
                'birth_date': birth_data['date'],
                'sun_sign': horoscope['sun_sign']
            },
            'transits': transits,
            'daily_horoscope': horoscope,
            'key_influences': transits['major_transits'][:3],  # Top 3 major transits
            'overall_theme': AstrologyReadings.get_overall_theme(transits, horoscope)
        }
        
        return reading
    
    @staticmethod
    def get_overall_theme(transits: dict, horoscope: dict) -> str:
        """Determine the overall theme for the day"""
        major_transits = transits.get('major_transits', [])
        energy_level = horoscope.get('energy_level', 'Moderate')
        lunar_phase = horoscope.get('lunar_phase', 'full_moon')
        
        if not major_transits:
            return f"A relatively calm day with {energy_level.lower()} energy. Focus on daily routines and the {lunar_phase.replace('_', ' ')} energy."
        
        # Analyze major transit themes
        themes = []
        for transit in major_transits[:2]:
            if 'sun' in [transit['natal_planet'], transit['transiting_planet']]:
                themes.append("identity and life purpose")
            if 'moon' in [transit['natal_planet'], transit['transiting_planet']]:
                themes.append("emotions and inner needs")
            if 'venus' in [transit['natal_planet'], transit['transiting_planet']]:
                themes.append("relationships and values")
            if 'mars' in [transit['natal_planet'], transit['transiting_planet']]:
                themes.append("action and initiative")
            if 'jupiter' in [transit['natal_planet'], transit['transiting_planet']]:
                themes.append("growth and opportunity")
        
        if themes:
            return f"A dynamic day focusing on {', '.join(themes)}. With {energy_level.lower()} energy and {lunar_phase.replace('_', ' ')} influences, significant developments are possible."
        
        return f"An active day with {energy_level.lower()} energy. The {lunar_phase.replace('_', ' ')} phase supports your current activities."
