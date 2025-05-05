import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name, filename = "app.log"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = RotatingFileHandler(
            os.path.join(log_dir, filename), maxBytes=1_000_000_000, backupCount=3
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
