import threading
from flask import Blueprint, request, jsonify
import uuid
import time

from src.core.task_manager import TaskManager
from src.utils import get_logger

logger = get_logger()
api_bp = Blueprint('v1', __name__)
task_manager = TaskManager()


@api_bp.route('/gen_images', methods=['POST'])
def gen_images():
    request_id = str(uuid.uuid4())
    try:
        data = request.get_json()
        task_thread = threading.Thread(target=task_manager.process_tasks, args=(request_id, data))    # Daemon task thread
        task_thread.start()
        return jsonify({"code": 0, "message": "Task launch success!", "request_id": request_id, })

    except Exception as e:
        error_msg = f"请求处理失败: {str(e)}"
        logger.error(f"Request ID: {request_id} -> {error_msg}")
        return jsonify({"code": -1, "message": error_msg}), 500


@api_bp.route('/progress/<request_id>', methods=['GET'])
def get_progress(request_id: str):
    progress = task_manager.progress_manager.get_progress(request_id)
    if not progress:
        return jsonify({"error": "请求ID不存在"}), 404
    return jsonify(progress)


@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "picture_processor"})
