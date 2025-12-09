#!/usr/bin/env python3
"""
desktop_gui.py
Standalone desktop GUI for natal chart calculator with compatibility analysis.
Uses CustomTkinter with Dylan's custom sci-fi theme.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import json
import pandas as pd
from datetime import datetime
import sys
import os
import threading
from typing import Dict, Any, Optional

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from natal_chart_enhanced import calculate_complete_chart
from cli import save_chart_json, save_chart_csv, save_chart_text
from theme import DylanCustomTheme

class CompatibilityCalculator:
    """Handles synastry compatibility calculations between two charts"""
    
    @staticmethod
    def calculate_synastry(chart1: Dict, chart2: Dict) -> Dict:
        """Calculate synastry aspects between two charts"""
        synastry = {
            'aspects': [],
            'compatibility_score': 0,
            'key_aspects': [],
            'analysis': {}
        }
        
        # Get planetary positions from both charts
        bodies1 = chart1.get('bodies', {})
        bodies2 = chart2.get('bodies', {})
        
        # Define aspect orbs and meanings
        aspects_config = {
            'conjunction': {'orb': 8, 'weight': 3, 'harmony': 'neutral'},
            'opposition': {'orb': 8, 'weight': 2, 'harmony': 'challenging'},
            'trine': {'orb': 8, 'weight': 3, 'harmony': 'harmonious'},
            'square': {'orb': 8, 'weight': 2, 'harmony': 'challenging'},
            'sextile': {'orb': 6, 'weight': 2, 'harmony': 'harmonious'},
            'quincunx': {'orb': 3, 'weight': 1, 'harmony': 'challenging'},
        }
        
        # Calculate planet-to-planet aspects
        for planet1, pos1 in bodies1.items():
            for planet2, pos2 in bodies2.items():
                angle = abs(pos1['ecliptic_longitude_deg'] - pos2['ecliptic_longitude_deg'])
                angle = min(angle, 360 - angle)
                
                for aspect_name, config in aspects_config.items():
                    target_angles = {
                        'conjunction': 0,
                        'opposition': 180,
                        'trine': 120,
                        'square': 90,
                        'sextile': 60,
                        'quincunx': 150,
                    }
                    
                    target_angle = target_angles[aspect_name]
                    orb_diff = abs(angle - target_angle)
                    
                    if orb_diff <= config['orb']:
                        synastry['aspects'].append({
                            'between': [planet1, planet2],
                            'aspect': aspect_name,
                            'angle': angle,
                            'orb': orb_diff,
                            'strength': max(0, 1 - (orb_diff / config['orb'])),
                            'harmony': config['harmony'],
                            'weight': config['weight']
                        })
        
        # Calculate compatibility score
        total_score = 0
        max_score = 0
        
        for aspect in synastry['aspects']:
            strength = aspect['strength']
            weight = aspect['weight']
            
            if aspect['harmony'] == 'harmonious':
                total_score += strength * weight
            elif aspect['harmony'] == 'challenging':
                total_score += strength * weight * 0.5  # Challenging aspects worth half
            else:  # neutral
                total_score += strength * weight * 0.75
            
            max_score += weight
        
        synastry['compatibility_score'] = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Identify key aspects
        synastry['key_aspects'] = [
            aspect for aspect in synastry['aspects'] 
            if aspect['strength'] > 0.7 and aspect['weight'] >= 2
        ]
        
        # Generate analysis
        synastry['analysis'] = CompatibilityCalculator.generate_analysis(synastry)
        
        return synastry
    
    @staticmethod
    def generate_analysis(synastry: Dict) -> Dict:
        """Generate compatibility analysis text"""
        score = synastry['compatibility_score']
        key_aspects = synastry['key_aspects']
        
        # Determine overall compatibility
        if score >= 80:
            overall = "Excellent"
            description = "Strong harmonious connections with excellent compatibility"
        elif score >= 65:
            overall = "Very Good"
            description = "Good compatibility with mostly harmonious aspects"
        elif score >= 50:
            overall = "Good"
            description = "Balanced compatibility with mix of harmonious and challenging aspects"
        elif score >= 35:
            overall = "Moderate"
            description = "Some compatibility with notable challenges to work through"
        else:
            overall = "Challenging"
            description = "Significant differences that require conscious effort to harmonize"
        
        # Analyze key themes
        themes = []
        harmonious_count = len([a for a in key_aspects if a['harmony'] == 'harmonious'])
        challenging_count = len([a for a in key_aspects if a['harmony'] == 'challenging'])
        
        if harmonious_count > challenging_count:
            themes.append("Strong mutual understanding and support")
        if challenging_count > 0:
            themes.append("Growth opportunities through challenges")
        if any('venus' in a['between'] or 'mars' in a['between'] for a in key_aspects):
            themes.append("Strong romantic and creative connection")
        if any('jupiter' in a['between'] for a in key_aspects):
            themes.append("Shared optimism and expansion")
        if any('saturn' in a['between'] for a in key_aspects):
            themes.append("Serious commitment and stability potential")
        
        return {
            'overall': overall,
            'description': description,
            'score': score,
            'themes': themes,
            'harmonious_aspects': harmonious_count,
            'challenging_aspects': challenging_count,
            'total_key_aspects': len(key_aspects)
        }

class NatalChartGUI:
    """Main desktop GUI application"""
    
    def __init__(self):
        # Set up the main window
        self.root = ctk.CTk()
        self.root.title("🌟 Enhanced Natal Chart Calculator")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Apply Dylan's custom theme
        self.theme = DylanCustomTheme()
        self.theme.apply_theme(ctk)
        
        # Configure main window styling
        self.root.configure(fg_color=self.theme.get_color('background.primary'))
        
        # Initialize variables
        self.current_chart = None
        self.person1_chart = None
        self.person2_chart = None
        self.compatibility_result = None
        
        # Create GUI components
        self.create_widgets()
        
        # Center window on screen
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create main container
        main_container = ctk.CTkFrame(self.root, corner_radius=10)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create title
        title_label = ctk.CTkLabel(
            main_container,
            text="🌟 Enhanced Natal Chart Calculator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_container,
            text="Professional Astrological Calculations with Compatibility Analysis",
            font=ctk.CTkFont(size=14),
            text_color=self.theme.get_color('text.secondary')
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Create tabbed interface
        self.tabview = ctk.CTkTabview(main_container, width=1100, height=600)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configure tabs
        self.create_natal_chart_tab()
        self.create_compatibility_tab()
        self.create_about_tab()
    
    def create_natal_chart_tab(self):
        """Create the single natal chart tab"""
        tab = self.tabview.add("🪐 Natal Chart")
        
        # Create main container for this tab
        tab_frame = ctk.CTkFrame(tab)
        tab_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create input section
        input_frame = ctk.CTkFrame(tab_frame)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Title for input section
        input_title = ctk.CTkLabel(
            input_frame,
            text="📊 Birth Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        input_title.pack(pady=10)
        
        # Create input fields in a grid
        fields_frame = ctk.CTkFrame(input_frame)
        fields_frame.pack(fill="x", padx=20, pady=10)
        
        # Personal Information
        self.name_var = ctk.StringVar(value="Dylan")
        self.create_input_field(fields_frame, "Name:", self.name_var, 0, 0)
        
        # Date and Time
        self.date_var = ctk.StringVar(value="1998-03-03")
        self.create_input_field(fields_frame, "Birth Date (YYYY-MM-DD):", self.date_var, 0, 1)
        
        self.time_var = ctk.StringVar(value="14:10:00")
        self.create_input_field(fields_frame, "Birth Time (HH:MM:SS):", self.time_var, 0, 2)
        
        # Location
        self.latitude_var = ctk.StringVar(value="-37.203")
        self.create_input_field(fields_frame, "Latitude:", self.latitude_var, 1, 0)
        
        self.longitude_var = ctk.StringVar(value="174.934")
        self.create_input_field(fields_frame, "Longitude:", self.longitude_var, 1, 1)
        
        self.timezone_var = ctk.StringVar(value="Pacific/Auckland")
        self.create_input_field(fields_frame, "Timezone:", self.timezone_var, 1, 2)
        
        # Options
        options_frame = ctk.CTkFrame(input_frame)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        # House system
        house_frame = ctk.CTkFrame(options_frame)
        house_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(house_frame, text="House System:").pack(side="left", padx=10)
        self.house_system_var = ctk.StringVar(value="P")
        house_menu = ctk.CTkOptionMenu(
            house_frame,
            variable=self.house_system_var,
            values=["P (Placidus)", "W (Whole Sign)", "A (Equal)", "K (Koch)", "C (Campanus)"],
            width=200
        )
        house_menu.pack(side="left", padx=10)
        
        # Calculate button
        button_frame = ctk.CTkFrame(input_frame)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        calculate_btn = ctk.CTkButton(
            button_frame,
            text="🌟 Calculate Natal Chart",
            command=self.calculate_natal_chart,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        calculate_btn.pack(pady=10)
        
        # Results section
        results_frame = ctk.CTkFrame(tab_frame)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        results_title = ctk.CTkLabel(
            results_frame,
            text="📈 Chart Results",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        results_title.pack(pady=10)
        
        # Create scrollable results area
        self.results_text = ctk.CTkTextbox(results_frame, height=300)
        self.results_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Export buttons
        export_frame = ctk.CTkFrame(results_frame)
        export_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            export_frame,
            text="💾 Save JSON",
            command=lambda: self.save_chart("json"),
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            export_frame,
            text="💾 Save CSV",
            command=lambda: self.save_chart("csv"),
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            export_frame,
            text="💾 Save Text",
            command=lambda: self.save_chart("text"),
            width=120
        ).pack(side="left", padx=5)
    
    def create_compatibility_tab(self):
        """Create the compatibility calculator tab"""
        tab = self.tabview.add("💕 Compatibility")
        
        # Create main container
        tab_frame = ctk.CTkFrame(tab)
        tab_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            tab_frame,
            text="💕 Synastry Compatibility Calculator",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=10)
        
        # Create two-person input section
        persons_frame = ctk.CTkFrame(tab_frame)
        persons_frame.pack(fill="x", padx=20, pady=10)
        
        # Person 1 section
        person1_frame = ctk.CTkFrame(persons_frame)
        person1_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            person1_frame,
            text="👤 Person 1",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=5)
        
        self.p1_name = ctk.StringVar(value="Person 1")
        self.p1_date = ctk.StringVar(value="1998-03-03")
        self.p1_time = ctk.StringVar(value="14:10:00")
        self.p1_lat = ctk.StringVar(value="-37.203")
        self.p1_lon = ctk.StringVar(value="174.934")
        self.p1_tz = ctk.StringVar(value="Pacific/Auckland")
        
        self.create_person_inputs(person1_frame, self.p1_name, self.p1_date, self.p1_time, 
                                  self.p1_lat, self.p1_lon, self.p1_tz)
        
        # Person 2 section
        person2_frame = ctk.CTkFrame(persons_frame)
        person2_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            person2_frame,
            text="👤 Person 2",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=5)
        
        self.p2_name = ctk.StringVar(value="Person 2")
        self.p2_date = ctk.StringVar(value="1990-07-15")
        self.p2_time = ctk.StringVar(value="09:30:00")
        self.p2_lat = ctk.StringVar(value="40.713")
        self.p2_lon = ctk.StringVar(value="-74.006")
        self.p2_tz = ctk.StringVar(value="America/New_York")
        
        self.create_person_inputs(person2_frame, self.p2_name, self.p2_date, self.p2_time,
                                  self.p2_lat, self.p2_lon, self.p2_tz)
        
        # Calculate compatibility button
        compat_btn = ctk.CTkButton(
            tab_frame,
            text="💕 Calculate Compatibility",
            command=self.calculate_compatibility,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        compat_btn.pack(pady=10)
        
        # Compatibility results
        results_frame = ctk.CTkFrame(tab_frame)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.compat_results = ctk.CTkTextbox(results_frame, height=300)
        self.compat_results.pack(fill="both", expand=True, padx=20, pady=10)
    
    def create_person_inputs(self, parent, name_var, date_var, time_var, lat_var, lon_var, tz_var):
        """Create input fields for a person"""
        fields = [
            ("Name:", name_var),
            ("Date (YYYY-MM-DD):", date_var),
            ("Time (HH:MM:SS):", time_var),
            ("Latitude:", lat_var),
            ("Longitude:", lon_var),
            ("Timezone:", tz_var)
        ]
        
        for i, (label, var) in enumerate(fields):
            frame = ctk.CTkFrame(parent)
            frame.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(frame, text=label, width=120).pack(side="left")
            entry = ctk.CTkEntry(frame, textvariable=var, width=150)
            entry.pack(side="left", padx=5)
    
    def create_input_field(self, parent, label, variable, row, col):
        """Create a labeled input field"""
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(frame, text=label, width=150).pack(side="left")
        entry = ctk.CTkEntry(frame, textvariable=variable, width=200)
        entry.pack(side="left", padx=5)
    
    def create_about_tab(self):
        """Create the about tab"""
        tab = self.tabview.add("ℹ️ About")
        
        about_frame = ctk.CTkFrame(tab)
        about_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        about_text = """
🌟 Enhanced Natal Chart Calculator v1.0

FEATURES:
• Complete planetary positions with retrograde detection
• North/South Nodes, Chiron, and Part of Fortune calculations  
• Multiple house systems (Placidus, Whole Sign, Equal, Koch, Campanus)
• Advanced aspect pattern detection (T-squares, Grand Trines, Yods, Stelliums)
• Synastry compatibility analysis between two charts
• Multiple output formats (JSON, CSV, text)
• Professional Swiss Ephemeris integration

TECHNICAL:
• Built with Python, CustomTkinter, and Swiss Ephemeris
• Dylan's Custom Sci-fi Theme for stunning visual appearance
• Cross-platform compatibility (Windows, macOS, Linux)
• Standalone desktop application

CREDITS:
• Swiss Ephemeris for high-precision astronomical calculations
• Skyfield for planetary position calculations
• CustomTkinter for modern UI components
• Theme design by Dylan Marriner

© 2025 Enhanced Natal Chart Calculator
MIT License
        """
        
        about_label = ctk.CTkLabel(about_frame, text=about_text, justify="left")
        about_label.pack(padx=20, pady=20)
    
    def calculate_natal_chart(self):
        """Calculate a single natal chart"""
        try:
            # Get input values
            name = self.name_var.get()
            date = self.date_var.get()
            time = self.time_var.get()
            timezone = self.timezone_var.get()
            latitude = float(self.latitude_var.get())
            longitude = float(self.longitude_var.get())
            house_system = self.house_system_var.get().split()[0]
            
            # Validate inputs
            if not all([name, date, time, timezone]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            # Calculate chart in a separate thread to avoid freezing GUI
            def calculate():
                try:
                    chart = calculate_complete_chart(
                        date, time, timezone, latitude, longitude, house_system
                    )
                    self.current_chart = chart
                    self.display_natal_results(chart)
                except Exception as e:
                    messagebox.showerror("Calculation Error", f"Error calculating chart: {str(e)}")
            
            # Show loading indicator
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", "🔮 Calculating your natal chart...")
            self.root.update()
            
            # Run calculation
            threading.Thread(target=calculate, daemon=True).start()
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    
    def calculate_compatibility(self):
        """Calculate compatibility between two people"""
        try:
            # Get person 1 data
            p1_data = {
                'name': self.p1_name.get(),
                'date': self.p1_date.get(),
                'time': self.p1_time.get(),
                'timezone': self.p1_tz.get(),
                'latitude': float(self.p1_lat.get()),
                'longitude': float(self.p1_lon.get())
            }
            
            # Get person 2 data
            p2_data = {
                'name': self.p2_name.get(),
                'date': self.p2_date.get(),
                'time': self.p2_time.get(),
                'timezone': self.p2_tz.get(),
                'latitude': float(self.p2_lat.get()),
                'longitude': float(self.p2_lon.get())
            }
            
            # Validate inputs
            required_fields = ['name', 'date', 'time', 'timezone']
            for key in required_fields:
                if not p1_data.get(key) or not p2_data.get(key):
                    messagebox.showerror("Error", f"Please fill in all required fields for both people")
                    return
            
            # Show loading
            self.compat_results.delete("1.0", "end")
            self.compat_results.insert("1.0", "💕 Calculating compatibility analysis...")
            self.root.update()
            
            def calculate():
                try:
                    # Calculate both charts
                    chart1 = calculate_complete_chart(
                        p1_data['date'], p1_data['time'], p1_data['timezone'],
                        p1_data['latitude'], p1_data['longitude']
                    )
                    chart2 = calculate_complete_chart(
                        p2_data['date'], p2_data['time'], p2_data['timezone'],
                        p2_data['latitude'], p2_data['longitude']
                    )
                    
                    # Calculate synastry
                    synastry = CompatibilityCalculator.calculate_synastry(chart1, chart2)
                    
                    self.person1_chart = chart1
                    self.person2_chart = chart2
                    self.compatibility_result = synastry
                    
                    self.display_compatibility_results(p1_data, p2_data, synastry)
                    
                except Exception as e:
                    messagebox.showerror("Calculation Error", f"Error calculating compatibility: {str(e)}")
            
            threading.Thread(target=calculate, daemon=True).start()
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    
    def display_natal_results(self, chart):
        """Display natal chart results"""
        self.results_text.delete("1.0", "end")
        
        # Format results
        results = f"""
🌟 NATAL CHART FOR {chart['birth']['date']} {chart['birth']['time_local']}
📍 Location: {chart['birth']['latitude']:.3f}°, {chart['birth']['longitude']:.3f}°

🪐 PLANETARY POSITIONS:
"""
        
        # Add planetary positions
        for body_name, body_data in chart['bodies'].items():
            retrograde = " R" if body_data.get('retrograde', False) else ""
            results += f"   {body_name.replace('_', ' ').title()}: {body_data['sign']} {body_data['degree_in_sign']:.2f}°{retrograde}\n"
        
        results += f"""
⬆️ ANGLES:
   Ascendant: {chart['angles']['ascendant']['sign']} {chart['angles']['ascendant']['degree_in_sign']:.2f}°
   Midheaven: {chart['angles']['midheaven']['sign']} {chart['angles']['midheaven']['degree_in_sign']:.2f}°

🏠 HOUSES:
"""
        
        # Add house positions
        for house_name, house_data in chart['houses'].items():
            results += f"   {house_name.replace('_', ' ').title()}: {house_data['sign']} {house_data['degree_in_sign']:.2f}°\n"
        
        # Add aspect patterns if available
        if 'aspect_patterns' in chart:
            patterns = chart['aspect_patterns']
            results += f"\n🔮 ASPECT PATTERNS DETECTED: {len(patterns)}\n"
            for pattern in patterns:
                results += f"   • {pattern['type']}: {pattern.get('description', 'N/A')}\n"
        
        results += f"\n✨ Chart calculation complete! {len(chart['aspects'])} aspects analyzed."
        
        self.results_text.insert("1.0", results)
    
    def display_compatibility_results(self, p1_data, p2_data, synastry):
        """Display compatibility results"""
        self.compat_results.delete("1.0", "end")
        
        analysis = synastry['analysis']
        
        results = f"""
💕 SYNASTRY COMPATIBILITY ANALYSIS
=====================================

👤 PERSON 1: {p1_data['name']}
   Born: {p1_data['date']} {p1_data['time']} in {p1_data['timezone']}

👤 PERSON 2: {p2_data['name']}  
   Born: {p2_data['date']} {p2_data['time']} in {p2_data['timezone']}

🎯 OVERALL COMPATIBILITY: {analysis['overall']}
📊 COMPATIBILITY SCORE: {analysis['score']:.1f}%

📝 DESCRIPTION:
{analysis['description']}

🔮 KEY THEMES:
"""
        
        for theme in analysis['themes']:
            results += f"   • {theme}\n"
        
        results += f"""
📈 ASPECT BREAKDOWN:
   Harmonious Aspects: {analysis['harmonious_aspects']}
   Challenging Aspects: {analysis['challenging_aspects']}
   Total Key Aspects: {analysis['total_key_aspects']}

⭐ KEY SYNASTRY ASPECTS:
"""
        
        for aspect in synastry['key_aspects'][:10]:  # Show top 10
            planet1, planet2 = aspect['between']
            results += f"   • {planet1.title()} - {planet2.title()}: {aspect['aspect'].title()} ({aspect['angle']:.1f}°)\n"
        
        results += f"\n✨ Analysis complete! {len(synastry['aspects'])} total aspects found."
        
        self.compat_results.insert("1.0", results)
    
    def save_chart(self, format_type):
        """Save chart to file"""
        if not self.current_chart:
            messagebox.showerror("Error", "No chart to save. Please calculate a chart first.")
            return
        
        try:
            # Get file path
            name = self.name_var.get().replace(" ", "_").lower()
            date = self.date_var.get().replace("-", "")
            default_filename = f"{name}_{date}_chart.{format_type}"
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{format_type}",
                filetypes=[(f"{format_type.upper()} files", f"*.{format_type}")],
                initialfile=default_filename
            )
            
            if not file_path:
                return
            
            # Save based on format
            if format_type == "json":
                with open(file_path, 'w') as f:
                    json.dump(self.current_chart, f, indent=2)
            elif format_type == "csv":
                # Create CSV of planetary positions
                with open(file_path, 'w') as f:
                    f.write("Planet,Sign,Degree,Longitude,Retrograde\n")
                    for body_name, body_data in self.current_chart['bodies'].items():
                        retrograde = "Yes" if body_data.get('retrograde', False) else "No"
                        f.write(f"{body_name},{body_data['sign']},{body_data['degree_in_sign']:.2f},{body_data['ecliptic_longitude_deg']:.2f},{retrograde}\n")
            else:  # text
                with open(file_path, 'w') as f:
                    f.write(f"Natal Chart for {self.name_var.get()}\n")
                    f.write(f"Born: {self.date_var.get()} {self.time_var.get()} in {self.timezone_var.get()}\n")
                    f.write(f"Location: {self.latitude_var.get()}°, {self.longitude_var.get()}°\n\n")
                    for body_name, body_data in self.current_chart['bodies'].items():
                        retrograde = " R" if body_data.get('retrograde', False) else ""
                        f.write(f"{body_name.replace('_', ' ').title()}: {body_data['sign']} {body_data['degree_in_sign']:.1f}°{retrograde}\n")
            
            messagebox.showinfo("Success", f"Chart saved to {file_path}")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving chart: {str(e)}")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main entry point for desktop GUI"""
    try:
        app = NatalChartGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Startup Error", f"Error starting GUI: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
