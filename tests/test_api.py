# tests/test_api.py (updated)
import unittest
import requests 
import json
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.models import load_model

class TestMLAPI(unittest.TestCase):
    
    def setUp(self):
        # Create test app
        self.app = create_app({
            'TESTING': True,
            'API_KEY': 'test-api-key'
        })
        self.client = self.app.test_client()
        self.headers = {'X-API-KEY': 'test-api-key'}
    
    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.get_json())
    
    def test_prediction_valid(self):
        data = {'features': [5.1, 3.5, 1.4, 0.2]}
        response = self.client.post(
            '/predict', 
            json=data, 
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('prediction', json_data)
        self.assertIn('confidence', json_data)
    
    # ... other test methods

if __name__ == '__main__':
    unittest.main()