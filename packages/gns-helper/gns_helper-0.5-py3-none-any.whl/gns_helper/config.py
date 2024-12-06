"""
Configuration module for logging.

This module sets up logging configuration for the application. It defines the log level, format, and handlers for both file and console logging.

Logging Configuration:
    - Log Level: DEBUG
    - Log Format: "[%(asctime)s]:[%(levelname)s]: %(message)s", formatted as "%Y-%m-%d %H:%M:%S"
    - File Handler: Logs to "logs.txt" with DEBUG level.
    - Console Handler: Logs to standard output with DEBUG level.
"""
import logging
from sys import stdout


# Logger
log_level = logging.DEBUG
logger = logging.getLogger("main")
logger.setLevel(log_level)

log_format = logging.Formatter(
    "[%(asctime)s]:[%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S"
)

fh = logging.FileHandler("logs.txt")
fh.setLevel(log_level)
fh.setFormatter(log_format)

ch = logging.StreamHandler(stdout)
ch.setLevel(log_level)
ch.setFormatter(log_format)

logger.addHandler(fh)
logger.addHandler(ch)
