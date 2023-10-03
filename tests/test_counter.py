"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should return an error if counter is not updated"""
        # Create a counter
        create_result = self.client.post('/counters/foo')
        self.assertEqual(create_result.status_code, status.HTTP_201_CREATED)

        # Initialize the baseline value to 0
        baseline_value = 0

        # Update the counter
        update_result = self.client.put('/counters/foo')
        self.assertEqual(update_result.status_code, status.HTTP_200_OK)

        # Increment the baseline value by 1
        baseline_value += 1

        # Check that the updated counter value is one more than the baseline
        self.assertEqual(update_result.json['foo'], baseline_value)

    def test_read_a_counter(self):
        """It should return an error if it can not get the current counter"""
        # Create a counter
        create_result = self.client.post('/counters/my_counter')
        self.assertEqual(create_result.status_code, status.HTTP_201_CREATED)

        # Read the value of the counter
        read_result = self.client.get('/counters/my_counter')
        self.assertEqual(read_result.status_code, status.HTTP_200_OK)

        # Check that the value of the counter matches the expected initial value (0)
        self.assertEqual(read_result.json['my_counter'], 0)
