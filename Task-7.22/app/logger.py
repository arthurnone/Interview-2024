"""
Python script for logging configuration.

This file sets up logging for the application, defining a formatter for log messages,
and configuring a FileHandler to output logs to a file specified in the configuration settings.

Developer: WangPeifeng
Date: 2024-05-28
"""
import logging
import config


# Define a formatter for log messages with date, log level, and message
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a FileHandler to output logs to a file specified in your config
logger_handler = logging.FileHandler(config.Config.LOG_PATH)
# Set the log level from your config
logger_handler.setLevel(config.Config.LOG_LEVEL)
logger_handler.setFormatter(formatter)  # Apply the formatter to the handler
