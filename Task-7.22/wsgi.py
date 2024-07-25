"""
WSGI script for running a Flask application.

This script initializes a Flask application using settings from the 'config' module.
It logs information about the application's configuration and runs the Flask app
with specified host, port, and debug mode if executed directly.

Developer: WangPeifeng
Date: 2024-05-29
"""

import config 
from app import create_app  


app = create_app()  # Create the Flask application 


if __name__ == '__main__':
    # If this script is executed directly 

    app.logger.info(f'app run server with debug') 
    app.logger.info(f'app run config={config.Config.NAME}')  # Log an info message showing the current configuration name
    app.logger.info(f'app run port={config.Config.PORT}') 
    app.run(host=config.Config.HOST, port=config.Config.PORT, debug=True)  # Run the Flask app with specified host, port, and debug mode
