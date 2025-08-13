from src.tmpl import TemplateManager
from src.llm import build_module_prompt, build_page_prompt


class DataParser:
    def __init__(self, tmpl_manager: TemplateManager):
        self.tmpl_manager = tmpl_manager

    def parse_module(self, request_id: str, data:dict) -> list[dict]:
        # Parse module JSON into tasks list
        tasks = []
        
        for mid, module in enumerate(data["web_pages"]):
            tasks.append(
                {
                    "request_id": request_id,
                    "task_id": f'module-{mid}',
                    "return_code": True,
                    "query": build_module_prompt({
                                            "web_title": data["title"], 
                                            "web_detail": data["page_detail"] ,
                                            "module_name": module["page_name"],
                                            "module_desc": module["page_description"],
                                            "module_pages": [m["name"] for m in module['page']],
                                            "tmpl": self.tmpl_manager.load_template(int(module["style"]+1))
                    })
                }
            )
        return tasks

    def parse_page(self, request_id: str, data: dict, gen_tmpls: dict) -> list[dict]:
        # Parse page JSON into tasks list
        tasks = []
        for mid, module in enumerate(data["web_pages"]):
            for pid, page in enumerate(module['page']):
                tasks.append(
                    {
                        "request_id": request_id,
                        "task_id": f"{page["id"]}",
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

    @staticmethod
    def parse_task_ids(data:dict) -> list[str]:
        task_ids = []
        for module in data["web_pages"]:
            for page in module['page']:
                task_ids.append(page["id"])
        return task_ids