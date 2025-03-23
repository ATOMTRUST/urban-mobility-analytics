"""Configuration parameters for data generators."""

import os
from datetime import datetime

# General settings
PROJECT_NAME = "urban-mobility-analytics"
SEED = 42  # For reproducibility
DEFAULT_OUTPUT_DIR = os.path.join(os.getcwd(), "data", "generated")

# Time settings
SIMULATION_START_TIME = datetime(2023, 1, 1, 0, 0, 0)
SIMULATION_TIME_STEP_SECONDS = 30  # Generate data every 30 seconds
SIMULATION_SPEED_FACTOR = 60  # Simulate 60x faster than real-time

# Transit vehicle settings
NUM_VEHICLES = 100
VEHICLE_TYPES = ["bus", "train", "tram"]
VEHICLE_SPEEDS = {
    "bus": {"min": 10, "max": 60},  # km/h
    "train": {"min": 20, "max": 120},
    "tram": {"min": 10, "max": 50}
}
ROUTES = {
    "1": {"name": "Downtown Express", "type": "bus", "stops": ["A1", "A2", "A3", "A4", "A5"]},
    "2": {"name": "Airport Line", "type": "train", "stops": ["B1", "B2", "B3", "B4"]},
    "3": {"name": "University Route", "type": "bus", "stops": ["C1", "C2", "C3", "C4", "C5", "C6"]},
    "4": {"name": "Central Loop", "type": "tram", "stops": ["D1", "D2", "D3", "D4", "D5", "D1"]},
    "5": {"name": "Suburban Express", "type": "train", "stops": ["E1", "E2", "E3"]}
}

# Passenger settings
PASSENGER_VOLUME = {
    "weekday_morning_rush": {"start": "07:00", "end": "09:00", "volume": "high"},
    "weekday_evening_rush": {"start": "16:00", "end": "18:30", "volume": "high"},
    "weekday_daytime": {"start": "09:00", "end": "16:00", "volume": "medium"},
    "weekday_night": {"start": "18:30", "end": "07:00", "volume": "low"},
    "weekend_daytime": {"start": "10:00", "end": "20:00", "volume": "medium"},
    "weekend_night": {"start": "20:00", "end": "10:00", "volume": "low"}
}
PASSENGER_EVENTS_PER_HOUR = {
    "high": 500,
    "medium": 200,
    "low": 50
}

# Weather settings
WEATHER_UPDATE_FREQUENCY_MINUTES = 60
WEATHER_CONDITIONS = ["clear", "cloudy", "rain", "snow", "fog", "storm"]
TEMPERATURE_RANGE = {
    "winter": {"min": -10, "max": 10},
    "spring": {"min": 5, "max": 25},
    "summer": {"min": 15, "max": 35},
    "fall": {"min": 0, "max": 20}
}