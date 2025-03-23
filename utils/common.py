# src/utils/common.py

"""Common utility functions for data generation."""

import os
import json
import random
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_dir(directory):
    """Ensure that a directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")

def save_json(data, file_path):
    """Save data as a JSON file."""
    try:
        directory = os.path.dirname(file_path)
        ensure_dir(directory)
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Data saved to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving JSON data: {e}")
        return False

def get_time_partition(timestamp):
    """Convert a timestamp to a directory partition structure."""
    dt = timestamp if isinstance(timestamp, datetime) else datetime.fromisoformat(timestamp)
    return f"year={dt.year}/month={dt.month:02d}/day={dt.day:02d}/hour={dt.hour:02d}"

def random_float(min_val, max_val, precision=2):
    """Generate a random float between min_val and max_val."""
    return round(random.uniform(min_val, max_val), precision)

def get_simulation_time(start_time, current_step, time_step_seconds):
    """Calculate the current simulation time based on the step."""
    return start_time + timedelta(seconds=current_step * time_step_seconds)

def is_rush_hour(dt):
    """Determine if a given datetime is during rush hour."""
    hour = dt.hour
    is_weekday = dt.weekday() < 5  # Monday-Friday
    
    if is_weekday:
        return (7 <= hour < 9) or (16 <= hour < 19)
    return False