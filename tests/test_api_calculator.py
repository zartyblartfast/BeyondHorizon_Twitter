"""
Unit tests for the CurvatureCalculator API functionality.
"""
import unittest
from unittest.mock import patch, MagicMock
import json
import os
import requests
from src.curvature_calculator import CurvatureCalculator, APIError, ValidationError

class TestCurvatureCalculatorAPI(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        # Ensure environment variables are set for testing
        os.environ.setdefault('AZURE_FUNCTION_URL', 'http://localhost:7071')
        os.environ.setdefault('AZURE_FUNCTION_KEY', '')
        
        self.calculator = CurvatureCalculator(use_api=True)
        self.test_params = {
            "h1": 4808,    # Mont Blanc height
            "L0": 100,     # Distance in km
            "XZ": 2000,    # Target height
            "refraction_factor": 1.07
        }
        
        # Example API response based on actual Azure Function
        self.mock_api_response = {
            "hidden_height": 1.786,
            "horizon_distance": 256.031,
            "total_distance": 100.0,
            "dip_angle": 2.23,
            "is_metric": True,
            "visible_target_height": 0.214,
            "apparent_visible_height": 0.214,
            "perspective_scaled_height": 0.002,
            "target_visible": True
        }

    @patch('requests.post')
    def test_successful_api_call(self, mock_post):
        """Test successful API calculation"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_api_response
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Call API
        result = self.calculator.calculate_via_api(**self.test_params)

        # Verify API was called with correct parameters
        mock_post.assert_called_once()
        call_args = mock_post.call_args[1]['json']
        self.assertEqual(call_args['observerHeight'], self.test_params['h1'])
        self.assertEqual(call_args['distance'], self.test_params['L0'])
        self.assertEqual(call_args['targetHeight'], self.test_params['XZ'])
        self.assertEqual(call_args['refractionFactor'], self.test_params['refraction_factor'])
        self.assertTrue(call_args['isMetric'])

        # Verify response format
        self.assertIn('D1', result)
        self.assertIn('dip_angle', result)
        self.assertIn('h2', result)
        self.assertIn('h3', result)
        self.assertIn('CD', result)
        self.assertIn('is_visible', result)
        self.assertIn('total_distance', result)
        self.assertIn('perspective_scaled_height', result)

    @patch('requests.post')
    def test_api_validation_error(self, mock_post):
        """Test API validation error handling"""
        # Mock API validation error response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": "Observer height must be at least 2.0 meters"
        }
        mock_post.return_value = mock_response
        
        # Create HTTPError with mock response
        http_error = requests.exceptions.HTTPError(response=mock_response)
        mock_response.raise_for_status.side_effect = http_error

        # Test with invalid height
        invalid_params = self.test_params.copy()
        invalid_params['h1'] = 1  # Below minimum height

        with self.assertRaises(ValidationError) as context:
            self.calculator.calculate_via_api(**invalid_params)
        
        self.assertIn("Observer height", str(context.exception))

    @patch('requests.post')
    def test_api_connection_error(self, mock_post):
        """Test API connection error handling"""
        # Mock connection error
        mock_post.side_effect = requests.exceptions.ConnectionError()

        with self.assertRaises(APIError) as context:
            self.calculator.calculate_via_api(**self.test_params)
        
        self.assertIn("Could not connect to API", str(context.exception))

    def test_fallback_to_local(self):
        """Test fallback to local calculation when API fails"""
        # Create calculators
        calculator = CurvatureCalculator(use_api=True)
        local_calculator = CurvatureCalculator(use_api=False)
        
        # Calculate using local method first
        local_result = local_calculator.calculate_visibility(**self.test_params)
        
        # Calculate with API (which should fail and fall back to local)
        with patch('requests.post', side_effect=requests.exceptions.ConnectionError()):
            api_result = calculator.calculate_visibility(**self.test_params)
        
        # Results should match local calculation
        self.assertEqual(local_result['D1'], api_result['D1'])
        self.assertEqual(local_result['dip_angle'], api_result['dip_angle'])
        self.assertEqual(local_result['h2'], api_result['h2'])
        if 'h3' in local_result:
            self.assertEqual(local_result['h3'], api_result['h3'])
        if 'CD' in local_result:
            self.assertEqual(local_result['CD'], api_result['CD'])
        self.assertEqual(local_result['is_visible'], api_result['is_visible'])

    def test_api_url_from_env(self):
        """Test API URL is correctly loaded from environment"""
        # Test default URL
        calculator = CurvatureCalculator(use_api=True)
        self.assertEqual(calculator.api_url, "http://localhost:7071")
        
        # Test custom URL from environment
        with patch.dict(os.environ, {'AZURE_FUNCTION_URL': 'https://custom-url.com'}):
            calculator = CurvatureCalculator(use_api=True)
            self.assertEqual(calculator.api_url, "https://custom-url.com")

if __name__ == '__main__':
    unittest.main()
