import unittest
import json
from app import app

class BankingAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_loan_user_not_found(self):
        response = self.app.post('/loan', json={"UserName": "NonExistentUser"})
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"not registered", response.data)

    def test_loan_missing_username(self):
        response = self.app.post('/loan', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing UserName", response.data)

    def test_update_no_userid(self):
        response = self.app.put('/update', json={"PAN": "NEWPAN123"})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing UserID", response.data)

    def test_update_no_pan_tan(self):
        response = self.app.put('/update', json={"UserID": "U001"})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"No PAN or TAN", response.data)

if __name__ == '__main__':
    unittest.main()
