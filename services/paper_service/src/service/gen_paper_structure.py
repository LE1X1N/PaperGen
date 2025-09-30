import json
from llm.prompt import PAPER_STRUCTURE_PROMPT
from llm.client import call_chat_completion


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


if __name__== "__main__":
    generate_paper_structure( 
        title = "基于Android+XAMPP+MySQL的家校互动平台设计与实现",
        save=True,
        save_path="services/paper_service/test/structure_test.json")