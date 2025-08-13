from config import conf, client
from openai import APIConnectionError

def build_module_prompt(module:dict):
    prompt = f"""
            你需要为【{module["web_title"]}】系统的【{module["module_name"]}】模块生成对应 React 代码模板（JSX），请参考以下示例的设计模式，同时严格遵循以下规则：。

            ### 1. 模块基本信息
            - 系统名称：{module["web_title"]}
            - 模块名称：{module["module_name"]}
            - 模块功能描述：{module["module_desc"]}
            - 包含页面（导航项）：{module["module_pages"]}

            ### 2. 核心设计原则
            2.1. **业务适配**：
            - 导航栏必须包含所有页面（{module["module_pages"]}），但仅展示导航项框架（名称、图标），不实现具体跳转逻辑。
            - 导航栏不实现点击效果。
            
            2.2. **占位块标记**：
            - 所有需要后续页面级实现的部分，必须用**JSX块注释+结构化标识**占位，格式为：/* MODULE_SLOT: [占位位置描述] */
            - 导航栏仅保留导航项名称和图标，功能逻辑用注释占位。
            - 主内容区的页面细节（如表格、表单、按钮组等），仅保留容器，内容用注释占位。
            - 动态交互逻辑（如数据加载、状态切换等），完全用注释占位，不生成具体代码。

            2.3. **代码完整性**：
            - 导航栏：完整展示所有页面（{module["module_pages"]}），包含名称和图标，但** 无任何点击逻辑 **（用`MODULE_SLOT`占位）。
            - 依赖导入：包含`React`、图标库（如`lucide-react`）等必要依赖，与参考示例一致。
            
            2.4. **风格与配色**：
            - 布局与配色需与模块功能 {module["module_name"]} 匹配。
            - 主色调需明亮轻快, 辅助色与主色调形成和谐对比，增强视觉层次感。
            - 仅参考代码的布局，风格配色需要重新设计。
            
             ### 3. 参考布局代码
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
            - 仅修改模板中所有标记为 /* MODULE_SLOT: [占位位置描述] */ 的内容。
            
            2.2. **风格统一**  
            - 若标记对应导航栏功能：需实现当前页面在导航栏中的 “激活状态”（如高亮样式），并保留其他导航项的框架
            - 必须复用模板中的所有样式类名
            - 图标需使用模板中已导入的库（如 lucide-react），且图标风格（大小、颜色）与模板中其他导航项保持一致
            - 风格，配色符合现代人审美。
            
            ### 3. 模块模板代码
            ```jsx
            {page["tmpl"]}
            ```
            
        """
    return prompt


def call_chat_completion(messages):
    """
        Call LLM to generate code
    """
    try:
        # openai compatible
        response = client.chat.completions.create(
                model=conf["model"],  
                messages=messages,
                stream=False,
                extra_headers={
                    'AIMC-OrderId': "coder-test-leixin",
                    'AIMC-OrderType': "test",
                    'AIMC-Remarks' : "test-leixin",
                    'DOUBAO-THINKING': "disabled"  
                }
            )
        res = response.choices[0].message.content
        return res
    
    except APIConnectionError:
        raise