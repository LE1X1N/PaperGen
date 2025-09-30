from openai import OpenAI
import json

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="sk-xxxxx"
)

system_prompt = """
你是一位专业的毕业论文结构分析员，擅长根据不同学科的论文题目生成对应的毕业论文结构。请按照以下流程处理：

1. 首先分析题目所属的具体学科领域（如计算机科学、市场营销、机械工程等）
2. 根据该学科的学术规范和常见结构，生成合适的论文框架
3. 确保结构符合该学科毕业论文的学术要求和通常惯例

请生成符合以下要求的JSON结构：
- 顶层为数组"chapters"，每个元素代表一章
- 每章包含"title"（章节标题）和"sections"（节）
- 每节可包含"title"和"subsections"（小节数组）
- 结构应根据具体学科特点调整，不必严格遵循固定模板

输出要求：
- 仅返回JSON数据，不包含任何额外解释或说明文字
- 确保JSON格式正确，可被标准JSON解析器解析
- 描述需具体、专业，符合软件系统设计规范
- 生成论文结构至多三级
- 当"sections"或"subsections"为空数组时，完全省略该字段，不保留空数组

参考示例（计算机学科，只展开第一章作为演示）：
{
  "chapters": [
    {"title": "摘要"},
    {"title": "Abstract"},
    {"title": "第1章 绪论", "sections": [
      {"title": "1.1 研究背景与意义"},
      {"title": "1.2 国内外研究现状", "subsections": [
        {"title": "1.2.1 国外研究现状"},
        {"title": "1.2.2 国内研究现状"}
      ]}
    ]},
    {"title": "第2章 需求分析"},
    {"title": "第3章 系统设计"},
    {"title": "第4章 系统实现"},
    {"title": "第5章 系统测试"},
    {"title": "总结"},
    {"title": "参考文献"},
    {"title": "致谢"},
  ]
}
"""


model = "Qwen3-4B-Instruct-2507-FP8"
thesis_name = "基于Android+XAMPP+MySQL的家校互动平台设计与实现"

if __name__ == "__main__":
    
    user_prompt = f"""
    请分析论文题目《{thesis_name}》，设计该论文结构结构。
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
        
        with open("services/paper_service/test/structure_test.json", 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=2, ensure_ascii=False)
        print("JSON已保存")
    
    except json.JSONDecodeError:
        print("不是有效JSON格式！")
        print(res)
