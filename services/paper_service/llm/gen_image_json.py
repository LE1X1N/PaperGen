from openai import OpenAI
import json

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="sk-xxxxx"
)

system_prompt = """
你是一位专业的软件系统设计文档工程师，擅长分析论文题目并生成详细的系统页面结构。请严格按照以下流程处理用户提供的论文题目：

请严格按照以下流程处理用户提供的论文题目：
- 首先分析系统的核心用户角色（通常为 2-3 类，如管理员 / 普通用户等）
- 针对每类用户角色，确定其对应的界面样式（0 为网站类型，1 为手机程序类型，2 为微信小程序类型）
- 为每类用户设计合理的页面体系，包括导航标签页和次级页面

请生成符合以下要求的 **JSON** 结构：

1. 顶级键为"data"，包含两个子键：
   - "title"：直接使用用户提供的论文题目
   - "roles"：数组，每个元素代表一类用户的页面集合

2. "roles"中的每个对象包含：
   - "role"：该模块所属用户角色类型
   - "pages"：数组，包含该角色可访问的所有页面
   - "style"：样式标识（0/1/2，根据角色特性合理分配）

3. "pages"中的每个元素是一个对象，包含：
   - "name"：具体页面名称
   - "desc"：详细描述页面功能、包含元素及操作方式（
   - "id"：唯一标识符（数字，从0开始递增）
   - "tab"：布尔值，表示该页面是否需要功能栏（默认为True）

输出要求：
- 仅返回JSON数据，不包含任何额外解释或说明文字
- 确保JSON格式正确，可被标准JSON解析器解析
- 根据论文题目中的系统特性合理划分使用用户类别。
- 描述需具体、专业，符合软件系统设计规范
- 所有页面总数(最大id)不超过 15 个
"""


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
