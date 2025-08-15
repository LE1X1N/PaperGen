from typing import Dict, List, Optional, Tuple
import gradio as gr
import time
from dashscope.api_entities.dashscope_response import Role
import random
from openai import OpenAI

import modelscope_studio.components.base as ms
import modelscope_studio.components.legacy as legacy
import modelscope_studio.components.antd as antd
import modelscope_studio.components.pro as pro

from utils import *
from app_conf import SYSTEM_PROMPT, REACT_IMPORTS, SERVICE_NAME, DEMO_LIST, MODEL, PORT, BASE_URL, API_KEY

# logger
logger = setup_logger(SERVICE_NAME)

# open-ai client
client = OpenAI(
    base_url=BASE_URL,  
    api_key=API_KEY 
)

print(f"Service Port: {PORT}")
print(f"Model: {MODEL}")


class GradioEvents:
    
    @staticmethod
    def generation_code(query: Optional[str], _setting: Dict[str, str], _history: Optional[History], task_id: Optional[int]=None):  
        if query is None:
            query = ""
        if _history is None:
            _history = []

        if task_id is None:
            task_id = random.randint(1000, 9999)
        else:
            logger.info(f"Task_{task_id} 模型再次生成开始...")                

        messages = history_to_messages(_history, _setting["system"])
        messages.append({"role": Role.USER, "content": query})
    
        # OpenAI compatible generation
        gen = client.chat.completions.create(
                model=MODEL,  
                messages=messages, 
                stream=True,
            )

        full_content = "" 
        start_time = time.time()
        
        for chunk in gen:
            if len(chunk.choices) == 0:
                # chat completion
                break
            
            content = chunk.choices[0].delta.content or ""
            full_content += content

            finish_reason = chunk.choices[0].finish_reason
                        
            if finish_reason == "stop":
                # finish state
                _history = messages_to_history(
                    messages + [{"role": "assistant", "content": full_content}]
                )
                # print("history")
                # print(_history)
                
                logger.info(f"Task_{task_id} 模型生成成功，耗时 {time.time() - start_time} 秒.")
                            
                generated_files = get_generated_files(full_content)
                react_code = generated_files.get("index.tsx") or generated_files.get("index.jsx")
                html_code = generated_files.get("index.html")
                            
                yield {
                    code_output: full_content,
                    history: _history,
                    # sandbox: send_to_sandbox(remove_code_block(full_content)),                  
                    sandbox: gr.update(template="react" if react_code else "html",
                                        imports=REACT_IMPORTS if react_code else {},
                                        height=700,
                                        value={
                                            "./index.tsx": """import Demo from './demo.tsx'
                                                            import "@tailwindcss/browser"
                                                            export default Demo
                                                            """,
                                            "./demo.tsx": react_code
                                            } if react_code else {"./index.html": html_code},
                                        ),
                    state_tab: gr.update(active_key="render"),
                    code_drawer: gr.update(open=False),
                    current_task_id: task_id,
                }
            else:
                # loading state
                yield {
                    code_output: full_content,  
                    state_tab: gr.update(active_key="loading"),
                    code_drawer: gr.update(open=True),
                    current_task_id: task_id,
                }
    
    
    @staticmethod
    def history_render(history: History):
        return gr.update(open=True), history

    @staticmethod
    def clear_history():
        gr.Success("History Cleared.", duration=5)
        return [], ""

    @staticmethod
    def demo_card_click(e: gr.EventData, ):
        index = e._data["component"]["index"]
        return DEMO_LIST[index]["prompt"]

    @staticmethod
    # Handle Sandbox compile or render error
    def handle_compile_success(e: gr.EventData, task_id: int):
        logger.info(f"Task_{task_id}:【编译成功】: 代码编译成功，无语法错误，开始渲染...")
        gr.Success(f"界面编译成功！", duration=5)
         
        yield {
            input: gr.update(
                        value = None,
                        placeholder="请描述需要修改的地方：",
                        elem_style={"height": "200px"} 
                    )
        }

    @staticmethod
    def handle_compile_error(e: gr.EventData, task_id: int, _setting: Dict[str, str], _history: Optional[History],):
        # Frontend compile error
        error_prompt = f"【编译错误】：{e._data['payload'][0]}"
        logger.error(f"Task_{task_id} {error_prompt}")
        gr.Warning(f"界面编译失败！正在重新进行代码生成...", duration=20)
        # regenerate code
        yield from GradioEvents.generation_code(error_prompt, _setting, _history, task_id)

    @staticmethod
    def handle_render_error(e: gr.EventData, task_id: int, _setting: Dict[str, str], _history: Optional[History],):
        # Frontend render error
        error_prompt = f"【渲染错误】：{e._data['payload'][0]}"
        logger.error(f"Task_{task_id} :{error_prompt}")
        gr.Warning(f"界面渲染失败！正在重新进行代码生成...", duration=20)
        
        # regenerate code
        yield from GradioEvents.generation_code(error_prompt, _setting, _history, task_id)
        

with gr.Blocks(css_paths="demo/app_style.css") as demo:
    # gradio state
    history = gr.State([])      # chat history
    setting = gr.State({"system": SYSTEM_PROMPT,})
    current_task_id = gr.State("")      # task 
    # render_success = gr.State(False)     # render success flat

    with ms.Application() as app:
        with antd.ConfigProvider():
            with antd.Row(gutter=[32, 12]) as layout:
                
                """Left side (input area)"""
                with antd.Col(span=24, md=8):
                    with antd.Flex(vertical=True, gap="middle", wrap=True):
                        # header
                        header = gr.HTML(
                            """
                                <div class="left_header">
                                    <h1>网站界面设计</h2>
                                </div>
                            """
                        )
                        
                        # input
                        input = antd.InputTextarea(
                            size="large",
                            allow_clear=True,
                            placeholder="Please enter what kind of application you want",
                            elem_style={"height": "200px"},
                            elem_id="input-container"
                        )
                        submit_btn = antd.Button("发送", type="primary", size="large", elem_id="submit-btn")
                        clear_btn = antd.Button("清除对话记录", type="default", size="large", danger=True, elem_id="clear-btn")

                        # examples
                        antd.Divider("应用案例")
                        with antd.Flex(gap="small", wrap=True, elem_id="demo_container"):
                            with ms.Each(DEMO_LIST):
                                with antd.Card(hoverable=True, as_item="card" ) as demoCard:
                                    antd.CardMeta()
                                demoCard.click(GradioEvents.demo_card_click, outputs=[input])
                        
                        # settings
                        antd.Divider("设置")
                        with antd.Flex(gap="small", wrap=True):
                            settingPromptBtn = antd.Button("⚙️ 设置系统提示词", type="default")
                            # codeBtn = antd.Button("🧑‍💻 浏览代码", type="default")
                            # historyBtn = antd.Button("📜 对话历史", type="default")
                            tour_btn = antd.Button("💡 使用教程", type="default")

                    # set system Prompt buttons
                    with antd.Modal(
                        open=False, title="set system Prompt", width="800px"
                    ) as system_prompt_modal:
                        systemPromptInput = antd.InputTextarea(
                            SYSTEM_PROMPT, auto_size=True
                        )

                    settingPromptBtn.click(
                        lambda: gr.update(open=True),
                        inputs=[],
                        outputs=[system_prompt_modal],
                    )
                    
                    # System Prompt set
                    system_prompt_modal.ok(
                        lambda input: ({"system": input}, gr.update(open=False)),
                        inputs=[systemPromptInput],
                        outputs=[setting, system_prompt_modal],
                    )
                    system_prompt_modal.cancel(
                        lambda: gr.update(open=False), outputs=[system_prompt_modal]
                    )

                    # Code Drawer
                    with antd.Drawer(open=False, title="code", placement="left", width="750px") as code_drawer:
                        code_output = legacy.Markdown()
                        
                    code_drawer.close(
                        lambda: gr.update(open=False), inputs=[], outputs=[code_drawer]
                    )

                    # History Drawer
                    with antd.Drawer(open=False, title="history", placement="left", width="900px") as history_drawer:
                        history_output = legacy.Chatbot(
                            show_label=False,
                            flushing=False,
                            height=960,
                            elem_classes="history_chatbot",
                        )

                    history_drawer.close(
                        lambda: gr.update(open=False),
                        inputs=[],
                        outputs=[history_drawer],
                    )
                    
                    

                """ Right side (output area) """
                with antd.Col(span=24, md=16):
                    with ms.Div(elem_classes="right_panel"):
                        
                        with antd.Card(title="Output",
                                        elem_style=dict(height="100%",
                                        display="flex",
                                        flexDirection="column"),
                                        styles=dict(body=dict(height=0, flex=1)),
                                        elem_id="output-container",
                                        ):
                        
                            # header
                            with ms.Slot("extra"):
                                with ms.Div(elem_id="output-container-extra"):
                                    with antd.Button("Download Code",
                                                    type="link",
                                                    href_target="_blank",
                                                    disabled=True,
                                            ) as download_btn:
                                                with ms.Slot("icon"):
                                                    antd.Icon("DownloadOutlined")
                                    # download_content = gr.Text(visible=False)
                                    code_btn = antd.Button("🧑‍💻 浏览代码", type="default")
                                    history_btn = antd.Button("📜 对话历史", type="default")
                            
                            # fake chrome btn
                            gr.HTML('<div class="render_header"><span class="header_btn"></span><span class="header_btn"></span><span class="header_btn"></span></div>')                          
                            
                            # tabs for different states
                            with antd.Tabs(active_key="empty", render_tab_bar="() => null") as state_tab:
                                # 1. empty
                                with antd.Tabs.Item(key="empty"):
                                    empty = antd.Empty(description="empty input", elem_classes="right_content")
                                # 2. loading
                                with antd.Tabs.Item(key="loading"):
                                    loading = antd.Spin(True, tip="coding...", size="large", elem_classes="right_content")
                                # 3. render
                                with antd.Tabs.Item(key="render"):
                                    sandbox = pro.WebSandbox(
                                        height=700,
                                        elem_classes="output-html",
                                        template="html",
                                    )
                                    # error process
                                    sandbox.compile_error(GradioEvents.handle_compile_error, inputs=[current_task_id, setting, history], outputs=[code_output, history, sandbox, state_tab, code_drawer, current_task_id])
                                    sandbox.render_error(GradioEvents.handle_render_error, inputs=[current_task_id, setting, history], outputs=[code_output, history, sandbox, state_tab, code_drawer, current_task_id])
                                    sandbox.compile_success(GradioEvents.handle_compile_success, inputs=[current_task_id], outputs=[input])

                """ tour """
                with antd.Tour(open=False) as usage_tour:
                    antd.Tour.Step(
                        title="1️⃣ Step 1",
                        description="Describe the web application you want to create.",
                        get_target=
                            "() => document.querySelector('#input-container')")
                    antd.Tour.Step(
                        title="2️⃣Step 2",
                        description="Click the submit button.",
                        get_target=
                            "() => document.querySelector('#submit-btn')")
                    antd.Tour.Step(
                        title="3️⃣Step 3",
                        description="Wait for the result.",
                        get_target=
                            "() => document.querySelector('#output-container')")
                    antd.Tour.Step(
                        title="4️⃣ Step 4",
                        description="Review the generated code and chat history.",
                        get_target=
                            "() => document.querySelector('#output-container-extra')")
                    antd.Tour.Step(
                        title="#️⃣Additional Settings",
                        description="You can delete chat history and start a new chat turn.",
                        get_target=
                            "() => document.querySelector('#clear-btn')")
                    antd.Tour.Step(
                        title="🚀Let's begin!🚀",
                        description="Choose a demo to start your journey in LangCoder!.",
                        get_target=
                            "() => document.querySelector('#demo_container')")
                    
            
            tour_btn.click(fn=lambda: gr.update(open=True), outputs=[usage_tour])
            gr.on(fn=lambda: gr.update(open=False),
                    triggers=[usage_tour.close, usage_tour.finish],
                    outputs=[usage_tour]
                )
            
            
            submit_btn.click(
                    GradioEvents.generation_code,
                    inputs=[input, setting, history],
                    outputs=[code_output, history, sandbox, state_tab, code_drawer, current_task_id],
                )

            clear_btn.click(GradioEvents.clear_history, inputs=[], outputs=[history, input])
            

            code_btn.click(lambda: gr.update(open=True), inputs=[], outputs=[code_drawer])
            history_btn.click(GradioEvents.history_render, inputs=[history], outputs=[history_drawer, history_output],)


if __name__ == "__main__":
    demo.launch(ssr_mode=False, share=False, debug=False, server_port=PORT)
