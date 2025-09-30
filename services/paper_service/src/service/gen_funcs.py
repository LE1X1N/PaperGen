import json
from src.llm.prompt import PAPER_STRUCTURE_PROMPT, IMAGE_JSON_PROMPT
from src.llm.client import call_chat_completion


def generate_paper_structure(title: str=None, save: bool=False, save_path: str=None):
    
    user_prompt = f"""
    请分析论文题目《{title}》，设计该论文结构结构。
    """
    messages=[
            {'role':'assistant', 'content': PAPER_STRUCTURE_PROMPT},
            {'role': 'user', 'content': user_prompt}
    ]

    try:
        raw_res = call_chat_completion(messages)
        res = json.loads(raw_res)
        
        if not save:
            return res
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
    
    except json.JSONDecodeError:
        print("不是有效JSON格式！")
        print(res)


def generate_image_json(title: str=None, save: bool=False, save_path: str=None):
    user_prompt = f"""
    请分析论文题目《{title}》，设计该家校互动平台的页面结构，包括所有必要的页面模块、具体页面及其功能描述。
    按照要求的JSON格式输出，确保涵盖不同角色的功能页面（如管理员、用户等角色）。
    """
    
    messages=[
        {'role':'assistant', 'content': IMAGE_JSON_PROMPT},
        {'role': 'user', 'content': user_prompt}
    ]
    
    try:
        raw_res = call_chat_completion(messages)
        res = json.loads(raw_res)
        
        if not save:
            return res
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
    
    except json.JSONDecodeError:
        print("不是有效JSON格式！")
        print(res)
