from openai import OpenAI
import json

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="sk-xxxxx"
)

system_prompt = """
你是一位专业的软件系统设计文档工程师，擅长分析论文题目并生成详细的系统页面结构。

请根据用户提供的论文题目，分析该系统的核心功能和用户角色，然后生成符合以下要求的JSON结构：

1. 顶级键为"data"，包含两个子键：
   - "title"：论文题目（直接使用用户提供的题目）
   - "web_pages"：数组，包含系统的主要页面模块

2. "web_pages"中的每个元素是一个对象，包含：
   - "page_name"：页面模块名称
   - "page"：数组，包含该模块下的具体页面
   - "style"：样式标识（0/1/2,根据页面特性决定，0为网站类型，1为手机程序类型，2为微信小程序类型）

3. "page"中的每个元素是一个对象，包含：
   - "name"：具体页面名称
   - "text"：页面功能详细描述，需说明页面包含的元素、功能和操作
   - "id"：唯一标识符（数字，从0开始递增）
   - "tab"：布尔值，表示该页面是否为导航标签页（直接展示在导航栏的页面为true）

输出要求：
- 仅返回JSON数据，不包含任何额外解释或说明文字
- 确保JSON格式正确，可被标准JSON解析器解析
- 根据论文题目中的系统特性合理划分页面模块和功能
- 描述需具体、专业，符合软件系统设计规范
"""


model = "Qwen3-4B-Instruct-2507-FP8"
thesis_name = "基于Android+XAMPP+MySQL的家校互动平台设计与实现"

if __name__ == "__main__":
    
    user_prompt = f"""
    请分析论文题目《{thesis_name}》，设计该家校互动平台的页面结构，包括所有必要的页面模块、具体页面及其功能描述。
    按照要求的JSON格式输出，确保涵盖不同角色的功能页面（如管理员、用户等角色），以及系统公共页面（如登录注册、首页等）。
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
        
        with open("tmp.json", 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
        print("JSON已保存")
    
    except json.JSONDecodeError:
        print("不是有效JSON格式！")
        print(res)
