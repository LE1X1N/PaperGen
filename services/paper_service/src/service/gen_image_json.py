from openai import OpenAI
import json

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="sk-xxxxx"
)


model = "Qwen3-4B-Instruct-2507-FP8"
thesis_name = "基于Android+XAMPP+MySQL的家校互动平台设计与实现"

if __name__ == "__main__":
    
    user_prompt = f"""
    请分析论文题目《{thesis_name}》，设计该家校互动平台的页面结构，包括所有必要的页面模块、具体页面及其功能描述。
    按照要求的JSON格式输出，确保涵盖不同角色的功能页面（如管理员、用户等角色）。
    """
    
    response = client.chat.completions.create(
        messages=[
            {'role':'assistant', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ],
        model=model,
        temperature=0.3
    )
    
    try:
        raw_res = response.choices[0].message.content.strip()
        res = json.loads(raw_res)
        
        with open("services/paper_service/test/tmp.json", 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
        print("JSON已保存")
    
    except json.JSONDecodeError:
        print("不是有效JSON格式！")
        print(res)
