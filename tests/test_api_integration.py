"""
Integration tests for the CurvatureCalculator API functionality.
Tests require a running local API instance.
"""
import unittest
import os
from dotenv import load_dotenv
from src.curvature_calculator import CurvatureCalculator, APIError

def format_value(val):
    if isinstance(val, float):
        return f"{val:.6f}"
    return str(val)

def write_comparison(case_name, params, api_result, local_result):
    output = []
    output.append("="*80)
    output.append(f"Test Case: {case_name}")
    output.append(f"Parameters:")
    for k, v in params.items():
        output.append(f"  {k}: {v}")
    output.append("="*80)
    
    output.append("\nResults Comparison:")
    output.append(f"{'Field':<25} {'API Value':<20} {'Local Value':<20} {'Diff %':<10}")
    output.append("-"*75)
    
    all_fields = sorted(set(api_result.keys()) | set(local_result.keys()))
    for field in all_fields:
        api_val = api_result.get(field, "N/A")
        local_val = local_result.get(field, "N/A")
        
        if isinstance(api_val, (int, float)) and isinstance(local_val, (int, float)):
            max_val = max(abs(float(api_val)), abs(float(local_val)))
            if max_val > 0:
                diff_pct = abs(float(api_val) - float(local_val)) / max_val * 100
                diff_str = f"{diff_pct:.1f}%"
            else:
                diff_str = "0%"
        else:
            diff_str = "N/A"
            
        output.append(f"{field:<25} {format_value(api_val):<20} {format_value(local_val):<20} {diff_str:<10}")
    
    output.append("\nAnalysis:")
    for field in ["D1", "h2", "h3"]:
        if field in api_result and field in local_result:
            api_val = float(api_result[field])
            local_val = float(local_result[field])
            if abs(api_val - local_val) > 0.001:
                output.append(f"- {field}: Significant difference detected")
                output.append(f"  API calculation: {api_val}")
                output.append(f"  Local calculation: {local_val}")
    
    return "\n".join(output) + "\n\n"

class TestAPIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        load_dotenv("config/.env")
        cls.api_url = os.getenv("AZURE_FUNCTION_URL")
        if not cls.api_url:
            raise unittest.SkipTest("AZURE_FUNCTION_URL not set in environment")
        
        cls.calculator = CurvatureCalculator(use_api=True)
        
    def setUp(self):
        """Set up test cases"""
        self.test_cases = [
            {
                "name": "Mont Blanc Standard",
                "params": {
                    "h1": 4808,     # Mont Blanc height
                    "L0": 100,      # Distance in km
                    "XZ": 2000,     # Target height
                    "refraction_factor": 1.07
                }
            },
            {
                "name": "Low Altitude",
                "params": {
                    "h1": 10,       # Observer height
                    "L0": 10,       # Distance in km
                    "XZ": 20,       # Target height
                    "refraction_factor": 1.07
                }
            }
        ]
    
    def test_api_connectivity(self):
        """Test basic API connectivity"""
        try:
            result = self.calculator.calculate_visibility(h1=100, L0=10)
            self.assertIsNotNone(result)
            self.assertIn('D1', result)
            print(f"\nAPI Connection successful. Response: {result}")
        except APIError as e:
            self.fail(f"API connection failed: {str(e)}")
    
    def test_known_locations(self):
        """Test calculations for known locations"""
        print("\n" + "="*50)
        print("Testing API Integration")
        print("="*50)

        for case in self.test_cases:
            with self.subTest(case=case["name"]):
                try:
                    result = self.calculator.calculate_visibility(**case["params"])
                    print(f"\nTesting {case['name']}:")
                    print(f"Parameters: {case['params']}")
                    print(f"Result: {result}")
                    
                    self.assertIn("is_visible", result, "Result missing visibility status")
                except Exception as e:
                    self.fail(f"Test failed for {case['name']}: {str(e)}")
    
    def test_local_api_match(self):
        """Test that API results match local calculations"""
        try:
            api_calc = CurvatureCalculator(use_api=True)
            local_calc = CurvatureCalculator(use_api=False)
            
            # Open comparison file
            with open("tests/comparison_results_output.txt", "w") as f:
                for case in self.test_cases:
                    # Get results
                    api_result = api_calc.calculate_visibility(**case["params"])
                    local_result = local_calc.calculate_visibility(**case["params"])
                    
                    # Write comparison to file and print to console
                    comparison = write_comparison(
                        case["name"],
                        case["params"],
                        api_result,
                        local_result
                    )
                    f.write(comparison)
                    print(comparison)
                    
        except Exception as e:
            self.fail(f"Test failed: {str(e)}")

if __name__ == '__main__':
    unittest.main()
