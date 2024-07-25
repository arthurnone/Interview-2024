"""
Python script for database connection management.

This file defines the Database class as a singleton to manage database connections,
including methods for connecting to the database and checking the connection status.

Developer: WangPeifeng
Date: 2024-05-28
"""

import pymysql
from flask import current_app
from pymysql.err import OperationalError


class Database:
    _instance = None  # Class variable to hold the singleton instance of Database class

    def __new__(cls, *args, **kwargs):
        if not cls._instance:  # Check if an instance of the class already exists
            # Create a new instance using the superclass's __new__ method
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
            cls._instance.connection = None  # Initialize connection attribute to None
        return cls._instance  # Return the singleton instance of the class

    def connect(self):
        # Establish a new database connection if not already connected or if connection is not alive
        if not self.connection or not self._is_connection_alive():
            self.connection = pymysql.connect(
                # Database host address from Flask app config
                host=current_app.config['DB_HOST'],
                # Database username from Flask app config
                user=current_app.config['DB_USERNAME'],
                # Database password from Flask app config
                password=current_app.config['DB_PASSWORD'],
                # Database name from Flask app config
                database=current_app.config['DB_NAME'],
                # Database port number from Flask app config
                port=current_app.config['DB_PORT']
            )
        return self.connection  # Return the database connection object

    def _is_connection_alive(self):
        try:
            with self.connection.cursor() as cursor:
                # Execute a test query to check if connection is alive
                cursor.execute('SELECT 1')
            # Return True if query executed successfully (connection is alive)
            return True
        except (AttributeError, OperationalError):
            # Return False if AttributeError or OperationalError occurs (connection is not alive)
            return False

    def get_cursor(self):
        connection = self.connect()  # Ensure a connection is established
        return connection.cursor()  # Return a cursor object for executing queries


# Create a singleton instance of the Database class
db = Database()
