# src/test_generator.py

"""Test the transit vehicle data generator."""

import os
import logging
from data_generators.transit_vehicle_generator import TransitVehicleGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run a test of the transit vehicle generator."""
    output_dir = os.path.join(os.getcwd(), "data", "test_output")
    generator = TransitVehicleGenerator(output_dir=output_dir)
    
    # Generate 10 steps of data
    steps = generator.generate_data(num_steps=10)
    
    logger.info(f"Successfully generated {steps} steps of transit vehicle data")
    logger.info(f"Output directory: {output_dir}")

if __name__ == "__main__":
    main()