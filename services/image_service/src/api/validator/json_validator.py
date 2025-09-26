from src.errors import InvalidJSONError

class JSONValidator:
    
    @staticmethod
    def check_field(data: dict):
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
        