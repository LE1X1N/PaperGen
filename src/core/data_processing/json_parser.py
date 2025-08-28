from src.llm import build_module_prompt, build_page_prompt
from src.errors import InvalidJSONError

from .tmpl_manager import TemplateManager


class DataParser:
    def __init__(self):
        self.tmpl_manager = TemplateManager()

    def check_field(self, data: dict):
        # Check whether input JSON is valid
        try:
            if "title" not in data:
                raise InvalidJSONError("缺少必需字段: title")
            if "web_pages" not in data:
                raise InvalidJSONError("缺少必需字段: web_pages") 
                
            # check web_pages type
            if not isinstance(data["web_pages"], list):
                raise InvalidJSONError("web_pages必须是数组类型") 
            
            # check web_pages
            for mid, module in enumerate(data["web_pages"]):
                if not isinstance(module, dict):
                    raise InvalidJSONError("web_pages[{mid}]必须是对象类型")
                    
                if "page_name" not in module:
                    raise InvalidJSONError("web_pages[{mid}]缺少必需字段: page_name")
                if "page" not in module:
                    raise InvalidJSONError("web_pages[{mid}]缺少必需字段: page")
                    
                # check page
                if not isinstance(module["page"], list):
                    raise InvalidJSONError("web_pages[{mid}].page必须是数组类型")
                    
                for pid, page in enumerate(module["page"]):
                    if not isinstance(page, dict):
                        raise InvalidJSONError("web_pages[{mid}].page[{pid}]必须是对象类型")
                    if "id" not in page:
                        raise InvalidJSONError("web_pages[{mid}].page[{pid}]缺少必需字段: id")
                    if "name" not in page:
                        raise InvalidJSONError("web_pages[{mid}].page[{pid}]缺少必需字段: name")
                    if "text" not in page:
                        raise InvalidJSONError("web_pages[{mid}].page[{pid}]缺少必需字段: text")

        except InvalidJSONError:
            raise
        
                    

    def parse_module(self, request_id: str, data:dict) -> list[dict]:
        # Parse module JSON into tasks list
        try:
            tasks = []
            tmpls = {}
            # choose template for different styles
            for module in data["web_pages"]:
                tmpls[int(module["style"])] = self.tmpl_manager.load_template(int(module["style"]))
            
            for mid, module in enumerate(data["web_pages"]):
                tasks.append(
                    {
                        "request_id": request_id,
                        "page_id": f'module-{mid}',
                        "return_code": True,
                        "query": build_module_prompt({
                                                "web_title": data["title"], 
                                                "module_name": module["page_name"],
                                                "module_pages": [m["name"] for m in module['page']],
                                                "tmpl": tmpls[int(module["style"])]
                        })
                    }
                )
            return tasks
        
        except KeyError:
            raise
        
        
    def parse_page(self, request_id: str, data: dict, gen_tmpls: dict) -> list[dict]:
        # Parse page JSON into tasks list
        try:
            tasks = []
            for mid, module in enumerate(data["web_pages"]):
                for pid, page in enumerate(module['page']):
                    tasks.append(
                        {
                            "request_id": request_id,
                            "page_id": f"{page["id"]}",
                            "return_code": False,
                            "query": build_page_prompt({
                                        "web_title": data["title"], 
                                        "module_name": module["page_name"],
                                        "page_name": page["name"],
                                        "page_desc": page["text"],
                                        "tmpl": gen_tmpls[mid]
                            })

                        }
                    )
            return tasks
        
        except KeyError:
            raise
        

    @staticmethod
    def parse_task_ids(data:dict) -> list[str]:
        task_ids = []
        for module in data["web_pages"]:
            for page in module['page']:
                task_ids.append(page["id"])
        return task_ids
    