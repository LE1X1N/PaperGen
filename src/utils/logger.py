import logging
import os
from concurrent_log_handler import ConcurrentRotatingFileHandler

from config import conf


def setup_logger(service_name):
    """Initialize the logger for the application."""
    
    # dir
    WORK_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))    # file system
    LOG_DIR = os.path.join(WORK_ROOT_DIR, "log")
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # log file
    logger_file_name = "service.log"
    logger_file_path = os.path.join(LOG_DIR, logger_file_name)
    
    # basic logging
    BASE_LEVEL = logging.DEBUG
    BASE_FORMATTER = logging.Formatter(
        "%(asctime)s - %(name)s - %(threadName)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s"
    )
    
    # init logger
    logger = logging.getLogger(service_name)
    logger.setLevel(BASE_LEVEL)
    logger.propagate = False
    
    # log config
    service_handler = ConcurrentRotatingFileHandler(
        logger_file_path, maxBytes=500 * 1024 * 1024, backupCount=180, encoding="utf-8"
    )
    service_handler.setFormatter(BASE_FORMATTER)
    logger.addHandler(service_handler)
    return logger


def get_logger():
    logger = logging.getLogger(conf["service_name"])
    return logger