import time

import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms
import modelscope_studio.components.pro as pro

from src.errors import FrontendError, RenderTimeoutError


react_import = {
    # UI框架
    "semantic-ui-react": "https://esm.sh/semantic-ui-react@2.1.5",
    "semantic-ui-css": "https://esm.sh/semantic-ui-css@2.5.0",
    # 样式工具
    "styled-components": "https://esm.sh/styled-components@6.1.19",
    "@tailwindcss/browser": "https://esm.sh/@tailwindcss/browser@4.1.11",
    # 图标库
    "lucide-react": "https://esm.sh/lucide-react@0.525.0",
    # 动画引擎
    # "framer-motion": "https://esm.sh/framer-motion@12.23.6",
    "matter-js": "https://esm.sh/matter-js@0.20.0",
    # 3D 引擎  
    "three": "https://esm.sh/three@0.178.0",
    "@react-three/fiber": "https://esm.sh/@react-three/fiber@9.2.0",
    "@react-three/drei": "https://esm.sh/@react-three/drei@10.5.2",
    # 数据可视化
    "echarts": "https://esm.sh/echarts@6.0.0",
    "recharts": "https://esm.sh/recharts@3.1.0",
    "konva": "https://esm.sh/konva@9.3.22",
    "react-konva": "https://esm.sh/react-konva@19.0.7",
    "p5": "https://esm.sh/p5@2.0.3",
    # 工具库
    "dayjs": "https://esm.sh/dayjs",
}

def launch_sandbox_demo(request_id, page_id, react_code, port, browser_registry=None, logger=None, *args):
    """
        Sandbox based on modelscope_studio sandboxs
        
    """
    # compile / render 
    def handle_compile_error(e: gr.EventData):
        """ Compile Error """
        error_msg = f"【编译错误】：{e._data['payload'][0]}"
        if logger:
            logger.error(f"Request ID: {request_id} -> Task_{page_id}: {error_msg}")
        if browser_registry:
            browser_registry.put(error_msg)  # error flag

    def handle_render_error(e: gr.EventData):
        """ Render error """
        error_msg = f"【渲染错误】：{e._data['payload'][0]}"
        if logger:
            logger.error(f"Request ID: {request_id} -> Task_{page_id}: {error_msg}")
        if browser_registry:
            browser_registry.put(error_msg)  # error flag

    def handle_compile_success():
        """ Compile Success """
        msg = f"代码编译成功，无语法错误，开始渲染..."
        if logger:
            logger.info(f"Request ID: {request_id} -> Task_{page_id}:{msg}")
        if browser_registry is not None:
            browser_registry.put(page_id)  # compile success flag

    with gr.Blocks() as demo:
        with ms.Application():
            with antd.ConfigProvider():
                # init sandbox
                sandbox = pro.WebSandbox(
                    height=1080,
                    template="react",
                    imports=react_import,
                    value={
                        "./index.tsx": """import Demo from './demo.tsx'
                                            import "@tailwindcss/browser"
                                            export default Demo
                                            """,
                        "./demo.tsx": react_code
                    },
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
        *args
    )
    return demo


def wait_for_render(request_id, page_id, timeout, browser_registry=None, logger=None):  
        
    for _ in range(timeout):
        logger.info(f"Request ID: {request_id} -> Task_{page_id}: 检查渲染状态...")
            
        if not browser_registry.empty():
            completed_flag = browser_registry.get()

            if completed_flag != page_id:
                # render / compile error
                raise FrontendError(completed_flag)

            if completed_flag == page_id:
                # compile success, wait for render success
                wait_rounds = 0
                while wait_rounds < 3:
                    logger.info(f"Request ID: {request_id} -> Task_{page_id}: 编译成功，等待渲染成功信号...")
                    if not browser_registry.empty():
                        new_flag = browser_registry.get()
                        if new_flag != page_id:
                            raise FrontendError(new_flag)
                    wait_rounds += 1
                    time.sleep(1)

                logger.info(f"Request ID: {request_id} -> Task_{page_id}: 前端代码渲染成功！")
                return True
        time.sleep(1)
        
    raise RenderTimeoutError(f"Gradio渲染超时，超过 {timeout} 秒未渲染成功！")
