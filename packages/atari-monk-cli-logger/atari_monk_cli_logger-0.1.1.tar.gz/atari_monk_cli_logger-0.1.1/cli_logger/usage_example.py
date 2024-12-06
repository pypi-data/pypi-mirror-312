# usage_example.py

import logging
from logger import setup_logger, LoggerConfig

# Custom configuration for the logger
custom_config = {
    LoggerConfig.MAIN_LEVEL: logging.DEBUG,
    LoggerConfig.CONSOLE_LEVEL: logging.DEBUG,
    LoggerConfig.FILE_LEVEL: logging.DEBUG,
    LoggerConfig.LOG_TO_FILE_FLAG: True,
    LoggerConfig.LOG_FILE_PATH: 'logs/my_project.log',
    LoggerConfig.USE_ROTATING_FILE: True,
    LoggerConfig.MAX_BYTES: 5 * 1024 * 1024,  # 5 MB
    LoggerConfig.BACKUP_COUNT: 5,
}

# Setup logger with the custom configuration
logger = setup_logger('my_project_logger', custom_config)

# Log messages with various severity levels
logger.debug("This is a debug message.")
logger.info("This is an informational message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical error message.")

# Example of an exception logging
try:
    result = 10 / 0
except ZeroDivisionError as e:
    logger.exception("An exception occurred: %s", e)
