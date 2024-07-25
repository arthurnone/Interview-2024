"""
Python script for configuration settings.

This file defines the Config class with default configuration settings
for an application, including database credentials, logging settings,
and other configuration parameters.

Developer: WangPeifeng
Date: 2024-05-28
"""

import logging

class Config:
    # Default configuration settings
    NAME = "DEFAULT CONFIG"  # Name of the configuration
    SECRET_KEY = 'xxx.wangpeifeng.com'  # Secret key for application security
    HOST = '127.0.0.1'  # Host IP address
    PORT = 8088  # Port number for the application
    DB_NAME = 'xxx'  # Database name for MySQL
    DB_HOST = '127.0.0.1'  # Database host IP address
    DB_PORT = 3306  # Database port number
    DB_USERNAME = 'wangpeifeng'  # Database username
    DB_PASSWORD = '123qwe'  # Database password
    LOG_LEVEL = logging.INFO  # Logging level for application
    LOG_PATH = 'app.log'  # Path to log file

try:
    # Attempt to import and apply local configuration overrides
    from local_config import LocalConfig
    Config.__dict__.update(LocalConfig.__dict__)
    print("Using local configuration.")
except ImportError:
    # If local configuration is not found, fall back to default configuration
    print("No local configuration found, using default configuration.")
