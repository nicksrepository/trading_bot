# src/utils/logging_utils.py

import os
import sys
import logging

# Add the project root to the Python path
from src.utils.utils import add_project_root_to_path
add_project_root_to_path()

# Now you can import from src
from src.config import LOG_FORMAT, LOG_LEVEL

# ... rest of the file

def setup_logging(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    formatter = logging.Formatter(LOG_FORMAT)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
