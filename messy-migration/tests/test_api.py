import unittest
import json
from app import app
from app.models.user_repository import UserRepository

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_endpoint(self):
        response = self.app.get('/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'User Management System')

    def test_create_user_success(self):
        test_user = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.app.post('/users',
                               data=json.dumps(test_user),
                               content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['status'], 'success')
        self.assertTrue('id' in data['data'])

    def test_create_user_invalid_data(self):
        test_user = {
            'name': 'T',  # Invalid name (too short)
            'email': 'invalid-email',  # Invalid email
            'password': 'short'  # Invalid password (too short)
        }
        response = self.app.post('/users',
                               data=json.dumps(test_user),
                               content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 'error')

if __name__ == '__main__':
    unittest.main()
