import logging
import os
from concurrent_log_handler import ConcurrentRotatingFileHandler

from src.config import conf


def setup_logger():
    """Initialize the logger for the application."""
    
    # dir
    work_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))    # file system
    log_dir = os.path.join(work_root_dir, conf["service"]["log"]["base_dir"])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # log file
    logger_file_name = conf["service"]["log"]["file_name"]
    logger_file_path = os.path.join(log_dir, logger_file_name)

    # init logger
    logger = logging.getLogger(conf["service"]["name"])
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    
    # log config
    service_handler = ConcurrentRotatingFileHandler(
        logger_file_path, maxBytes=conf["service"]["log"]["roll_max_bytes"], backupCount=conf["service"]["log"]["backup_count"], encoding="utf-8"
    )
    service_handler.setFormatter(logging.Formatter(conf["service"]["log"]["format"]))
    logger.addHandler(service_handler)
    return logger


def get_logger():
    try:
        logger = logging.getLogger(conf["service"]["name"])
    except (KeyError, NameError) as e:
        logger = logging.getLogger("fallback_console_logger")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.warning(f"无法获取日志配置: {str(e)}，已切换到控制台输出")    
    return logger
