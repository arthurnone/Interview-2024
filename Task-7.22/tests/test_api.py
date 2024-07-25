"""
Python script for unit testing an API.

This file defines a set of unit tests for an API that handles recipes.
It includes tests for various HTTP methods (GET, POST, PATCH, DELETE)
to ensure the API behaves as expected.

Developer: WangPeifeng
Date: 2024-05-29
"""

import json
import unittest
from flask import current_app
from flask_restful import Api
from app import create_app


class BasicsTestCase(unittest.TestCase):
    # Set up the test case environment before each test
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.api = Api(self.app)

    # Tear down the test case environment after each test
    def tearDown(self):
        self.app_context.pop()

    # Test to check if the Flask application instance exists
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    # Test to check the response status code for the root URL
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 404)

    # Test to check the response for a 404 error
    def test_404_response(self):
        response = self.client.get('/')
        data = json.loads(response.data)
        expected_keys = {"message", "status"}
        self.assertEqual(response.status_code, 404)
        self.assertTrue(expected_keys.issubset(data.keys()))

    # Test to check the response for a POST request to the '/recipes' endpoint
    def test_response_post(self):
        # Define the data to be sent in the POST request
        post_data = {
            "title": "Tomato Soup",
            "making_time": "15 min",
            "serves": "5 people",
            "ingredients": "onion, tomato, seasoning, water",
            "cost": "450"
        }
        response = self.client.post(
            '/recipes', json=post_data, content_type='application/json')

        data = json.loads(response.data)

        # Define the expected response data
        expected_data = {
            "message": "Recipe successfully created!",
            "recipe": [
                {
                    "title": "Tomato Soup",
                    "making_time": "15 min",
                    "serves": "5 people",
                    "ingredients": "onion, tomato, seasoning, water",
                    "cost": 450,
                    "created_at": "2016-01-12 14:10:12",
                    "updated_at": "2016-01-12 14:10:12"
                }
            ]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], expected_data["message"])
        self.assertEqual(data["recipe"][0]["title"],
                         expected_data["recipe"][0]["title"])
        self.assertEqual(data["recipe"][0]["making_time"],
                         expected_data["recipe"][0]["making_time"])
        self.assertEqual(data["recipe"][0]["serves"],
                         expected_data["recipe"][0]["serves"])
        self.assertEqual(data["recipe"][0]["ingredients"],
                         expected_data["recipe"][0]["ingredients"])
        self.assertEqual(data["recipe"][0]["cost"],
                         expected_data["recipe"][0]["cost"])

    # Test to check the response for a GET request to the '/recipes' endpoint
    def test_response_get(self):
        response = self.client.get('/recipes')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("recipes" in data)
        self.assertIsInstance(data["recipes"], list)

    # Test to check the response for a GET request to the '/recipes/<id>' endpoint
    def test_response_get_id(self):
        response = self.client.get('/recipes/1')

        # Define the expected response data
        expected_data = {
            "message": "Recipe details by id",
            "recipe": [
                {
                    "id": 1,
                    "title": "Chicken Curry",
                    "making_time": "45 min",
                    "serves": "4 people",
                    "ingredients": "onion, chicken, seasoning",
                    "cost": 1000
                }
            ]
        }

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], expected_data["message"])
        self.assertEqual(data["recipe"][0]["id"],
                         expected_data["recipe"][0]["id"])
        self.assertEqual(data["recipe"][0]["title"],
                         expected_data["recipe"][0]["title"])
        self.assertEqual(data["recipe"][0]["making_time"],
                         expected_data["recipe"][0]["making_time"])
        self.assertEqual(data["recipe"][0]["serves"],
                         expected_data["recipe"][0]["serves"])
        self.assertEqual(data["recipe"][0]["ingredients"],
                         expected_data["recipe"][0]["ingredients"])
        self.assertEqual(data["recipe"][0]["cost"],
                         expected_data["recipe"][0]["cost"])

    # Test to check the response for a PATCH request to the '/recipes/<id>' endpoint
    def test_response_patch(self):
        # Define the data to be sent in the PATCH request
        post_data = {
            "title": "Tomato Soup",
            "making_time": "15 min",
            "serves": "5 people",
            "ingredients": "onion, tomato, seasoning, water",
            "cost": "450"
        }
        response = self.client.patch(
            '/recipes/2', json=post_data, content_type='application/json')

        data = json.loads(response.data)

        # Define the expected response data
        expected_data = {
            "message": "Recipe successfully updated!",
            "recipe": [
                {
                    "title": "Tomato Soup",
                    "making_time": "15 min",
                    "serves": "5 people",
                    "ingredients": "onion, tomato, seasoning, water",
                    "cost": "450"
                }
            ]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], expected_data["message"])
        self.assertEqual(data["recipe"][0]["title"],
                         expected_data["recipe"][0]["title"])
        self.assertEqual(data["recipe"][0]["making_time"],
                         expected_data["recipe"][0]["making_time"])
        self.assertEqual(data["recipe"][0]["serves"],
                         expected_data["recipe"][0]["serves"])
        self.assertEqual(data["recipe"][0]["ingredients"],
                         expected_data["recipe"][0]["ingredients"])
        self.assertEqual(data["recipe"][0]["cost"],
                         expected_data["recipe"][0]["cost"])

    # Test to check the response for a DELETE request to the '/recipes/<id>' endpoint
    def test_response_delete(self):
        response = self.client.delete('/recipes/3')

        data = json.loads(response.data)
        expected_data = {"message": "Recipe successfully removed!"}

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], expected_data["message"])


if __name__ == '__main__':
    unittest.main()
