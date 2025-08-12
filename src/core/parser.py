from src.tmpl import TemplateManager
from src.llm import build_module_prompt, build_page_prompt

class DataParser:
    def __init__(self, tmpl_manager: TemplateManager):
        self.tmpl_manager = tmpl_manager

    def parse_module(self, data:dict, request_id: str) -> list:
        # Parse module JSON into tasks list
        tasks = []
        
        for mid, module in enumerate(data["web_pages"]):
            tasks.append(
                {
                    "request_id": request_id,
                    "task_id": f'{mid}',
                    "return_code": True,
                    "query": build_module_prompt({
                                            "web_title": data["title"], 
                                            "web_detail": data["page_detail"] ,
                                            "module_name": module["page_name"],
                                            "module_desc": module["page_description"],
                                            "module_pages": [m["name"] for m in module['page']],
                                            "tmpl": self.tmpl_manager.load_template(int(module["style"]))
                    })
                }
            )
        return tasks

    def parse_page(self, data: dict, gen_tmpls: dict, request_id: str) -> list:
        # Parse page JSON into tasks list
        tasks = []
        for mid, module in enumerate(data["web_pages"]):
            for pid, page in enumerate(module['page']):
                tasks.append(
                    {
                        "request_id": request_id,
                        "task_id": f'{mid}_{pid}',
                        "return_code": False,
                        "query": build_page_prompt({
                                    "web_title": data["title"], 
                                    "web_detail": data["page_detail"] ,
                                    "module_name": module["page_name"],
                                    "page_name": page["name"],
                                    "page_desc": page["text"],
                                    "tmpl": gen_tmpls[mid]["code"] if gen_tmpls[mid]["status"] else self.tmpl_manager.load_template(int(module["style"]))
                        })

                    }
                )
        return tasks
    
