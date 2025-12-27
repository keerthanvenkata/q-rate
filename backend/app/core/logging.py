import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import settings

# Create logs directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Formatters
DETAILED_FORMAT = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
)

def get_logger(name: str):
    """
    Returns a configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    
    # Prevent duplicate handlers if get_logger is called multiple times
    if logger.handlers:
        return logger

    # 1. Console Handler (Standard Output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(DETAILED_FORMAT)
    logger.addHandler(console_handler)

    # 2. File Handler (Deep Debug Persistence)
    # Only active if DEBUG is True, or we can make it always active for auditing.
    # User requested "Deep Debug" logging to file.
    if settings.DEBUG:
        file_handler = RotatingFileHandler(
            LOG_DIR / "debug.log", 
            maxBytes=10*1024*1024, # 10MB
            backupCount=5
        )
        file_handler.setFormatter(DETAILED_FORMAT)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    return logger

# Global App Logger
app_logger = get_logger("q-rate")
