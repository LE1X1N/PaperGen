import logging
import os
from concurrent_log_handler import ConcurrentRotatingFileHandler

from src.config import conf


def setup_logger(service_type):
    """Initialize the logger for the application."""
    
    # dir
    work_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))    # file system
    log_dir = os.path.join(work_root_dir, "log")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # log file
    logger_file_name = f"service_{conf['mode']}.log"
    # logger_file_name = f"service.log"
    logger_file_path = os.path.join(log_dir, logger_file_name)

    # init logger
    logger = logging.getLogger(service_type)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    
    # log config
    service_handler = ConcurrentRotatingFileHandler(
        logger_file_path, maxBytes=500 * 1024 * 1024, backupCount=180, encoding="utf-8"
    )
    service_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(processName)s - %(threadName)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s"
        ))
    logger.addHandler(service_handler)
    return logger


def get_logger():
    try:
        logger = logging.getLogger(conf["service_type"])
    except (KeyError, NameError) as e:
        logger = logging.getLogger("fallback_console_logger")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.warning(f"无法获取日志配置: {str(e)}，已切换到控制台输出")    
    return logger
