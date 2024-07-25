"""
Python script for creating and configuring a Flask application.

This file defines the function to create and configure the Flask application,
including setting up routes, logging, and error handlers.

Developer: WangPeifeng
Date: 2024-05-29
"""

from flask import Flask, jsonify
import traceback
from config import Config
from .logger import logger_handler
from .routes import create_routes


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Apply configuration settings from the Config class to the Flask application.
    app.config.from_object(Config)

    create_routes(app)  # Register routes defined in create_routes function

    # Set logging level for the application
    app.logger.setLevel(Config.LOG_LEVEL)
    # Add custom logger handler to Flask application
    app.logger.addHandler(logger_handler)

    @app.errorhandler(Exception)
    def handle_exception(error):
        """
        Error handler for unhandled exceptions.

        Args:
            error (Exception): The exception object.

        Returns:
            tuple: JSON response with an error message and HTTP status code 500.
        """
        traceback_info = traceback.format_exc()  # Get traceback information as a string
        # Log the error traceback
        app.logger.error('An error occurred:\n%s', traceback_info)
        response = {
            'status': 500,
            'message': 'Internal Server Error'
        }  # Create JSON response with error message
        # Return JSON response and HTTP status code 500
        return jsonify(response), 500

    @app.errorhandler(404)
    def page_not_found(error):
        """
        Error handler for 404 Not Found errors.

        Args:
            error: The error object.

        Returns:
            tuple: JSON response with a message indicating the requested URL was not found, and HTTP status code 404.
        """
        response = {
            'status': 404,
            'message': 'The requested URL was not found on the server. If you entered the URL manually, please check your spelling and try again.'
        }
        # Return JSON response and HTTP status code 404
        return jsonify(response), 404

    return app
