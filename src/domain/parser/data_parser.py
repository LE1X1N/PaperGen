from .tmpl_parser import TemplateParser
from .prompts import build_page_prompt, build_module_prompt

class DataParser:
    def __init__(self, logger=None):
        self.tmpl_parser = TemplateParser()
        self.logger = logger
        
    def parse_module(self, request_id: str, data:dict) -> list[dict]:
        # Parse module JSON into tasks list
        try:
            tasks = []
            tmpls = {}
            # choose template for different styles
            for module in data["web_pages"]:
                tmpls[int(module["style"])] = self.tmpl_parser.load_template(int(module["style"]))
            
            for mid, module in enumerate(data["web_pages"]):
                tasks.append(
                    {
                        "request_id": request_id,
                        "page_id": f'module-{mid}',
                        "return_code": True,
                        "style": int(module["style"]),
                        "query": build_module_prompt({
                                                "web_title": data["title"], 
                                                "module_name": module["page_name"],
                                                "style": int(module["style"]),
                                                "module_pages": [m["name"] for m in module['page'] if m["tab"]],
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
                            "style": int(module["style"]),
                            "query": build_page_prompt({
                                        "web_title": data["title"], 
                                        "module_name": module["page_name"],
                                        "style": module["style"],
                                        "page_name": page["name"],
                                        "page_desc": page["text"],
                                        "tmpl": gen_tmpls[mid],
                                        "tab": page['tab']
                            })

                        }
                    )
            return tasks
        
        except KeyError:
            raise
        

    @staticmethod
    def parse_page_ids(data:dict) -> list[str]:
        task_ids = []
        for module in data["web_pages"]:
            for page in module['page']:
                task_ids.append(page["id"])
        return task_ids
