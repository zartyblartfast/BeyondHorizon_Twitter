"""
Core calculation module for Beyond Horizon Twitter Bot.
Implements essential curvature calculations focused on tweet-relevant outputs.

Variable naming follows project conventions:
- h1: Observer Height (meters)
- L0: Total Distance (kilometers)
- XZ: Target Height (meters)
- D1: Distance to Horizon (kilometers)
- h2/XC: Hidden Height (meters)
- h3: Visible Height (meters)
- CD: Apparent Visible Height (meters)
"""
import math
import os
import json
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import urllib.parse

# Load environment variables
load_dotenv("config/.env")

class ValidationError(Exception):
    """Custom exception for input validation errors"""
    pass

class APIError(Exception):
    """Custom exception for API-related errors"""
    pass

class CurvatureCalculator:
    # Constants
    EARTH_RADIUS = 6371000  # meters
    
    # Validation limits
    H1_MIN = 2        # Minimum observer height (meters)
    H1_MAX = 9000     # Maximum observer height (meters)
    L0_MIN = 5        # Minimum distance (kilometers)
    L0_MAX = 600      # Maximum distance (kilometers)
    XZ_MAX = 9000     # Maximum target height (meters)
    RF_MIN = 1.00     # Minimum refraction factor
    RF_MAX = 1.25     # Maximum refraction factor
    RF_DEFAULT = 1.07 # Default refraction factor

    def __init__(self, use_api: bool = False):
        """
        Initialize calculator with option to use API.
        
        Args:
            use_api: Whether to use the API for calculations (default False)
        """
        self.use_api = use_api
        if use_api:
            self.api_url = os.getenv("AZURE_FUNCTION_URL", "http://localhost:7071")
            self.api_key = os.getenv("AZURE_FUNCTION_KEY", "")
            
    def calculate_via_api(self, h1: float, L0: float, XZ: Optional[float] = None, 
                         refraction_factor: float = RF_DEFAULT) -> Dict[str, Any]:
        """
        Calculate visibility parameters using the API.
        
        Args:
            h1: Observer height in meters
            L0: Total distance in kilometers
            XZ: Optional target height in meters
            refraction_factor: Refraction factor (default 1.07)
            
        Returns:
            dict: API response with calculation results
            
        Raises:
            APIError: If API request fails
            ValidationError: If input validation fails
        """
        endpoint = f"{self.api_url}/api/calculate"
        
        # Prepare API request payload
        payload = {
            "observerHeight": h1,
            "distance": L0,
            "refractionFactor": refraction_factor,
            "isMetric": True
        }
        if XZ is not None:
            payload["targetHeight"] = XZ
            
        try:
            # Prepare the API key parameter (decode it first as it's already URL encoded)
            params = {"code": urllib.parse.unquote(self.api_key)}
            
            # Make API request with params separate from endpoint
            response = requests.post(endpoint, params=params, json=payload)
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            
            # Convert API response to local format with correct units
            # Note: API returns heights in kilometers, we need meters
            converted = {
                "D1": result["horizon_distance"],  # Already in km
                "dip_angle": result["dip_angle"],  # Degrees, no conversion needed
                "h2": result["hidden_height"] * 1000,  # Convert km to m
                "total_distance": result["total_distance"],  # Already in km
            }
            
            # Optional fields that might be present if target height was provided
            if "visible_target_height" in result:
                converted["h3"] = result["visible_target_height"] * 1000  # Convert km to m
            if "apparent_visible_height" in result:
                converted["CD"] = result["apparent_visible_height"] * 1000  # Convert km to m
            if "target_visible" in result:
                converted["is_visible"] = result["target_visible"]  # Boolean, no conversion
            if "perspective_scaled_height" in result:
                converted["perspective_scaled_height"] = result["perspective_scaled_height"]  # Ratio, no conversion
            
            return converted
            
        except requests.exceptions.ConnectionError:
            raise APIError("Could not connect to API. Check if it's running and URL is correct.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                raise ValidationError(response.json().get("error", "Invalid input"))
            raise APIError(f"API request failed: {str(e)}")
        except Exception as e:
            raise APIError(f"Unexpected error: {str(e)}")

    @staticmethod
    def validate_inputs(h1: float, L0: float, XZ: Optional[float] = None, refraction_factor: float = RF_DEFAULT) -> None:
        """
        Validate all input parameters against defined ranges.
        
        Args:
            h1: Observer height (meters)
            L0: Distance (kilometers)
            XZ: Optional target height (meters)
            refraction_factor: Refraction factor
            
        Raises:
            ValidationError: If any input is outside its valid range
        """
        # Validate observer height (h1)
        if not isinstance(h1, (int, float)) or h1 < CurvatureCalculator.H1_MIN or h1 > CurvatureCalculator.H1_MAX:
            raise ValidationError(
                f"Observer height must be between {CurvatureCalculator.H1_MIN} and {CurvatureCalculator.H1_MAX} meters"
            )
        
        # Validate distance (L0)
        if not isinstance(L0, (int, float)) or L0 < CurvatureCalculator.L0_MIN or L0 > CurvatureCalculator.L0_MAX:
            raise ValidationError(
                f"Distance must be between {CurvatureCalculator.L0_MIN} and {CurvatureCalculator.L0_MAX} kilometers"
            )
        
        # Validate target height (XZ) if provided
        if XZ is not None:
            if not isinstance(XZ, (int, float)) or XZ < 0 or XZ > CurvatureCalculator.XZ_MAX:
                raise ValidationError(
                    f"Target height must be between 0 and {CurvatureCalculator.XZ_MAX} meters"
                )
        
        # Validate refraction factor
        if not isinstance(refraction_factor, (int, float)) or refraction_factor < CurvatureCalculator.RF_MIN or refraction_factor > CurvatureCalculator.RF_MAX:
            raise ValidationError(
                f"Refraction factor must be between {CurvatureCalculator.RF_MIN} and {CurvatureCalculator.RF_MAX}"
            )

    @staticmethod
    def calculate_hidden_height(L0: float, refraction_factor: float = RF_DEFAULT) -> float:
        """
        Calculate hidden height (h2/XC) at distance L0 using spherical geometry.
        Matches the API implementation exactly.
        
        Args:
            L0: Distance in kilometers
            refraction_factor: Refraction factor (default 1.07)
            
        Returns:
            float: Hidden height in meters
        """
        CurvatureCalculator.validate_inputs(h1=CurvatureCalculator.H1_MIN, L0=L0, refraction_factor=refraction_factor)
        
        R = CurvatureCalculator.EARTH_RADIUS * refraction_factor  # Effective radius
        C = 2 * math.pi * R  # Earth's circumference
        distance_meters = L0 * 1000
        
        # Calculate d1 (distance to horizon) - not needed for h2 but used in API
        d1 = math.sqrt(2 * CurvatureCalculator.H1_MIN * R)
        
        # Calculate l2 (remaining distance)
        l2 = distance_meters - d1
        
        # Calculate BOX angle
        BOX_fraction = l2 / C
        BOX_angle = 2 * math.pi * BOX_fraction
        
        # Calculate OC and hidden height (XC)
        OC = R / math.cos(BOX_angle)
        hidden_height = OC - R
        
        return hidden_height

    def calculate_visibility(self, h1: float, L0: float, XZ: Optional[float] = None, 
                           refraction_factor: float = RF_DEFAULT) -> dict:
        """
        Calculate visibility parameters using spherical geometry.
        Matches the API implementation exactly.
        
        Args:
            h1: Observer height in meters
            L0: Total distance in kilometers
            XZ: Optional target height in meters
            refraction_factor: Refraction factor (default 1.07)
            
        Returns:
            dict: Results including:
                - D1: Distance to horizon (km)
                - dip_angle: Horizon dip angle (degrees)
                - h2: Hidden height (m)
                - h3: Visible height (m) - if target height provided
                - CD: Apparent visible height (m) - if target height provided
                - is_visible: Whether target is visible
                - total_distance: Total distance (km)
                - perspective_scaled_height: Height adjusted for perspective (ratio)
        """
        # Try API first if enabled
        if self.use_api:
            try:
                return self.calculate_via_api(h1, L0, XZ, refraction_factor)
            except (APIError, ValidationError) as e:
                # Log the error and fall back to local calculation
                print(f"API calculation failed: {str(e)}. Falling back to local calculation.")
        
        # Validate all inputs
        self.validate_inputs(h1=h1, L0=L0, XZ=XZ, refraction_factor=refraction_factor)
        
        # Calculate using spherical geometry
        R = self.EARTH_RADIUS * refraction_factor  # Effective radius including refraction
        C = 2 * math.pi * R  # Earth's circumference
        distance_meters = L0 * 1000
        
        # Calculate d1 (distance to horizon)
        d1 = math.sqrt(2 * h1 * R)
        D1 = d1 / 1000  # Convert to km
        
        # Calculate geometric dip angle using refracted radius
        effective_radius = self.EARTH_RADIUS * refraction_factor
        dip_angle = math.degrees(math.acos(effective_radius / (effective_radius + h1)))
        
        # Calculate hidden height
        l2 = distance_meters - d1
        BOX_fraction = l2 / C
        BOX_angle = 2 * math.pi * BOX_fraction
        OC = R / math.cos(BOX_angle)
        h2 = OC - R
        
        # Calculate total distance and visible distance
        d2 = R * math.sin(BOX_angle)
        d0 = d1 + d2
        
        # Prepare basic results
        results = {
            "D1": round(D1, 3),
            "dip_angle": round(dip_angle, 3),
            "h2": round(h2, 3),
            "total_distance": L0
        }
        
        # Add target visibility calculations if target height provided
        if XZ is not None:
            # Calculate visible height of target
            h3 = max(0, XZ - h2)
            
            # Calculate apparent height using angle from spherical geometry
            angle = distance_meters / R
            CD = h3 * math.cos(angle)
            
            # Calculate perspective scaled height using pinhole camera model
            perspective_scaled = CD / distance_meters  # Simplified from FOCAL_LENGTH * CD / (distance_meters * FOCAL_LENGTH)
            perspective_scaled = max(0, perspective_scaled)
            
            results.update({
                "h3": round(h3, 3),
                "CD": round(CD, 3),
                "is_visible": h3 > 0,
                "perspective_scaled_height": round(perspective_scaled, 6)
            })
        
        return results

def test_calculations():
    """Run test calculations with validation"""
    calc = CurvatureCalculator()
    
    print("\nTesting Valid Inputs:")
    print("--------------------")
    try:
        # Test case 1: Mont Blanc (valid inputs)
        h1 = 4808   # Observer height (Mont Blanc) in meters
        L0 = 100    # Distance in kilometers
        XZ = 2000   # Target height in meters
        
        print(f"Test 1 - Mont Blanc viewpoint:")
        print(f"Observer Height (h1): {h1}m")
        print(f"Distance (L0): {L0}km")
        print(f"Target Height (XZ): {XZ}m")
        
        results = calc.calculate_visibility(h1=h1, L0=L0, XZ=XZ)
        
        print("\nResults:")
        print(f"Distance to Horizon (D1): {results['D1']}km")
        print(f"Horizon Dip Angle: {results['dip_angle']}°")
        print(f"Hidden Height (h2): {results['h2']}m")
        print(f"Visible Height (h3): {results['h3']}m")
        print(f"Apparent Visible Height (CD): {results['CD']}m")
        print(f"Target Visible: {'Yes' if results['is_visible'] else 'No'}")
        
    except ValidationError as e:
        print(f"Validation Error: {e}")
    
    print("\nTesting Invalid Inputs:")
    print("----------------------")
    
    # Test case 2: Invalid observer height
    try:
        results = calc.calculate_visibility(h1=1, L0=100, XZ=2000)
    except ValidationError as e:
        print(f"Invalid h1 test: {e}")
    
    # Test case 3: Invalid distance
    try:
        results = calc.calculate_visibility(h1=4808, L0=1000, XZ=2000)
    except ValidationError as e:
        print(f"Invalid L0 test: {e}")
    
    # Test case 4: Invalid target height
    try:
        results = calc.calculate_visibility(h1=4808, L0=100, XZ=10000)
    except ValidationError as e:
        print(f"Invalid XZ test: {e}")
    
    # Test case 5: Invalid refraction factor
    try:
        results = calc.calculate_visibility(h1=4808, L0=100, XZ=2000, refraction_factor=1.5)
    except ValidationError as e:
        print(f"Invalid refraction test: {e}")

if __name__ == "__main__":
    test_calculations()
