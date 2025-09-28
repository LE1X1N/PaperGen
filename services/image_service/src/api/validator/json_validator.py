from src.errors import InvalidJSONError

class JSONValidator:
    
    @staticmethod
    def check_field(data: dict):
        # Check whether input JSON is valid
        try:
            if "title" not in data:
                raise InvalidJSONError("缺少必需字段: title")

            if "roles" not in data:
                raise InvalidJSONError("缺少必需字段: roles")
            if not isinstance(data["roles"], list):
                raise InvalidJSONError("roles必须是数组类型") 
            
            # check roles
            for mid, module in enumerate(data["roles"]):
                if not isinstance(module, dict):
                    raise InvalidJSONError("roles[{mid}]必须是对象类型")
                    
                if "role" not in module:
                    raise InvalidJSONError("roles[{mid}]缺少必需字段: role")
                
                # check page
                if "pages" not in module:
                    raise InvalidJSONError("roles[{mid}]缺少必需字段: page")
                if not isinstance(module["pages"], list):
                    raise InvalidJSONError("roles[{mid}].page必须是数组类型")
                    
                for pid, page in enumerate(module["pages"]):
                    if not isinstance(page, dict):
                        raise InvalidJSONError("roles[{mid}].pages[{pid}]必须是对象类型")
                    if "id" not in page:
                        raise InvalidJSONError("roles[{mid}].pages[{pid}]缺少必需字段: id")
                    if "name" not in page:
                        raise InvalidJSONError("roles[{mid}].pages[{pid}]缺少必需字段: name")
                    if "desc" not in page:
                        raise InvalidJSONError("roles[{mid}].pages[{pid}]缺少必需字段: desc")

        except InvalidJSONError:
            raise
        