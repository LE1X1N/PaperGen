import logging
import os
from pathlib import Path
from concurrent_log_handler import ConcurrentRotatingFileHandler

from src.config import conf


def setup_logger():
    """
        Initialize the logger for the application.
    """
    log_dir = Path(conf["log"]["base_dir"])
    if not log_dir.exists():
        log_dir.mkdir(exist_ok=True)
        print(f"创建日志路径：{log_dir}") 
    
    # log file 
    logger_file_path = os.path.join(log_dir, conf["log"]["file_name"])

    # init logger
    logger = logging.getLogger(conf["service"]["name"])
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    
    # log config
    service_handler = ConcurrentRotatingFileHandler(
        logger_file_path, maxBytes=conf["log"]["roll_max_bytes"], backupCount=conf["log"]["backup_count"], encoding="utf-8"
    )
    service_handler.setFormatter(logging.Formatter(conf["log"]["format"]))
    logger.addHandler(service_handler)
    return logger_file_path


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
