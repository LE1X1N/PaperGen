from typing import Dict, List, Optional, Tuple
from dashscope.api_entities.dashscope_response import Role
import logging
import os
import re
from concurrent_log_handler import ConcurrentRotatingFileHandler

History = List[Tuple[str, str]]
Messages = List[Dict[str, str]]

def history_to_messages(history: History, system: str) -> Messages:
    messages = [{"role": Role.SYSTEM, "content": system}]
    for h in history:
        messages.append({"role": Role.USER, "content": h[0]})
        messages.append({"role": Role.ASSISTANT, "content": h[1]})
    return messages

def messages_to_history(messages: Messages) -> Tuple[str, History]:
    assert messages[0]["role"] == Role.SYSTEM
    history = []
    for q, r in zip(messages[1::2], messages[2::2]):
        history.append([q["content"], r["content"]])
    return history


def get_generated_files(text):
    patterns = {
        'html': r'```html\n(.+?)\n```',
        'jsx': r'```jsx\n(.+?)\n```',
        'tsx': r'```tsx\n(.+?)\n```',
    }
    result = {}

    for ext, pattern in patterns.items():
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            content = '\n'.join(matches).strip()
            result[f'index.{ext}'] = content

    if len(result) == 0:
        result["index.html"] = text.strip()
    return result


def setup_logger(service_name):
    """Initialize the logger for the application."""
    
    # dir
    WORK_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))    # file system
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