from flask import Blueprint, request, jsonify
import time
import uuid

from src.core.task_manager import TaskManager
from src.utils import get_logger


logger = get_logger()
api_bp = Blueprint('v1', __name__)

task_manager = TaskManager()

@api_bp.route('/gen_images', methods=['POST'])
def gen_images():
    start_time = time.time()
    request_id = str(uuid.uuid4())
    logger.info(f"Request ID: {request_id} ->: 开始处理请求")
    
    try:
        data = request.get_json()
        results = task_manager.process_tasks(data, request_id)
        logger.info(f"Request ID: {request_id} -> 请求完成，耗时 {time.time() - start_time} s")
        return jsonify({"request_id" : request_id, "response": results})
    
    except Exception as e:
        logger.info(f"Request ID: {request_id} -> 请求处理失败")
        return jsonify({"status": "error", "message": str(e)}), 500



@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "picture_processor"})

