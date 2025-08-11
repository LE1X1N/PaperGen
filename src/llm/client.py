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
            你需要为【{module["web_title"]}】的 【{module["module_name"]}】模块，生成对应 React 代码模板（JSX），请参考以下示例的设计模式，根据模块特点灵活设计布局，同时遵守核心原则。

            ### 1. 模块基本信息
            - 系统名称：{module["web_title"]}
            - 模块名称：{module["module_name"]}
            - 包含功能页面：{module["module_pages"]}
        
            ### 2. 核心设计原则
            1. **风格统一性**：
            - 为模块定义一套统一的样式（如主色、卡片样式、按钮风格），并在所有组件中复用（参考示例的`style`配置）。
            - 页面导航项（如Tab、侧边栏）的交互样式（高亮、 hover 效果）保持一致。
           
            2. **占位块标记**：
            - 必须使用 `data-slot` 属性标记可替换区域（供页面级生成），至少包含：
                - `data-slot="main_content"`：主内容区（页面具体内容）
                - `data-slot="page_title"`：页面标题（当前页名称）
            - 占位块标签类型不限（div/h2等），但`data-slot`属性值必须严格匹配。

            3. **业务适配性**：
            - 根据模块的业务场景设计布局（如“系统管理后台”适合复杂导航，“登录模块”适合居中表单，参考示例如何适配“用户答题中心”）。
            - 导航项必须包含模块的所有页面：{module["module_pages"]}，并动态生成（避免硬编码）。
            
            4. **代码完整性**：
            - 包含必要的依赖（React、图标库等，参考示例的import）。
            - 只生成静态UI，无需操作逻辑
            
             ### 3. 参考示例
             {module["tmpl"]}
        """
    return prompt


def build_page_prompt(page:dict):
    """
        Build prompt based on JSON
    """
    prompt = f"""
            你需要为【{page["module_name"]}】模块 中的 【{page["page_name"]}】界面，生成对应 React 代码（JSX），请参考以下示例的设计模式，根据模块特点灵活设计布局，同时遵守核心原则。

            ### 1. 页面基本信息
            - 系统名称：{page["web_title"]}
            - 模块名称：{page["module_name"]}
            - 页面名称：{page["page_name"]}
            - 页面描述：{page["page_desc"]}
            
            ### 2. 模块模板代码（仅参考可修改的区域，不改动其他部分）
            {page["tmpl"]}
            
            ### 3. 核心设计原则
            1. **强约束替换范围**  
              明确要求模型“仅修改 `data-slot` 标记内的内容”，并通过示例展示如何定位和替换，避免模型误改模板框架（如导航栏、样式类）。  

            2. **风格统一保障**  
              强制复用模板中的样式类名、依赖和组件风格，确保模块内页面风格一致。  
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