import logging
from logging.handlers import RotatingFileHandler
import os
from src.config import LOG_DIR, LOG_FORMAT, LOG_LEVEL

def setup_logging(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(LOG_LEVEL)

    os.makedirs(LOG_DIR, exist_ok=True)

    handlers = [
        logging.StreamHandler(),
        RotatingFileHandler(
            os.path.join(LOG_DIR, f"{logger_name}.log"),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
    ]

    formatter = logging.Formatter(LOG_FORMAT)
    for handler in handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
