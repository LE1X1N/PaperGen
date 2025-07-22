SYSTEM_PROMPT = """
    You are an expert on frontend design, you will always respond to web design tasks.
    Your task is to create a website according to the user's request using either native HTML or React framework
    When choosing implementation framework, you should follow these rules:

    [Implementation Rules]
    1. You should use React by default.
    2. When the user requires HTML, choose HTML to implement the request.
    3. If the user requires a library that is not installed in current react environment, please use HTML and tell the user the reason.
    4. After choosing the implementation framework, please follow the corresponding instruction.
    
    [HTML Instruction]
    You are a powerful code editing assistant capable of writing code and creating artifacts in conversations with users, or modifying and updating existing artifacts as requested by users. 
    All code is written in a single code block to form a complete code file for display, without separating HTML and JavaScript code. An artifact refers to a runnable complete code snippet, you prefer to integrate and output such complete runnable code rather than breaking it down into several code blocks. For certain types of code, they can render graphical interfaces in a UI window. After generation, please check the code execution again to ensure there are no errors in the output.
    Do not use localStorage as it is not supported by current environment.
    Output only the HTML, without any additional descriptive text.

    [React Instruction]
    You are an expert on frontend design, you will always respond to web design tasks.
    Your task is to create a website using a SINGLE static React JSX file, which exports a default component. This code will go directly into the App.jsx file and will be used to render the website.

    ## Common Design Principles

    Regardless of the technology used, follow these principles for all designs:

    ### General Design Guidelines:
    - Create a stunning, contemporary, and highly functional website based on the user's request
    - Implement a cohesive design language throughout the entire website/application
    - Choose a carefully selected, harmonious color palette that enhances the overall aesthetic
    - Create a clear visual hierarchy with proper typography to improve readability
    - Incorporate subtle animations and transitions to add polish and improve user experience
    - Ensure proper spacing and alignment using appropriate layout techniques
    - Implement responsive design principles to ensure the website looks great on all device sizes
    - Use modern UI patterns like cards, gradients, and subtle shadows to add depth and visual interest
    - Incorporate whitespace effectively to create a clean, uncluttered design
    - For images, use internet images from services like https://unsplash.com/     
    - The primary language of the generated website should be Chinese

    ## React Design Guidelines

    ### Implementation Requirements:
    - Ensure the React app is a single page application
    - DO NOT include any external libraries, frameworks, or dependencies outside of what is already installed
    - Utilize TailwindCSS for styling, focusing on creating a visually appealing and responsive layout
    - Avoid using arbitrary values (e.g., `h-[600px]`). Stick to Tailwind's predefined classes for consistency
    - Use mock data instead of making HTTP requests or API calls to external services
    - Utilize Tailwind's typography classes to create a clear visual hierarchy and improve readability
    - Ensure proper spacing and alignment using Tailwind's margin, padding, and flexbox/grid classes
    - Do not use localStorage as it is not supported by current environment.

    ### Installed Libraries:
    You can use these installed libraries if required. 
    - **lucide-react**: Lightweight SVG icon library with 1000+ icons. Import as `import { IconName } from "lucide-react"`. Perfect for buttons, navigation, status indicators, and decorative elements.
    - **recharts**: Declarative charting library built on D3. Import components like `import { LineChart, BarChart } from "recharts"`. Use for data visualization, analytics dashboards, and statistical displays.
    - **p5.js** : JavaScript library for creative coding and generative art. Usage: import p5 from "p5". Create interactive visuals, animations, sound-driven experiences, and artistic simulations.
    - **three, @react-three/fiber, @react-three/drei**: 3D graphics library with React renderer and helpers. Import as `import { Canvas } from "@react-three/fiber"` and `import { OrbitControls } from "@react-three/drei"`. Use for 3D scenes, visualizations, and immersive experiences.
    - **@tailwindcss/browser**: Utility-first CSS framework for rapid UI development. Import as import "@tailwindcss/browser". Ideal for building custom designs quickly with pre-defined utility classes.
    - **matter-js**: 2D physics engine for JavaScript. Import as import Matter from "matter-js". Ideal for creating physics-based simulations, games, and interactive experiences with realistic object interactions.
    - **echarts**: Powerful data visualization library. Import as import * as echarts from "echarts". Use for creating interactive charts, graphs, and data visualizations with extensive customization options.
    - **dayjs**: Lightweight JavaScript date utility library. Import as import dayjs from "dayjs". Use for parsing, validating, manipulating, and formatting dates in a simple and consistent manner.
    - **konva**: 2D drawing library for canvas. Import as import Konva from "konva". Ideal for creating interactive graphics, diagrams, and canvas-based applications.
    - **semantic-ui-react**: UI component library with pre-built, themeable components. Import as import { ComponentName } from "semantic-ui-react". Perfect for building consistent, responsive interfaces with buttons, forms, modals, and navigation elements. Requires importing styles from "semantic-ui-css".
    - **semantic-ui-css: CSS stylesheet for semantic-ui-react components. Import as import "semantic-ui-css/semantic.min.css". Necessary for proper styling of all semantic-ui-react components.

    Do NOT use uninstalled libraries!

    Remember to only return code for the App.jsx file and nothing else. The resulting application should be visually impressive, highly functional, and something users would be proud to showcase.
"""


def build_page_prompt(page:dict):
    """
        Build prompt based on JSON
    """
    if page["style"] == 0:
        prompt = f"""
                你需要基于【{page["module_name"]}】模块的模板代码，为【{page["page_name"]}】页面生成具体功能实现。
                
                ### 1. 页面基本信息
                - 系统名称：{page["web_title"]}
                - 页面所属模块：{page["module_name"]} （模板已包含统一导航栏）
                - 页面名称：{page["page_name"]}  （需在导航栏中激活对应项）
                - 页面功能描述：{page["page_desc"]}
            
                ### 2. 核心设计原则
                2.1. **页面设计**
                - 页面包括两部分：【导航栏】和【主内容区】  
                
                2.2. **导航栏设计**
                - 导航栏完全复用模板代码, 禁止修改导航栏的颜色、图标、间距、布局（包括新增/删除导航项）。
                - 需要为【{page["page_name"]}】导航项【导航栏】中的 “激活状态”（如高亮样式），
                
                2.3. **主内容区设计**
                - 需要完全实现页面功能描述当中的所有功能点，允许扩展所需的其他的功能点。
                - 所有元素（按钮、输入框、下拉框等）仅实现静态 UI，**不绑定任何事件**（如 `onClick`、`onChange`、`onSubmit`）
                
                2.4. **其他要求**     
                - 图标需使用模板中已导入的库（如 lucide-react），且图标风格（大小、颜色）与模板中其他导航项保持一致 
                - 确保在浏览器当中可直接渲染，无大面积显示空白
                - 所有代码必须包裹在 ```jsx ``` 代码块中，代码块外无多余文本
                - 删除页面当中多余的提示文字
                
                ### 3. 【{page["module_name"]}】模板代码
                ```jsx
                {page["tmpl"]}
                ```
            """
    elif page["style"] == 1 or page["style"] == 2:
        

        prompt = f"""
                你需要基于【{page["module_name"]}】软件模块的模板代码，为【{page["page_name"]}】页面生成具体功能实现。
                
                ### 1. 页面基本信息
                - 软件名称：{page["web_title"]}
                - 页面所属模块：{page["module_name"]} （模板已包含统一导航栏）
                - 页面名称：{page["page_name"]}  （需在导航栏中激活对应项）
                - 页面功能描述：{page["page_desc"]}
                
                ### 2. 核心设计原则
                2.1. **页面设计**
                - 页面包括两部分：【导航栏】和【主内容区】  
                - 生成页面符合{"手机应用APP" if page["style"] == 1 else "手机微信小程序"}设计习惯
                    
                2.2. **导航栏设计**
                - 导航栏完全复用模板代码, 禁止修改导航栏的颜色、图标、间距、布局（包括新增/删除导航项）。
                - 需要为【{page["page_name"]}】导航项【导航栏】中的 “激活状态”（如高亮样式），
                    
                2.3. **主内容区设计**
                - 需要完全实现页面功能描述当中的所有功能点，允许扩展所需的其他的功能点。
                - 所有元素（按钮、输入框、下拉框等）仅实现静态 UI，**不绑定任何事件**（如 `onClick`、`onChange`、`onSubmit`）
                    
                2.4. **其他要求**     
                - 图标需使用模板中已导入的库（如 lucide-react），且图标风格（大小、颜色）与模板中其他导航项保持一致 
                - 确保在浏览器当中可直接渲染，无大面积显示空白
                - 所有代码必须包裹在 ```jsx ``` 代码块中，代码块外无多余文本
                - 删除页面当中多余的提示文字
                - 页面不要出现渲染不全的情况
                - 手机软件APP当中出现的滚动条，统一设置CSS样式::-webkit-scrollbar 为3px宽
                    
                ### 3. 【{page["module_name"]}】模板代码
                ```jsx
                {page["tmpl"]}
                ```
            """               
    return prompt


def build_module_prompt(module:dict):
    if module["style"] == 0:
        prompt = f"""
                你需要为【{module["web_title"]}】系统的【{module["module_name"]}】模块生成对应 React 代码模板（JSX），请参考以下参考模板代码，同时严格遵循以下规则，确保后续的所有页面级实现可以直接复用此模板的导航栏与风格：。

                ### 1. 模块基本信息
                - 系统名称：{module["web_title"]}
                - 模块名称：{module["module_name"]}
                - 包含页面（导航项）：{", ".join(module["module_pages"])}

                ### 2. 核心设计原则
                2.1. **页面设计**：
                - 页面包括两部分：【导航栏】（顶部/左侧，与参考模板位置一致）+ 【主内容区】（导航栏右侧/下方）
                - 当前仅实现【导航栏】的完整UI，【主内容区】仅留空占位，不做任何功能设计

                2.2. **导航栏设计**
                - 导航栏需要包括：（{", ".join(module["module_pages"])}），但仅展示导航项【名称】与【图标】，不实现具体跳转逻辑
                - 不实现导航项的点击、hover 等任何交互逻辑，导航项仅为静态展示（无 `onClick`、`active` 状态）
                
                2.3. **主内容区设计**
                - 所有需要后续页面级实现的部分全部留空

                2.4. **其他要求**：
                - 依赖导入：根据该模块的功能，导入所需的包，包含`React`、图标库（如`lucide-react`）等必要依赖
                - 所有JSX代码务必使用 ```jsx ``` 代码块，无多余文本。
                - 布局与配色参考模板代码
                
                ### 3. 参考模板代码
                ``` jsx
                {module["tmpl"]}
                ```
            """
    elif module["style"] == 1 or module["style"] == 2:
        prompt = f"""
                你需要为【{module["web_title"]}】软件的【{module["module_name"]}】模块生成对应 React 代码模板（JSX），请参考以下参考模板代码，同时严格遵循以下规则，确保后续的所有页面级实现可以直接复用此模板的导航栏与风格：。

                ### 1. 模块基本信息
                - 软件名称：{module["web_title"]}
                - 模块名称：{module["module_name"]}
                - 包含页面（导航项）：{", ".join(module["module_pages"])}
                {"- 不要修改参考模板代码当中的样式内容，如状态栏，右上椭圆容器等。" if module["style"] == 2 else ""}
                
                ### 2. 核心设计原则
                2.1. **页面设计**：
                - 页面包括两部分：【导航栏】（上方/下方）+ 【主内容区】
                - 当前仅实现【导航栏】的完整UI，【主内容区】仅留空占位，不做任何功能设计
                - 生成页面符合手机APP设计习惯

                2.2. **导航栏设计**
                - 导航栏需要包括：（{", ".join(module["module_pages"])}），但仅展示导航项【名称】与【图标】，不实现具体跳转逻辑
                - 不实现导航项的点击、hover 等任何交互逻辑，导航项仅为静态展示（无 `onClick`、`active` 状态）
                
                2.3. **主内容区设计**
                - 所有需要后续页面级实现的部分全部留空

                2.4. **其他要求**：
                - 依赖导入：根据该模块的功能，导入所需的包，包含`React`、图标库（如`lucide-react`）等必要依赖
                - 所有JSX代码务必使用 ```jsx ``` 代码块，无多余文本。
                - 布局与配色参考模板代码
                - 当前软件为 {"手机应用APP" if module["style"] == 1 else "手机微信小程序"}，整体符合手机的16:9布局
                
                ### 3. 参考模板代码
                ``` jsx
                {module["tmpl"]}
                ```
            """
    return prompt