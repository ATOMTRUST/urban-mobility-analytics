"""Test the transit vehicle data generator."""

import os
import logging
import sys

# Add project root to path for imports to work
# when running the script directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Import the generator with relative import
import transit_vehicles_generator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run a test of the transit vehicle generator."""
    output_dir = os.path.join(os.getcwd(), "data", "test_output")
    generator = transit_vehicles_generator.TransitVehicleGenerator(output_dir=output_dir)
    
    # Generate 10 steps of data
    steps = generator.generate_data(num_steps=10)
    
    logger.info(f"Successfully generated {steps} steps of transit vehicle data")
    logger.info(f"Output directory: {output_dir}")

if __name__ == "__main__":
    main()