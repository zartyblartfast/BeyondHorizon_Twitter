"""
Client for interacting with the Azure Functions LoS Calculator API.
"""
import os
import logging
import requests
from typing import Dict, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CalculationInput:
    """Input parameters for LoS calculations (all in metric units)"""
    observer_height: float  # h1 (meters)
    distance: float        # L0 (kilometers)
    refraction: float     # default 1.07
    target_height: Optional[float] = None  # XZ (meters)

@dataclass
class CalculationResults:
    """Results from LoS calculations (all in metric units)"""
    # Basic results (always present)
    distance_to_horizon: float  # D1 (kilometers)
    horizon_dip_angle: float   # degrees
    hidden_height: float       # h2/XC (meters)
    
    # Additional results (when target height provided)
    visible_height: Optional[float] = None         # h3 (meters)
    apparent_visible_height: Optional[float] = None  # CD (meters)
    perspective_height: Optional[float] = None      # scaled apparent height (meters)

class CalculatorClient:
    """Client for Azure Functions LoS Calculator API (using metric units)"""
    
    def __init__(self):
        """Initialize the calculator client"""
        self.api_url = os.getenv('AZURE_FUNCTION_URL')
        self.api_key = os.getenv('AZURE_FUNCTION_KEY')
        
        if not self.api_url or not self.api_key:
            logger.warning("Azure Functions credentials not found in environment variables")
    
    def calculate(self, input_data: CalculationInput) -> CalculationResults:
        """
        Call Azure Functions API to perform LoS calculations
        All values are in metric units (meters for heights, kilometers for distances)
        
        Args:
            input_data: CalculationInput object with required parameters
            
        Returns:
            CalculationResults object containing all calculated values
            
        Raises:
            requests.RequestException: If API call fails
            ValueError: If required parameters are missing or invalid
        """
        if not self.api_url or not self.api_key:
            raise ValueError("Azure Functions credentials not configured")
            
        # Prepare request payload
        payload = {
            "observer_height": input_data.observer_height,  # meters
            "distance": input_data.distance,                # kilometers
            "refraction": input_data.refraction,
            "units": "metric"  # explicitly request metric units
        }
        
        if input_data.target_height is not None:
            payload["target_height"] = input_data.target_height  # meters
            
        # Add authentication
        headers = {
            "x-functions-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            
            # Create results object
            results = CalculationResults(
                distance_to_horizon=data["distance_to_horizon"],  # km
                horizon_dip_angle=data["horizon_dip_angle"],      # degrees
                hidden_height=data["hidden_height"]               # meters
            )
            
            # Add optional results if target height was provided
            if input_data.target_height is not None:
                results.visible_height = data.get("visible_height")           # meters
                results.apparent_visible_height = data.get("apparent_visible_height")  # meters
                results.perspective_height = data.get("perspective_height")    # meters
                
            return results
            
        except requests.RequestException as e:
            logger.error(f"API call failed: {str(e)}")
            raise
            
    def format_results(self, results: CalculationResults, with_target: bool = False) -> str:
        """
        Format calculation results for tweet content, using metric units
        
        Args:
            results: CalculationResults object
            with_target: Whether target height was provided
            
        Returns:
            Formatted string for tweet
        """
        lines = [
            f"📏 Horizon Distance: {results.distance_to_horizon:.1f}km",
            f"📐 Horizon Dip: {results.horizon_dip_angle:.2f}°",
            f"📊 Hidden Height: {results.hidden_height:.0f}m"  # rounded to whole meters
        ]
        
        if with_target and results.visible_height is not None:
            lines.extend([
                f"👁️ Visible Height: {results.visible_height:.0f}m",  # rounded to whole meters
                f"🔭 Apparent Height: {results.apparent_visible_height:.0f}m"  # rounded to whole meters
            ])
            
        return "\n".join(lines)
