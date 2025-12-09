#!/usr/bin/env python3
"""
test_calculations.py
Comprehensive unit tests for the natal chart calculator modules.
Tests calculations, houses, aspects, database, and astrology readings.
"""

import unittest
import sys
import os
import tempfile
import json
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from calculations import normalize_angle, deg_to_sign_deg, get_planet_longitudes, get_nodes_chiron
from houses import get_ascendant_mc_houses, calculate_whole_sign_houses, calculate_equal_houses
from aspects import compute_aspects, calculate_aspect_strength, detect_aspect_patterns
from database import AstrologyDatabase
from astrology_readings import AstrologyReadings

class TestCalculations(unittest.TestCase):
    """Test core calculation functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_angles = [0, 45, 90, 180, 270, 360, 720, -45, -180]
    
    def test_normalize_angle(self):
        """Test angle normalization"""
        test_cases = [
            (0, 0), (45, 45), (90, 90), (180, 180), (270, 270),
            (360, 0), (720, 0), (-45, 315), (-180, 180), (450, 90)
        ]
        
        for input_angle, expected in test_cases:
            with self.subTest(input_angle=input_angle):
                result = normalize_angle(input_angle)
                self.assertEqual(result, expected, f"Failed for angle {input_angle}")
                self.assertGreaterEqual(result, 0, "Angle should be non-negative")
                self.assertLess(result, 360, "Angle should be less than 360")
    
    def test_deg_to_sign_deg(self):
        """Test longitude to sign/degree conversion"""
        test_cases = [
            (0, ("Aries", 0)),
            (30, ("Taurus", 0)),
            (59.9, ("Taurus", 29.9)),
            (120, ("Leo", 0)),
            (180, ("Libra", 0)),
            (270, ("Capricorn", 0)),
            (359.9, ("Pisces", 29.9))
        ]
        
        for lon, expected in test_cases:
            with self.subTest(lon=lon):
                sign, deg = deg_to_sign_deg(lon)
                self.assertEqual(sign, expected[0], f"Wrong sign for {lon}")
                self.assertAlmostEqual(deg, expected[1], places=1, 
                                     msg=f"Wrong degree for {lon}")
    
    def test_deg_to_sign_deg_errors(self):
        """Test error handling in deg_to_sign_deg"""
        with self.assertRaises(Exception):
            deg_to_sign_deg("invalid")
        
        with self.assertRaises(Exception):
            deg_to_sign_deg(None)
    
    def test_normalize_angle_errors(self):
        """Test error handling in normalize_angle"""
        with self.assertRaises(Exception):
            normalize_angle("invalid")
        
        with self.assertRaises(Exception):
            normalize_angle(None)

class TestHouses(unittest.TestCase):
    """Test house calculation functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_ascendant = {
            "ecliptic_longitude_deg": 45.0,
            "sign": "Taurus",
            "degree_in_sign": 15.0
        }
    
    def test_calculate_whole_sign_houses(self):
        """Test Whole Sign house calculation"""
        houses = calculate_whole_sign_houses(self.test_ascendant)
        
        self.assertEqual(len(houses), 12, "Should have 12 houses")
        
        # Check house 1 starts at beginning of Ascendant sign
        house_1 = houses["house_1"]
        self.assertEqual(house_1["sign"], "Taurus")
        self.assertEqual(house_1["degree_in_sign"], 0)
        
        # Check house 2 is next sign
        house_2 = houses["house_2"]
        self.assertEqual(house_2["sign"], "Gemini")
    
    def test_calculate_equal_houses(self):
        """Test Equal house calculation"""
        houses = calculate_equal_houses(self.test_ascendant)
        
        self.assertEqual(len(houses), 12, "Should have 12 houses")
        
        # Check house 1 starts at Ascendant degree
        house_1 = houses["house_1"]
        self.assertEqual(house_1["sign"], "Taurus")
        self.assertEqual(house_1["degree_in_sign"], 15.0)
        
        # Check house 2 is 30 degrees from house 1
        house_2 = houses["house_2"]
        self.assertAlmostEqual(house_2["ecliptic_longitude_deg"], 75.0, places=1)
    
    def test_house_calculation_errors(self):
        """Test error handling in house calculations"""
        with self.assertRaises(Exception):
            calculate_whole_sign_houses(None)
        
        with self.assertRaises(Exception):
            calculate_whole_sign_houses({})
        
        with self.assertRaises(Exception):
            calculate_equal_houses(None)

class TestAspects(unittest.TestCase):
    """Test aspect calculation functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_bodies = {
            "sun": {"ecliptic_longitude_deg": 0},
            "moon": {"ecliptic_longitude_deg": 90},
            "mercury": {"ecliptic_longitude_deg": 120},
            "venus": {"ecliptic_longitude_deg": 180}
        }
    
    def test_compute_aspects(self):
        """Test aspect computation"""
        aspects = compute_aspects(self.test_bodies)
        
        self.assertIsInstance(aspects, list, "Should return a list")
        
        # Should find some aspects
        self.assertGreater(len(aspects), 0, "Should find at least one aspect")
        
        # Check aspect structure
        for aspect in aspects:
            self.assertIn("between", aspect)
            self.assertIn("aspect", aspect)
            self.assertIn("angle", aspect)
            self.assertIn("orb", aspect)
            self.assertIn("strength", aspect)
            self.assertGreaterEqual(aspect["strength"], 0)
            self.assertLessEqual(aspect["strength"], 1)
    
    def test_calculate_aspect_strength(self):
        """Test aspect strength calculation"""
        # Exact aspect should have maximum strength
        strength = calculate_aspect_strength(0, 8, "conjunction")
        self.assertAlmostEqual(strength, 1.0, places=2)
        
        # Wide orb should have lower strength
        strength = calculate_aspect_strength(7, 8, "conjunction")
        self.assertLess(strength, 1.0)
        self.assertGreater(strength, 0)
    
    def test_aspect_calculation_errors(self):
        """Test error handling in aspect calculations"""
        with self.assertRaises(Exception):
            compute_aspects(None)
        
        with self.assertRaises(Exception):
            compute_aspects({})
        
        with self.assertRaises(Exception):
            calculate_aspect_strength("invalid", 8, "conjunction")
        
        with self.assertRaises(Exception):
            calculate_aspect_strength(0, 0, "conjunction")

class TestDatabase(unittest.TestCase):
    """Test database functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.db = AstrologyDatabase(self.db_path)
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.db.close()
        os.unlink(self.db_path)
    
    def test_database_initialization(self):
        """Test database initialization"""
        self.assertIsNotNone(self.db.connection)
        stats = self.db.get_database_stats()
        self.assertIn("charts_count", stats)
    
    def test_save_and_get_chart(self):
        """Test saving and retrieving charts"""
        chart_data = {
            "bodies": {"sun": {"sign": "Aries", "degree": 10}},
            "houses": {"house_1": {"sign": "Aries", "degree": 0}}
        }
        
        chart_id = self.db.save_chart(
            "Test Person", "1998-03-03", "14:10:00",
            "Pacific/Auckland", -37.146, 174.91, "P", chart_data
        )
        
        self.assertIsInstance(chart_id, int)
        self.assertGreater(chart_id, 0)
        
        # Retrieve chart
        retrieved = self.db.get_chart(chart_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["name"], "Test Person")
        self.assertEqual(retrieved["birth_date"], "1998-03-03")
    
    def test_user_preferences(self):
        """Test user preference storage"""
        self.db.save_preference("theme", "dark")
        theme = self.db.get_preference("theme")
        self.assertEqual(theme, "dark")
        
        # Test default value
        unknown = self.db.get_preference("unknown", "default")
        self.assertEqual(unknown, "default")
    
    def test_database_errors(self):
        """Test database error handling"""
        # Test invalid database path
        with self.assertRaises(Exception):
            AstrologyDatabase("/invalid/path/database.db")

class TestAstrologyReadings(unittest.TestCase):
    """Test astrology readings functionality"""
    
    def test_get_sun_sign(self):
        """Test sun sign calculation"""
        sun_sign = AstrologyReadings.get_sun_sign(
            "1998-03-03", "14:10:00", "Pacific/Auckland", -37.146, 174.91
        )
        
        self.assertIsInstance(sun_sign, str)
        self.assertIn(sun_sign.lower(), [
            "aries", "taurus", "gemini", "cancer", "leo", "virgo",
            "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
        ])
    
    def test_get_lunar_phase(self):
        """Test lunar phase calculation"""
        lunar_phase = AstrologyReadings.get_lunar_phase(
            "2024-01-01", "12:00:00", "UTC", 0, 0
        )
        
        self.assertIsInstance(lunar_phase, str)
        self.assertIn(lunar_phase, [
            "new_moon", "waxing_crescent", "first_quarter", "waxing_gibbous",
            "full_moon", "waning_gibbous", "last_quarter", "waning_crescent"
        ])
    
    def test_sun_sign_errors(self):
        """Test error handling in sun sign calculation"""
        # This should not raise an error due to fallback logic
        sun_sign = AstrologyReadings.get_sun_sign(
            "invalid", "invalid", "invalid", 0, 0
        )
        self.assertIsInstance(sun_sign, str)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_complete_chart_calculation(self):
        """Test complete natal chart calculation workflow"""
        try:
            from natal_chart_enhanced import calculate_complete_chart
            
            chart = calculate_complete_chart(
                "1998-03-03", "14:10:00", "Pacific/Auckland",
                -37.146, 174.91
            )
            
            self.assertIsInstance(chart, dict)
            self.assertIn("birth", chart)
            self.assertIn("bodies", chart)
            self.assertIn("houses", chart)
            self.assertIn("aspects", chart)
            
            # Check essential bodies
            self.assertIn("sun", chart["bodies"])
            self.assertIn("moon", chart["bodies"])
            
        except ImportError:
            self.skipTest("natal_chart_enhanced module not available")
        except Exception as e:
            # Should not fail due to error handling
            self.fail(f"Complete chart calculation failed: {e}")
    
    def test_comprehensive_reading(self):
        """Test comprehensive astrology reading generation"""
        try:
            from natal_chart_enhanced import calculate_complete_chart
            
            natal_chart = calculate_complete_chart(
                "1998-03-03", "14:10:00", "Pacific/Auckland",
                -37.146, 174.91
            )
            
            reading = AstrologyReadings.generate_comprehensive_reading(
                natal_chart, "2024-01-01"
            )
            
            self.assertIsInstance(reading, dict)
            self.assertIn("target_date", reading)
            self.assertIn("natal_info", reading)
            self.assertIn("transits", reading)
            self.assertIn("daily_horoscope", reading)
            
        except ImportError:
            self.skipTest("natal_chart_enhanced module not available")
        except Exception as e:
            # Should not fail due to error handling
            self.fail(f"Comprehensive reading generation failed: {e}")

def run_tests():
    """Run all tests and return results"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestCalculations,
        TestHouses,
        TestAspects,
        TestDatabase,
        TestAstrologyReadings,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

if __name__ == "__main__":
    print("🧪 Running Comprehensive Test Suite for Natal Chart Calculator")
    print("=" * 70)
    
    result = run_tests()
    
    print("\n" + "=" * 70)
    print("📊 Test Results Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
