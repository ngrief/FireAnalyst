"""
Configuration parameters for FireAnalyst project.

This module centralizes all configuration settings, file paths, and analysis parameters
to ensure reproducibility and easy modification of analysis parameters.
"""

from pathlib import Path
from typing import Dict, List

# Project directory structure
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "Resources"
OUTPUT_DIR = PROJECT_ROOT / "output"
DOCS_DIR = PROJECT_ROOT / "docs"

# Data file paths
RAW_DATA_PATH = DATA_DIR / "California_Fire_Perimeters_(all).csv"
CLEANED_DATA_PATH = DATA_DIR / "cleaned_fire_data.csv"

# Ensure output directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
(OUTPUT_DIR / "figures").mkdir(exist_ok=True)
(OUTPUT_DIR / "tables").mkdir(exist_ok=True)

# Data validation parameters
VALIDATION_CONFIG = {
    "max_containment_hours": 8760,  # 1 year in hours
    "outlier_iqr_multiplier": 3.0,   # For IQR outlier detection
    "min_year": 1850,                 # Minimum valid year
    "max_year": 2025,                 # Maximum valid year
}

# Column mappings
CONTAINMENT_METHOD_MAPPING: Dict[int, str] = {
    1: "Direct Attack (Hand Crews & Tools)",
    2: "Indirect Attack (Firebreaks & Barriers)",
    3: "Aerial Suppression (Planes & Helicopters)",
    4: "Backburning (Controlled Burns)",
    5: "Fireline Construction (Bulldozers & Trenching)",
    6: "Natural Barriers (Using Terrain Features)",
    7: "Mop-up (Extinguishing Hot Spots)",
    8: "Fire Shelter Deployment (Emergency Only)"
}

FIRE_CAUSE_MAPPING: Dict[int, str] = {
    1: "Lightning",
    2: "Equipment Use",
    3: "Smoking",
    4: "Campfire",
    5: "Debris Burning",
    6: "Railroad",
    7: "Arson",
    8: "Children",
    9: "Miscellaneous",
    10: "Fireworks",
    11: "Powerline",
    12: "Structure",
    13: "Escaped Prescribed Burn",
    14: "Unknown",
    15: "Vehicle",
    16: "Reburn",
    17: "Playing with Fire",
    18: "Miscellaneous Human Causes",
    19: "Other"
}

# Columns to drop during cleaning
COLUMNS_TO_DROP: List[str] = [
    'COMMENTS',
    'COMPLEX_NAME',
    'IRWINID',
    'COMPLEX_ID',
    'FIRE_NUM'
]

# Essential columns that must be present
ESSENTIAL_COLUMNS: List[str] = [
    'YEAR_',
    'GIS_ACRES',
    'ALARM_DATE',
    'CONT_DATE'
]

# Visualization settings
VIZ_CONFIG = {
    "figure_dpi": 300,
    "figure_format": "png",
    "default_figsize": (14, 8),
    "color_palette": "Set2",
    "font_size": {
        "title": 16,
        "label": 14,
        "tick": 12
    }
}

# Statistical analysis settings
STATS_CONFIG = {
    "confidence_level": 0.95,
    "significance_threshold": 0.05,
    "random_seed": 42
}