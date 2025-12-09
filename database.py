#!/usr/bin/env python3
"""
database.py
SQLite database integration for natal chart calculator.
Handles chart storage, reading history, and user data management.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AstrologyDatabase:
    """SQLite database manager for astrology charts and readings"""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection"""
        try:
            if db_path is None:
                db_path = os.path.join(os.path.dirname(__file__), 'astrology_data.db')
            
            self.db_path = db_path
            self.connection = None
            self.connect()
            self.create_tables()
            logger.info(f"Database initialized at {db_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable dict-like access
            logger.info("Database connection established")
            
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def create_tables(self):
        """Create necessary database tables"""
        try:
            cursor = self.connection.cursor()
            
            # Charts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS charts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    birth_date TEXT NOT NULL,
                    birth_time TEXT NOT NULL,
                    timezone TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    house_system TEXT DEFAULT 'P',
                    chart_data TEXT NOT NULL,  -- JSON blob
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Readings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chart_id INTEGER NOT NULL,
                    reading_type TEXT NOT NULL,  -- 'comprehensive', 'transits_only', 'horoscope_only'
                    target_date TEXT NOT NULL,
                    reading_data TEXT NOT NULL,  -- JSON blob
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chart_id) REFERENCES charts (id) ON DELETE CASCADE
                )
            ''')
            
            # Compatibility analyses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS compatibility_analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chart1_id INTEGER NOT NULL,
                    chart2_id INTEGER NOT NULL,
                    compatibility_data TEXT NOT NULL,  -- JSON blob
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chart1_id) REFERENCES charts (id) ON DELETE CASCADE,
                    FOREIGN KEY (chart2_id) REFERENCES charts (id) ON DELETE CASCADE
                )
            ''')
            
            # User preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_charts_name ON charts(name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_charts_birth_date ON charts(birth_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_readings_chart_id ON readings(chart_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_readings_target_date ON readings(target_date)')
            
            self.connection.commit()
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    def save_chart(self, name: str, birth_date: str, birth_time: str, 
                   timezone: str, latitude: float, longitude: float, 
                   house_system: str, chart_data: Dict) -> int:
        """Save a natal chart to the database"""
        try:
            cursor = self.connection.cursor()
            
            # Check if chart with same name and birth data already exists
            cursor.execute('''
                SELECT id FROM charts 
                WHERE name = ? AND birth_date = ? AND birth_time = ? 
                AND timezone = ? AND latitude = ? AND longitude = ?
            ''', (name, birth_date, birth_time, timezone, latitude, longitude))
            
            existing_chart = cursor.fetchone()
            
            if existing_chart:
                # Update existing chart
                cursor.execute('''
                    UPDATE charts 
                    SET chart_data = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (json.dumps(chart_data), existing_chart['id']))
                chart_id = existing_chart['id']
                logger.info(f"Updated existing chart: {name}")
            else:
                # Insert new chart
                cursor.execute('''
                    INSERT INTO charts (name, birth_date, birth_time, timezone, 
                                      latitude, longitude, house_system, chart_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, birth_date, birth_time, timezone, latitude, 
                      longitude, house_system, json.dumps(chart_data)))
                chart_id = cursor.lastrowid
                logger.info(f"Saved new chart: {name}")
            
            self.connection.commit()
            return chart_id
            
        except Exception as e:
            logger.error(f"Failed to save chart: {e}")
            self.connection.rollback()
            raise
    
    def get_chart(self, chart_id: int) -> Optional[Dict]:
        """Retrieve a chart by ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM charts WHERE id = ?', (chart_id,))
            row = cursor.fetchone()
            
            if row:
                chart_data = dict(row)
                chart_data['chart_data'] = json.loads(chart_data['chart_data'])
                return chart_data
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve chart {chart_id}: {e}")
            return None
    
    def get_charts_by_name(self, name: str) -> List[Dict]:
        """Retrieve all charts for a given name"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM charts WHERE name LIKE ?', (f'%{name}%',))
            rows = cursor.fetchall()
            
            charts = []
            for row in rows:
                chart_data = dict(row)
                chart_data['chart_data'] = json.loads(chart_data['chart_data'])
                charts.append(chart_data)
            
            return charts
            
        except Exception as e:
            logger.error(f"Failed to retrieve charts for {name}: {e}")
            return []
    
    def get_all_charts(self) -> List[Dict]:
        """Retrieve all charts from database"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM charts ORDER BY created_at DESC')
            rows = cursor.fetchall()
            
            charts = []
            for row in rows:
                chart_data = dict(row)
                chart_data['chart_data'] = json.loads(chart_data['chart_data'])
                charts.append(chart_data)
            
            return charts
            
        except Exception as e:
            logger.error(f"Failed to retrieve all charts: {e}")
            return []
    
    def save_reading(self, chart_id: int, reading_type: str, target_date: str, 
                     reading_data: Dict) -> int:
        """Save a reading to the database"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO readings (chart_id, reading_type, target_date, reading_data)
                VALUES (?, ?, ?, ?)
            ''', (chart_id, reading_type, target_date, json.dumps(reading_data)))
            
            reading_id = cursor.lastrowid
            self.connection.commit()
            logger.info(f"Saved reading: {reading_type} for chart {chart_id}")
            
            return reading_id
            
        except Exception as e:
            logger.error(f"Failed to save reading: {e}")
            self.connection.rollback()
            raise
    
    def get_readings_for_chart(self, chart_id: int) -> List[Dict]:
        """Retrieve all readings for a specific chart"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM readings 
                WHERE chart_id = ? 
                ORDER BY created_at DESC
            ''', (chart_id,))
            
            rows = cursor.fetchall()
            readings = []
            
            for row in rows:
                reading_data = dict(row)
                reading_data['reading_data'] = json.loads(reading_data['reading_data'])
                readings.append(reading_data)
            
            return readings
            
        except Exception as e:
            logger.error(f"Failed to retrieve readings for chart {chart_id}: {e}")
            return []
    
    def save_compatibility_analysis(self, chart1_id: int, chart2_id: int, 
                                   compatibility_data: Dict) -> int:
        """Save compatibility analysis to database"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT INTO compatibility_analyses (chart1_id, chart2_id, compatibility_data)
                VALUES (?, ?, ?)
            ''', (chart1_id, chart2_id, json.dumps(compatibility_data)))
            
            analysis_id = cursor.lastrowid
            self.connection.commit()
            logger.info(f"Saved compatibility analysis for charts {chart1_id} and {chart2_id}")
            
            return analysis_id
            
        except Exception as e:
            logger.error(f"Failed to save compatibility analysis: {e}")
            self.connection.rollback()
            raise
    
    def get_compatibility_analyses(self) -> List[Dict]:
        """Retrieve all compatibility analyses"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT ca.*, c1.name as chart1_name, c2.name as chart2_name
                FROM compatibility_analyses ca
                JOIN charts c1 ON ca.chart1_id = c1.id
                JOIN charts c2 ON ca.chart2_id = c2.id
                ORDER BY ca.created_at DESC
            ''')
            
            rows = cursor.fetchall()
            analyses = []
            
            for row in rows:
                analysis_data = dict(row)
                analysis_data['compatibility_data'] = json.loads(analysis_data['compatibility_data'])
                analyses.append(analysis_data)
            
            return analyses
            
        except Exception as e:
            logger.error(f"Failed to retrieve compatibility analyses: {e}")
            return []
    
    def save_preference(self, key: str, value: str):
        """Save user preference"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_preferences (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (key, value))
            
            self.connection.commit()
            logger.info(f"Saved preference: {key} = {value}")
            
        except Exception as e:
            logger.error(f"Failed to save preference {key}: {e}")
            self.connection.rollback()
            raise
    
    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        """Get user preference"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT value FROM user_preferences WHERE key = ?', (key,))
            row = cursor.fetchone()
            
            return row['value'] if row else default
            
        except Exception as e:
            logger.error(f"Failed to retrieve preference {key}: {e}")
            return default
    
    def delete_chart(self, chart_id: int) -> bool:
        """Delete a chart and all associated data"""
        try:
            cursor = self.connection.cursor()
            
            # Delete associated readings and compatibility analyses
            cursor.execute('DELETE FROM readings WHERE chart_id = ?', (chart_id,))
            cursor.execute('DELETE FROM compatibility_analyses WHERE chart1_id = ? OR chart2_id = ?', 
                          (chart_id, chart_id))
            
            # Delete the chart
            cursor.execute('DELETE FROM charts WHERE id = ?', (chart_id,))
            
            self.connection.commit()
            logger.info(f"Deleted chart {chart_id} and associated data")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete chart {chart_id}: {e}")
            self.connection.rollback()
            return False
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        try:
            cursor = self.connection.cursor()
            
            stats = {}
            
            # Count charts
            cursor.execute('SELECT COUNT(*) as count FROM charts')
            stats['charts_count'] = cursor.fetchone()['count']
            
            # Count readings
            cursor.execute('SELECT COUNT(*) as count FROM readings')
            stats['readings_count'] = cursor.fetchone()['count']
            
            # Count compatibility analyses
            cursor.execute('SELECT COUNT(*) as count FROM compatibility_analyses')
            stats['compatibility_analyses_count'] = cursor.fetchone()['count']
            
            # Database size
            stats['database_size_mb'] = os.path.getsize(self.db_path) / (1024 * 1024)
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {}
    
    def backup_database(self, backup_path: str) -> bool:
        """Create a backup of the database"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to backup database: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        try:
            if self.connection:
                self.connection.close()
                logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

# Global database instance
_db_instance = None

def get_database() -> AstrologyDatabase:
    """Get global database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = AstrologyDatabase()
    return _db_instance

def close_database():
    """Close global database instance"""
    global _db_instance
    if _db_instance:
        _db_instance.close()
        _db_instance = None
