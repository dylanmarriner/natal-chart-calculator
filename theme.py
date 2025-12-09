#!/usr/bin/env python3
"""
theme.py
Dylan Custom Sci-fi Theme - Python version for desktop GUI.
Translated from TypeScript theme for use with CustomTkinter.
"""

class DylanCustomTheme:
    """Dylan's Custom Sci-fi Theme System for Desktop GUI"""
    
    # ------------------------------------------------------------------
    # COLOR SYSTEM
    # ------------------------------------------------------------------
    COLORS = {
        # Primary color palette
        'primary': {
            'cyan': '#06b6d4',
            'violet': '#d946ef', 
            'red': '#ef4444',
            'amber': '#f59e0b',
            'green': '#22c55e',
            'rose': '#f43f5e',
        },
        
        # Background colors
        'background': {
            'primary': '#0F172A',      # slate-950
            'secondary': '#1E293B',    # slate-800
            'panel': '#1E293B',        # slate-900
            'glass': '#1E293B',        # slate-900/50
            'overlay': '#000000',      # black/40
            'light': '#000000',        # black/20
        },
        
        # Text colors
        'text': {
            'primary': '#F8FAFC',      # slate-50
            'secondary': '#CBD5E1',    # slate-300
            'tertiary': '#94A3B8',     # slate-400
            'muted': '#64748B',        # slate-500
            'disabled': '#475569',     # slate-600
        },
        
        # Extended color variants
        'cyan': {
            '50': '#F0FDFA', '100': '#CCFBF1', '200': '#99F6E4', '300': '#5EEAD4',
            '400': '#2DD4BF', '500': '#14B8A6', '600': '#0D9488', '700': '#0F766E',
            '800': '#115E59', '900': '#134E4A', '950': '#042F2E',
        },
        
        'violet': {
            '50': '#F5F3FF', '100': '#EDE9FE', '200': '#DDD6FE', '300': '#C4B5FD',
            '400': '#A78BFA', '500': '#8B5CF6', '600': '#7C3AED', '700': '#6D28D9',
            '800': '#5B21B6', '900': '#4C1D95', '950': '#2E1065',
        },
        
        'red': {
            '50': '#FEF2F2', '100': '#FEE2E2', '200': '#FECACA', '300': '#FCA5A5',
            '400': '#F87171', '500': '#EF4444', '600': '#DC2626', '700': '#B91C1C',
            '800': '#991B1B', '900': '#7F1D1D', '950': '#450A0A',
        },
        
        'amber': {
            '50': '#FFFBEB', '100': '#FEF3C7', '200': '#FDE68A', '300': '#FCD34D',
            '400': '#FBBF24', '500': '#F59E0B', '600': '#D97706', '700': '#B45309',
            '800': '#92400E', '900': '#78350F', '950': '#451A03',
        },
        
        'green': {
            '50': '#F0FDF4', '100': '#DCFCE7', '200': '#BBF7D0', '300': '#86EFAC',
            '400': '#4ADE80', '500': '#22C55E', '600': '#16A34A', '700': '#15803D',
            '800': '#166534', '900': '#14532D', '950': '#052E16',
        },
        
        'rose': {
            '50': '#FFF1F2', '100': '#FFE4E6', '200': '#FECDD3', '300': '#FDA4AF',
            '400': '#FB7185', '500': '#F43F5E', '600': '#E11D48', '700': '#BE123C',
            '800': '#9F1239', '900': '#881337', '950': '#4C0519',
        },
    }
    
    # ------------------------------------------------------------------
    # CUSTOMTKINTER THEME CONFIGURATION
    # ------------------------------------------------------------------
    CUSTOMTKINTER_THEME = {
        # Window and frame colors
        "window": {
            "bg_color": COLORS['background']['primary'],
            "fg_color": COLORS['background']['secondary'],
            "border_width": 1,
            "border_color": COLORS['primary']['cyan'],
        },
        
        # Button styling
        "button": {
            "corner_radius": 6,
            "border_width": 1,
            "border_color": COLORS['primary']['cyan'],
            "fg_color": COLORS['background']['secondary'],
            "hover_color": COLORS['cyan']['700'],
            "text_color": COLORS['text']['primary'],
            "text_color_disabled": COLORS['text']['disabled'],
            "font": ("SF Mono", 12, "bold"),
        },
        
        # Entry field styling
        "entry": {
            "corner_radius": 6,
            "border_width": 1,
            "border_color": COLORS['primary']['cyan'],
            "fg_color": COLORS['background']['panel'],
            "text_color": COLORS['text']['primary'],
            "placeholder_text_color": COLORS['text']['muted'],
            "font": ("SF Mono", 12),
        },
        
        # Label styling
        "label": {
            "text_color": COLORS['text']['primary'],
            "font": ("SF Mono", 12),
        },
        
        # Tabview styling
        "tabview": {
            "corner_radius": 6,
            "border_width": 1,
            "border_color": COLORS['primary']['cyan'],
            "fg_color": COLORS['background']['secondary'],
            "text_color": COLORS['text']['primary'],
            "text_color_disabled": COLORS['text']['disabled'],
            "font": ("SF Mono", 12, "bold"),
        },
        
        # Frame styling
        "frame": {
            "corner_radius": 6,
            "border_width": 1,
            "border_color": COLORS['primary']['cyan'],
            "fg_color": COLORS['background']['panel'],
        },
        
        # Scrollbar styling
        "scrollbar": {
            "corner_radius": 6,
            "border_width": 1,
            "border_color": COLORS['primary']['cyan'],
            "fg_color": COLORS['cyan']['600'],
            "button_color": COLORS['cyan']['500'],
            "button_hover_color": COLORS['cyan']['400'],
        },
        
        # Progress bar styling
        "progressbar": {
            "corner_radius": 6,
            "border_width": 1,
            "border_color": COLORS['primary']['cyan'],
            "fg_color": COLORS['cyan']['500'],
            "progress_color": COLORS['primary']['cyan'],
        }
    }
    
    @classmethod
    def get_customtkinter_colors(cls):
        """Get colors formatted for CustomTkinter set_appearance_mode"""
        return {
            "dark-blue": {
                "path": "dark-blue.json",
                "primary": cls.COLORS['primary']['cyan'],
                "secondary": cls.COLORS['primary']['violet'],
                "tertiary": cls.COLORS['primary']['amber'],
            }
        }
    
    @classmethod
    def apply_theme(cls, ctk_instance):
        """Apply Dylan's custom theme to CustomTkinter instance"""
        try:
            # Set dark mode appearance
            ctk_instance.set_appearance_mode("dark")
            
            # Configure custom colors
            ctk_instance.set_default_color_theme(cls.get_customtkinter_colors())
            
            return True
        except Exception as e:
            print(f"Theme application error: {e}")
            return False
    
    @classmethod
    def get_color(cls, color_path: str):
        """Get color by path, e.g., 'primary.cyan' or 'background.primary'"""
        parts = color_path.split('.')
        current = cls.COLORS
        
        for part in parts:
            if part in current:
                current = current[part]
            else:
                return cls.COLORS['primary']['cyan']  # Default fallback
        
        return current if isinstance(current, str) else str(current)
    
    @classmethod
    def create_gradient_colors(cls, base_color: str, steps: int = 5):
        """Create gradient colors for a base color"""
        if base_color not in cls.COLORS['primary']:
            base_color = 'cyan'
        
        base_hex = cls.COLORS['primary'][base_color]
        # Simple gradient simulation by using existing color variants
        color_key = base_color
        if color_key in cls.COLORS:
            return [
                cls.COLORS[color_key]['900'],
                cls.COLORS[color_key]['700'],
                cls.COLORS[color_key]['500'],
                cls.COLORS[color_key]['300'],
                cls.COLORS[color_key]['100'],
            ]
        return [base_hex] * steps

# Export theme instance
theme = DylanCustomTheme()
