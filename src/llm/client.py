from config import conf, client

"""
你需要为“系统管理后台”模块生成基础前端框架代码（HTML+CSS+JS），要求：
1. 固定布局：左侧固定导航栏（包含“仪表盘”“问卷管理”等模块内页面入口）、顶部操作栏（含搜索框、用户信息）、主内容区（占比80%）。
2. 固定样式：导航栏背景色#2c3e50、激活项高亮色#3498db、按钮统一使用类名"btn-admin"（样式已定义）。
3. 标记可修改区域：用<!-- MODULE_SLOT: 区域名称 -->标记主内容区的可变部分，例如：
   <!-- MODULE_SLOT: main_content -->
   （此处为各页面的个性化内容，如“仪表盘”的图表/“问卷管理”的表格）
   <!-- MODULE_SLOT_END -->
4. 包含通用逻辑：导航栏点击切换高亮、页面加载动画、权限校验前置逻辑（无需修改）。

"""

"""
基于以下“系统管理后台”模块的基础模板，为“问卷管理”页面生成代码：
【模块基础模板】
{此处插入步骤1生成的模块模板代码，包含<!-- MODULE_SLOT: main_content -->标记}

要求：
1. 仅修改<!-- MODULE_SLOT: main_content -->和<!-- MODULE_SLOT_END -->之间的内容。
2. 内容需符合“问卷管理”页面需求：展示问卷列表表格（含名称、状态、操作列）、顶部“新建问卷”按钮（使用类名"btn-admin"）。
3. 不修改模板中的布局、样式变量、导航组件（如左侧导航栏的内容和样式）。
4. 复用模板中的组件：表格使用模板中定义的"table-admin"类，按钮使用"btn-admin"类。

"""

example = """
// 示例：“用户答题中心”模块的模板（供参考设计模式）
import React from 'react';
import { BookOpen, Clock, History, User } from 'lucide-react';
import dayjs from 'dayjs';

const UserAnswerCenterModule = () => {
  // 模块配置（与业务匹配）
  const moduleConfig = {
    moduleName: "用户答题中心",
    pages: ["可参与问卷", "进行中答题", "答题历史", "个人中心"],
    style: {
      primaryColor: "#4f46e5", // 模块主色（统一风格）
      cardStyle: "bg-white rounded-lg shadow-sm p-4" // 通用组件样式（统一风格）
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* 顶部导航（根据“用户答题中心”场景设计，非固定布局） */}
      <header className="bg-white border-b border-slate-200">
        <div className="container mx-auto px-4 py-3">
          <h1 className="text-xl font-bold text-slate-800">{moduleConfig.moduleName}</h1>
          <p className="text-sm text-slate-500">当前时间：{dayjs().format('YYYY-MM-DD')}</p>
        </div>
        
        {/* 页面导航（适配“用户中心”场景的顶部Tab，非固定布局） */}
        <nav className="border-b border-slate-200">
          <div className="container mx-auto px-4">
            <ul className="flex space-x-6">
              {moduleConfig.pages.map((page, idx) => (
                <li key={idx}>
                  <a 
                    href="#" 
                    className={`py-3 inline-block text-sm font-medium ${
                      /* 统一的高亮样式（保持风格） */
                      page === "可参与问卷" ? `text-${moduleConfig.style.primaryColor.substring(1)} border-b-2 border-${moduleConfig.style.primaryColor.substring(1)}` : "text-slate-500 hover:text-slate-700"
                    }`}
                  >
                    {page}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </nav>
      </header>

      {/* 主内容区（含占位块，供页面级替换） */}
      <main className="container mx-auto px-4 py-6">
        {/* 页面标题占位块（统一标记方式） */}
        <h2 data-slot="page_title" className="text-lg font-semibold mb-4 text-slate-800"></h2>
        
        {/* 主内容占位块（统一标记方式） */}
        <div data-slot="main_content" className={moduleConfig.style.cardStyle}></div>
      </main>
    </div>
  );
};

export default App;
"""


def build_module_prompt(module:dict):
    prompt = f"""
            你需要为【{module["web_title"]}】系统的【{module["module_name"]}】模块生成对应 React 代码模板（JSX），请参考以下示例的设计模式，同时严格遵循以下规则：。

            ### 1. 模块基本信息
            - 系统名称：{module["web_title"]}
            - 模块名称：{module["module_name"]}
            - 模块功能描述：{module["module_desc"]}
            - 包含页面（导航项）：{module["module_pages"]}

            ### 2. 核心设计原则
            1. **业务适配**：
            - 若为「管理后台类模块」（如“XX管理后台”）：优先采用“左侧固定导航栏+顶部操作栏+主内容区”布局，支持复杂导航层级。
            - 若为「用户交互类模块」（如“用户XX中心”）：可采用“顶部Tab导航+简洁主内容区”布局，减少操作复杂度。
            - 若为「简单功能模块」（如“登录/注册”）：采用“居中表单+弱导航”布局，聚焦核心交互。
            - 导航栏必须包含所有页面（{module["module_pages"]}），但仅展示导航项框架（名称、图标），不实现具体跳转逻辑。
            
            2. **占位块标记**：
            - 所有需要后续页面级实现的部分，必须用**JSX块注释+结构化标识**占位，格式为：/* MODULE_SLOT: [占位位置描述] */
            - 导航项（仅保留导航项名称和图标，功能逻辑用注释占位）。
            - 主内容区的页面细节（如表格、表单、按钮组等，仅保留容器，内容用注释占位）。
            - 动态交互逻辑（如数据加载、状态切换等，完全用注释占位，不生成具体代码）。

            3. **代码完整性**：
            - 布局结构：根据模块类型（管理后台/用户中心/简单功能）设计完整框架。
            - 导航栏：完整展示所有页面（{module["module_pages"]}），包含名称和图标，但** 无任何点击逻辑 **（用`MODULE_SLOT`占位）。
            - 样式体系：固化统一的样式（颜色、间距、圆角、阴影），通过类名定义（如`bg-primary` `card-container`），不允许在占位符中修改样式。
            - 依赖导入：包含`React`、图标库（如`lucide-react`）等必要依赖，与参考示例一致。
            
             ### 3. 参考示例
             {module["tmpl"]}
        """
    return prompt


def build_page_prompt(page:dict):
    """
        Build prompt based on JSON
    """
    prompt = f"""
            你需要基于【{page["module_name"]}】模块的模板代码，为【{page["page_name"]}】页面生成具体功能实现 （React），**仅修改模板中/* MODULE_SLOT: [占位位置描述] */ 标记的内容**，同时确保与模块风格统一。
            
            ### 1. 页面基本信息
            - 系统名称：{page["web_title"]}
            - 页面所属模块：{page["module_name"]}
            - 页面名称：{page["page_name"]}
            - 页面功能描述：{page["page_desc"]}
            
            ### 2. 模块模板代码
            ```jsx
            {page["tmpl"]}
            ```
            
            ### 3. 核心设计原则

            1. **替换范围**  
            - 仅修改模板中所有标记为 /* MODULE_SLOT: [占位位置描述] */ 的内容。
            - 若标记对应导航栏功能：需实现当前页面在导航栏中的 “激活状态”（如高亮样式），并保留其他导航项的框架
            
            2. **风格统一**  
            - 必须复用模板中的所有样式类名
            - 图标需使用模板中已导入的库（如 lucide-react），且图标风格（大小、颜色）与模板中其他导航项保持一致
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
    
    except Exception as e:
        raise Exception(f"处理响应失败: {str(e)}")