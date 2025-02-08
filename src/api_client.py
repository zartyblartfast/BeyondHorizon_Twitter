import logging
from curvature_calculator import CurvatureCalculator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

class CurvatureApiClient:
    def __init__(self):
        self.calculator = CurvatureCalculator()
        logger.info("Initialized local curvature calculator")

    def calculate(self, observer_height, distance, refraction_factor, target_height=None):
        """
        Calculate curvature effects using local implementation.
        
        Args:
            observer_height (float): Height of observer in meters
            distance (float): Distance in kilometers
            refraction_factor (float): Refraction factor (e.g., 1.07 for average)
            target_height (float, optional): Height of target in meters
            
        Returns:
            dict: Calculation results
        """
        try:
            # Log calculation request
            logger.info(f"Calculating with parameters:")
            logger.info(f"- Observer Height: {observer_height}m")
            logger.info(f"- Distance: {distance}km")
            logger.info(f"- Refraction: {refraction_factor}")
            if target_height:
                logger.info(f"- Target Height: {target_height}m")
            
            # Perform calculations
            if target_height is not None:
                result = self.calculator.calculate_visibility(
                    observer_height=observer_height,
                    target_height=target_height,
                    distance_km=distance,
                    refraction_factor=refraction_factor
                )
            else:
                # Basic calculations without target
                horizon_distance = self.calculator.calculate_horizon_distance(
                    observer_height, refraction_factor
                )
                hidden_height = self.calculator.calculate_hidden_height(
                    distance, refraction_factor
                )
                geometric_dip = self.calculator.calculate_geometric_dip(
                    observer_height
                )
                result = {
                    "horizon_distance": round(horizon_distance, 3),
                    "hidden_height": round(hidden_height, 3),
                    "geometric_dip": round(geometric_dip, 3)
                }
            
            logger.info(f"Calculation results: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Calculation failed: {str(e)}")
            raise

def test_api():
    """Simple test function to verify calculator functionality"""
    client = CurvatureApiClient()
    try:
        # Test with Mont Blanc example
        result = client.calculate(
            observer_height=4808,  # Mont Blanc height
            distance=100,
            refraction_factor=1.07,
            target_height=2000  # Example target height
        )
        print("\nCalculation Test Results:")
        print("-----------------------")
        print(f"Observer Height: 4808m")
        print(f"Distance: 100km")
        print(f"Refraction: 1.07")
        print(f"Target Height: 2000m")
        print("\nCalculated Values:")
        for key, value in result.items():
            print(f"{key}: {value}")
        return True
    except Exception as e:
        print(f"\nCalculation Test Failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_api()
