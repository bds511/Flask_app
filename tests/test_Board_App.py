import os
import Board_App
import unittest
import tempfile
import Board_App.user as BA


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        BA.app.post('/login', data=dict(id=1234, password=1234),follow_redirects=True)

    def tearDown(self):
        BA.app.get('/logout')

if __name__ == '__main__':
    unittest.main()