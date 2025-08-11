import gradio as gr
import logging
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms
import modelscope_studio.components.pro as pro

from config import REACT_IMPORTS, conf
from src.utils import get_generated_files

logger = logging.getLogger(conf["service_name"])

def launch_sandbox_demo(request_id, task_id, res, port, browser_registry, browser_lock):
    """
        Sandbox based on modelscope_studio sandboxs
    """
    
    generated_files = get_generated_files(res)
    react_code = generated_files.get("index.tsx") or generated_files.get("index.jsx")
    html_code = generated_files.get("index.html")
        
    # compile / render 
    def handle_compile_error(e: gr.EventData):
        """ Compile Error """
        error_prompt = f"【编译错误】：{e._data['payload'][0]}"
        logger.error(f"Request ID: {request_id} -> Task_{task_id} {error_prompt}")
        with browser_lock:
            browser_registry.put(error_prompt)  # error flag


    def handle_render_error(e: gr.EventData):
        """ Render error """
        error_prompt = f"【渲染错误】：{e._data['payload'][0]}"
        logger.error(f"Request ID: {request_id} -> Task_{task_id} :{error_prompt}")
        with browser_lock:
            browser_registry.put(error_prompt)  # error flag


    def handle_compile_success():
        """ Compile Success """
        logger.info(f"Request ID: {request_id} -> Task_{task_id}:【编译成功】: 代码编译成功，无语法错误，开始渲染...")
        with browser_lock:
            browser_registry.put(task_id)   # compile success flag
        
    with gr.Blocks() as demo:
        with ms.Application():
            with antd.ConfigProvider():
                # init sandbox
                sandbox = pro.WebSandbox(
                    height=1080,
                    template="react" if react_code else "html",
                    imports=REACT_IMPORTS,
                    value={
                        "./index.tsx": """import Demo from './demo.tsx'
                                            import "@tailwindcss/browser"
                                            export default Demo
                                            """,
                        "./demo.tsx": react_code
                    } if react_code else {"./index.html": html_code},
                )
                # trigger
                sandbox.compile_error(handle_compile_error)
                sandbox.render_error(handle_render_error)
                sandbox.compile_success(handle_compile_success)
        
    demo.launch(
        ssr_mode=False,
        share=False,
        debug=False,
        prevent_thread_lock=False,
        server_port=port,
        server_name="0.0.0.0",
        quiet=True,
    )
    
    return demo
