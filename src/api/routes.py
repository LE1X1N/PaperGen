import threading
from flask import Blueprint, request, jsonify
import time
import uuid
import os

from config import SCREENSHOT_DIR
from src.core.task_manager import TaskManager
from src.core.upload_manager import UploadManager
from src.utils import get_logger

logger = get_logger()
api_bp = Blueprint('v1', __name__)

task_manager = TaskManager()
upload_manager = UploadManager()


def task_handler(data, request_id):
    results = task_manager.process_tasks(data, request_id)
    results = upload_manager.upload_files(results)


@api_bp.route('/gen_images', methods=['POST'])
def gen_images():
    start_time = time.time()
    request_id = str(uuid.uuid4())
    # dir
    save_dir = SCREENSHOT_DIR / request_id
    os.makedirs(save_dir, exist_ok=True)
    logger.info(f"Request ID: {request_id} ->: 开始处理请求，文件存储路径：{save_dir}")

    try:
        data = request.get_json()
        # Daemon task thread
        task_thread = threading.Thread(target=task_handler, args=(data, request_id))
        task_thread.start()
        return jsonify({"request_id": request_id, "message": "Task launch success!"})

    except Exception as e:
        logger.error(f"Request ID: {request_id} -> 请求处理失败")
        return jsonify({"status": "error", "message": str(e)}), 500


@api_bp.route('/task_status/<request_id>', methods=['GET'])
def task_status(request_id):
    save_dir = SCREENSHOT_DIR / request_id
    if not os.path.exists(save_dir):
        return jsonify({"status": "error", "message": f"Request ID `{request_id} not exists!"}), 404

    success_tasks = os.listdir(save_dir)
    return jsonify({"status": "success", "message": success_tasks})


@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "picture_processor"})
