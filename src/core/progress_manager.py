import json
import os
from datetime import datetime
from typing import Dict, Optional, Literal
from pathlib import Path

from src.utils import get_logger
from .data_processing.json_parser import DataParser

logger = get_logger()


class ProgressStatus:
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"

class ProgressManager:
    """
        Upload status JSON to local dir or to mongodb
    """
    
    def __init__(self, base_dir: str, mode: Literal["local, db"] = "local"):
        self.base_dir = Path(base_dir)
        self.request_dict_name = "request_status.json"
        
        if not self.base_dir.exists():
            self.base_dir.mkdir(exist_ok=True)
            logger.info(f"创建文件存储路径：{self.base_dir}")
            
    def _get_request_dir(self, request_id):
        return self.base_dir / request_id
    
    def _get_request_dict_path(self, request_id):
        return self._get_request_dir(request_id) /  self.request_dict_name
        
    def init_request(self, request_id: str, data: dict, task_id: str):
        task_ids = DataParser.parse_task_ids(data)
        
        # create corresponding dir
        save_dir = self._get_request_dir(request_id)
        os.makedirs(save_dir, exist_ok=True)
        
        # create initial dict
        file_path = save_dir / self.request_dict_name
        
        request_dict = {
            "task_id": task_id,
            "request_id": request_id,
            "create_time": datetime.now().isoformat(),
            "total_tasks": len(task_ids),
            "tasks": [
                {"id": task_id, "status": ProgressStatus.PENDING, "url": ""} for task_id in task_ids
            ]
        }
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(request_dict, f, indent=2, ensure_ascii=False)
        logger.info(f"Request ID: {request_id} ->: 开始处理请求，状态文件存储路径：{file_path}")    
        return file_path
    
    
    def update_task_status(self, request_id: str, page_id:str, status:str, url:str="", error: str=""):
        # update corresponding request dict
        file_path = self._get_request_dict_path(request_id)
        if not file_path.exists():
            return False    
        
        # read JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f) 
        
        # updata field
        for task in data.get("tasks", []):
            if task.get("id") == page_id:
                task["status"] = status
                task["url"] = url
                if error:
                    task["error"] = error
                else:
                    task.pop("error", None)  
                break
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        if status == ProgressStatus.FAILED:
            logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【任务失败】{error}")
        return True
    

    def update_all_tasks(self, request_id: str, status:str, url:str="", error: str=""):
        # read JSON
        file_path = self._get_request_dict_path(request_id)
        if not file_path.exists():
            return False   
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f) 
        
        # updata task field
        for task in data.get("tasks", []):
            task["status"] = status
            task["url"] = url
            if error:
                task["error"] = error
            else:
                task.pop("error", None)  
        
        # write JSON
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        if status == ProgressStatus.FAILED:
            logger.error(f"Request ID: {request_id}: 【任务失败】{error}")
            
        return True
        
    
    def get_progress(self, request_id: str) -> Optional[Dict]:
        file_path = self._get_request_dict_path(request_id)
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    
    def save_code(self, request_id: str, page_id: str, code: str):
        file_path = self._get_request_dir(request_id) / f"task_{page_id}.jsx"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        logger.info(f"Request ID: {request_id} -> Task_{page_id}: 代码存储路径：{str(file_path)}")
        