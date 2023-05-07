import logging
from logging import Logger
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(app_name: str) -> Logger:
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)

    # Add a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(console_handler)

    # Add a file handler with log rotation
    file_handler = RotatingFileHandler("app.log", maxBytes=1024 * 1024, backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    return logger

log = setup_logger("AIPlaylist")