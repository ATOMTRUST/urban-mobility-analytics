"""Generate simulated transit vehicle data."""

import os
import uuid
import random
import logging
from datetime import datetime
import math

# Import configuration with relative imports
import config
from utils import common

# Set random seed for reproducibility
random.seed(config.SEED)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TransitVehicleGenerator:
    """Generate simulated transit vehicle data."""
    
    def __init__(self, output_dir=config.DEFAULT_OUTPUT_DIR):
        """Initialize the generator."""
        self.output_dir = output_dir
        self.vehicles = self._initialize_vehicles()
        self.current_step = 0
        logger.info(f"Initialized {len(self.vehicles)} simulated vehicles")
    
    def _initialize_vehicles(self):
        """Create initial set of vehicles with routes."""
        vehicles = []
        
        for i in range(config.NUM_VEHICLES):
            # Select a random route
            route_id = random.choice(list(config.ROUTES.keys()))
            route = config.ROUTES[route_id]
            
            # Create vehicle with matching type for the route
            vehicle = {
                "vehicle_id": f"V{i:04d}",
                "vehicle_type": route["type"],
                "route_id": route_id,
                "status": "in_service",
                # Start at a random position in the route
                "current_stop_index": random.randint(0, len(route["stops"]) - 1),
                "next_stop": None,  # Will be set during simulation
                "direction": 1,  # 1 for forward, -1 for backward
                "delay": 0,  # No delay initially
                # Random position near the route
                "latitude": 40.7128 + common.random_float(-0.1, 0.1, 6),  # Around NYC
                "longitude": -74.0060 + common.random_float(-0.1, 0.1, 6),
                "speed": 0,
                "bearing": random.randint(0, 359),
                "occupancy_status": random.randint(0, 4)
            }
            
            # Set next stop
            route_stops = route["stops"]
            current_idx = vehicle["current_stop_index"]
            next_idx = (current_idx + vehicle["direction"]) % len(route_stops)
            vehicle["next_stop"] = route_stops[next_idx]
            
            vehicles.append(vehicle)
        
        return vehicles
    
    def _update_vehicle_positions(self, simulation_time):
        """Update positions of all vehicles based on the current time."""
        for vehicle in self.vehicles:
            route = config.ROUTES[vehicle["route_id"]]
            route_stops = route["stops"]
            
            # Determine if the vehicle is at a stop
            at_stop = random.random() < 0.1  # 10% chance to be at a stop
            
            if at_stop:
                # Update occupancy at stops
                old_occupancy = vehicle["occupancy_status"]
                if common.is_rush_hour(simulation_time):
                    # More likely to increase during rush hour
                    change = random.choices([-1, 0, 1, 2], weights=[0.1, 0.2, 0.5, 0.2])[0]
                else:
                    change = random.choices([-1, 0, 1], weights=[0.4, 0.4, 0.2])[0]
                
                new_occupancy = max(0, min(4, old_occupancy + change))
                vehicle["occupancy_status"] = new_occupancy
                
                # Set speed to 0 when at stop
                vehicle["speed"] = 0
                
                # Update next stop
                current_idx = route_stops.index(vehicle["next_stop"])
                
                # If at the end of route, reverse direction
                if current_idx == 0 and vehicle["direction"] == -1:
                    vehicle["direction"] = 1
                elif current_idx == len(route_stops) - 1 and vehicle["direction"] == 1:
                    vehicle["direction"] = -1
                
                next_idx = (current_idx + vehicle["direction"]) % len(route_stops)
                vehicle["next_stop"] = route_stops[next_idx]
                
                # Add random delay
                if random.random() < 0.2:  # 20% chance for delay
                    vehicle["delay"] += random.randint(0, 120)  # 0-2 minutes delay
                else:
                    # Gradually reduce delay if possible
                    vehicle["delay"] = max(0, vehicle["delay"] - random.randint(0, 30))
            
            else:
                # Vehicle is moving
                speed_range = config.VEHICLE_SPEEDS[vehicle["vehicle_type"]]
                vehicle["speed"] = common.random_float(speed_range["min"], speed_range["max"])
                
                # Update position (simplified - just random movement)
                move_factor = vehicle["speed"] / 1000  # Convert to degrees
                vehicle["latitude"] += common.random_float(-move_factor, move_factor, 6)
                vehicle["longitude"] += common.random_float(-move_factor, move_factor, 6)
                
                # Update bearing (direction)
                vehicle["bearing"] = (vehicle["bearing"] + random.randint(-20, 20)) % 360
    
    def generate_data(self, num_steps=10):
        """Generate vehicle data for a number of simulation steps."""
        for step in range(num_steps):
            self.current_step += 1
            simulation_time = common.get_simulation_time(
                config.SIMULATION_START_TIME, 
                self.current_step, 
                config.SIMULATION_TIME_STEP_SECONDS
            )
            
            # Update vehicle states
            self._update_vehicle_positions(simulation_time)
            
            # Create records for this timestep
            records = []
            for vehicle in self.vehicles:
                record = vehicle.copy()
                record["timestamp"] = simulation_time.isoformat()
                record["event_id"] = str(uuid.uuid4())
                records.append(record)
            
            # Save to file
            timestamp_str = simulation_time.strftime("%Y%m%d_%H%M%S")
            partition_path = common.get_time_partition(simulation_time)
            file_path = os.path.join(
                self.output_dir, 
                "transit_vehicles",
                partition_path,
                f"vehicles_{timestamp_str}.json"
            )
            
            common.save_json(records, file_path)
            
            logger.info(f"Generated data for {len(records)} vehicles at step {self.current_step}")
        
        return self.current_step