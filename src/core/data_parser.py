from src.llm import build_module_prompt, build_page_prompt
from .tmpl_manager import TemplateManager

class DataParser:
    def __init__(self, tmpl_manager: TemplateManager):
        self.tmpl_manager = tmpl_manager

    def check_field(self, data: dict) -> list[dict]:
        # Check whether input JSON is valid
        try:
            if "title" not in data:
                return False, f"缺少必需字段: title"
            if "page_detail" not in data:
                return False, f"缺少必需字段: page_detail"
            if "web_pages" not in data:
                return False, f"缺少必需字段: web_pages"
                
            # check web_pages type
            if not isinstance(data["web_pages"], list):
                return False, "web_pages必须是数组类型"
            
            # check web_pages
            for mid, module in enumerate(data["web_pages"]):
                if not isinstance(module, dict):
                    return False, f"web_pages[{mid}]必须是对象类型"
                    
                if "page_name" not in module:
                    return False, f"web_pages[{mid}]缺少必需字段: page_name"
                if "page_description" not in module:
                    return False, f"web_pages[{mid}]缺少必需字段: page_description"
                if "page" not in module:
                    return False, f"web_pages[{mid}]缺少必需字段: page"
                    
                # check page
                if not isinstance(module["page"], list):
                    return False, f"web_pages[{mid}].page必须是数组类型"
                    
                for pid, page in enumerate(module["page"]):
                    if not isinstance(page, dict):
                        return False, f"web_pages[{mid}].page[{pid}]必须是对象类型"
                    if "id" not in page:
                        return False, f"web_pages[{mid}].page[{pid}]缺少必需字段: id"
                    if "name" not in page:
                        return False, f"web_pages[{mid}].page[{pid}]缺少必需字段: name"
                    if "text" not in page:
                        return False, f"web_pages[{mid}].page[{pid}]缺少必需字段: text"
        
        except Exception as e:
            return False, f"检查过程中发生错误: {str(e)}"
        
        return True, "所有必需字段检查通过"
                    

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
                                                "web_detail": data["page_detail"] ,
                                                "module_name": module["page_name"],
                                                "module_desc": module["page_description"],
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
                                        "web_detail": data["page_detail"] ,
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