from openai import OpenAI
from openai import APIConnectionError, InternalServerError

from src.config import conf


def build_module_prompt(module:dict):
    prompt = f"""
            你需要为【{module["web_title"]}】系统的【{module["module_name"]}】模块生成对应 React 代码模板（JSX），请参考以下示例的设计模式，同时严格遵循以下规则：。

            ### 1. 模块基本信息
            - 系统名称：{module["web_title"]}
            - 模块名称：{module["module_name"]}
            - 模块功能描述：{module["module_desc"]}
            - 包含页面（导航项）：{module["module_pages"]}

            ### 2. 核心设计原则
            2.1. **页面设计**：
            - 页面包括两部分：【导航栏】和【主内容区】

            2.2 **导航栏设计**
            - 导航栏需要包括：（{module["module_pages"]}），但仅展示导航项【名称】与【图标】，不实现具体跳转逻辑。
            - 导航栏不实现点击效果。
            
            2.3 **主内容区设计**
            - 主内容区的页面细节不进行设计，内容用注释占位， 
            - 所有需要后续页面级实现的部分，必须用**JSX块注释+结构化标识**占位，格式为：/* MODULE_SLOT: [占位位置描述] */

            2.4. **其他要求**：
            - 布局与配色需要与模块功能 {module["module_name"]} 匹配。
            - 依赖导入：根据该模块的功能，导入所需的包，包含`React`、图标库（如`lucide-react`）等必要依赖。
            
             ### 3. 参考模板代码
             {module["tmpl"]}
        """
    return prompt


def build_page_prompt(page:dict):
    """
        Build prompt based on JSON
    """
    prompt = f"""
            你需要基于【{page["module_name"]}】模块的模板代码，为【{page["page_name"]}】页面生成具体功能实现 （React JSX），**仅修改模板中/* MODULE_SLOT: [占位位置描述] */ 标记的内容**，同时确保与模块风格统一。
            
            ### 1. 页面基本信息
            - 系统名称：{page["web_title"]}
            - 页面所属模块：{page["module_name"]}
            - 页面名称：{page["page_name"]}   (导航栏根据此激活对应项)
            - 页面功能描述：{page["page_desc"]}
          
            ### 2. 核心设计原则
            2.1. **替换范围**  
            - 核心修改模板当中的 【主内容区】
            - 依照页面功能描述，修改模板中所有标记为 /* MODULE_SLOT: [占位位置描述] */ 的内容。
            
            2.2. **风格统一**  
            - 若标记对应导航栏功能：需实现当前页面在导航栏中的 “激活状态”（如高亮样式），并保留其他导航项的框架
            - 必须复用模板中的所有样式类名
            - 图标需使用模板中已导入的库（如 lucide-react），且图标风格（大小、颜色）与模板中其他导航项保持一致
            
            ### 3. 【{page["module_name"]}】模板代码
            ```jsx
            {page["tmpl"]}
            ```
            
        """
    return prompt

 # OpenAI client
client = OpenAI(
    base_url=conf["base_url"],
    api_key=conf["api_key"]
)

def call_chat_completion(messages):
    """
        Call LLM to generate code
    """
    try:
        # openai compatible
        response = client.chat.completions.create(
                model=conf["model"],  
                messages=messages,
                stream=True,
                extra_headers={
                    'AIMC-OrderId': "coder-test-leixin",
                    'AIMC-OrderType': "test",
                    'AIMC-Remarks' : "test-leixin",
                    'DOUBAO-THINKING': "disabled"  
                }
            )
        
        full_content = []
        for chunk in response:
            if chunk.choices:
                content = chunk.choices[0].delta.content
                if content:
                    full_content.append(content) 
        return ''.join(full_content)
    
    except APIConnectionError:
        raise
    
    except InternalServerError:
        raise
    
    except Exception:
        raise