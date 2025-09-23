from datetime import datetime
from typing import Dict, Optional

from src.infrastructure.db import get_mongo_collection


class ProgressStatus:
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class ProgressRepository:
    """
        Upload status JSON to local dir or to mongodb
    """
    
    def __init__(self, logger=None):
        self.logger = logger
        self.collection = get_mongo_collection()
        
        
    def init_request(self, request_id: str, page_ids: list, task_id: str):
        """
            request_id: 服务对于每个请求request生成的独立ID
            page_id: 请求体中的每个页面附带ID
            task_id: 请求体中附带任务ID
        """    
        request_dict = {
            "_id": request_id,
            "task_id": task_id,
            "create_time": datetime.now().isoformat(),
            "total_tasks": len(page_ids),
            "tasks": [
                {"id": page_id, "status": ProgressStatus.PENDING, "url": ""} for page_id in page_ids
            ]
        }
        
        res = self.collection.insert_one(request_dict)
        return res.inserted_id
    
    
    def update_task_status(self, request_id: str, page_id:str, status:str, url:str="", error: str=""):
        # update corresponding request dict
        update_fields = {
            f"tasks.$.status" : status
        }
        if url:
            update_fields[f"tasks.$.url"] = url
        if error:
            update_fields[f"tasks.$.error"] = error
        
        # filter
        res = self.collection.update_one(
            filter={
                "_id": request_id, 
                "tasks.id": page_id
            },
            update={"$set": update_fields}
        )
        
        self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: 【任务完成】MongoDB任务状态更新成功：{status}")
        return res.modified_count == 1
    

    def get_progress(self, request_id: str) -> Optional[Dict]:
        document = self.collection.find_one({"_id": request_id})
        if document:
            str_id = str(document["_id"])
            del document["_id"]
            document["request_id"] = str_id
        return document
