import threading
from flask import Blueprint, request, jsonify
import uuid

from .validator.json_validator import JSONValidator
from src.utils import get_logger
from src.domain.pipeline import TaskManager
from src.infrastructure.llm import check_openai_health
from src.infrastructure.db import check_mongodb_health

api_bp = Blueprint('v1', __name__)
logger = get_logger()

task_manager = TaskManager(logger=logger)  # global task manager


@api_bp.route('/gen_figures', methods=['POST'])
def gen_figures():
    request_id = str(uuid.uuid4())
    req = request.get_json()      
    logger.info(f"Request ID: {request_id} -> 接收请求：{req}")
      
    task_id = req['task_id']
    data = req['data']
  
    try:
        JSONValidator.check_field(data)    # check JSON field
        task_thread = threading.Thread(target=task_manager.process_tasks, args=(request_id, data, task_id))  
        task_thread.start()
        logger.info(f"Request ID: {request_id} -> 创建任务成功！")
        return jsonify({"code": 0, "message": "任务创建成功!", "task_id": task_id,  "request_id": request_id})
        
    except Exception as e:
        logger.info(f"Request ID: {request_id} -> 创建任务失败：{e} ")
        return jsonify({"code": -1, "message": f"任务创建失败! {e}"}), 500
    

@api_bp.route('/progress/<request_id>', methods=['GET'])
def get_progress(request_id: str):
    progress = task_manager.progress_repo.get_progress(request_id)
    if not progress:
        return jsonify({"error": "请求ID不存在"}), 404
    return jsonify(progress)


@api_bp.route('/health', methods=['GET'])
def health_check():
    try:
        check_openai_health()                                 
        check_mongodb_health()
        return jsonify({"code": 0, "status": "healthy"})
    
    except Exception as e:
        return jsonify({"code": -1, "status": "error", "msg": str(e)}), 500
    
    