import json
from typing import Dict

from src.llm.prompt import PAPER_STRUCTURE_PROMPT,  PAPER_ABSTRACT_PROMPT
from src.llm.prompt import TABLE_DESC_JSON_PROMPT, FIGURE_DESC_JSON_PROMPT
from src.llm.client import call_chat_completion


def llm_json_generator(system_prompt: str) -> callable:
    """
        a decorator which encapsulate llm calling, JSON parsing and file saving
    """
    
    def decorator(func):    # input is a function
        def wrapper(*args, **kwargs) -> Dict:
            func(*args, **kwargs)   # run initial function
            
            query = kwargs["query"]
            save = kwargs["save"]
            save_path = kwargs["save_path"]
        
            messages = [
                {'role': 'assistant', 'content': system_prompt},
                {'role': 'user', 'content': query}
            ]    
            
            try:
                raw_res = call_chat_completion(messages)
                res = json.loads(raw_res)
                if save:
                    with open(save_path, 'w', encoding='utf-8') as f:
                        json.dump(res, f, indent=2, ensure_ascii=False)
                return res
            
            except json.JSONDecodeError:
                print("不是有效的JSON格式")
            
        return wrapper
    return decorator


class JSONGenerator:
    
    @llm_json_generator(PAPER_STRUCTURE_PROMPT)
    def generate_paper_structure(self, query: str=None, save: bool=False, save_path: str=None) -> Dict:
        pass


    @llm_json_generator(PAPER_ABSTRACT_PROMPT)
    def generate_abstract_json(self, query: str=None, save: bool=False, save_path: str=None) -> Dict:
        pass


    @llm_json_generator(TABLE_DESC_JSON_PROMPT)
    def generate_table_desc_json(self, query: str=None, save: bool=False, save_path: str=None) -> Dict:
        pass

    @llm_json_generator(TABLE_DESC_JSON_PROMPT)
    def generate_table_desc_json(self, query: str=None, save: bool=False, save_path: str=None) -> Dict:
        pass

    @llm_json_generator(FIGURE_DESC_JSON_PROMPT)
    def generate_figure_desc_json(self, query: str=None, save: bool=False, save_path: str=None) -> Dict:
        pass