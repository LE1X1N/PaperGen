import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from multiprocessing import Process, Lock, Queue
from openai import APIConnectionError, InternalServerError
from requests.exceptions import ConnectTimeout

from src.errors import *
from src.config import conf
from src.llm import call_chat_completion
from src.browser import launch_sandbox_demo
from src.browser import  init_driver, capture_screenshot
from src.utils import get_random_available_port, wait_for_port, get_logger, get_generated_files

from .data_parser import DataParser
from .tmpl_manager import TemplateManager
from .progress_manager import ProgressManager, ProcessStatus
from .upload_manager import UploadManager

logger = get_logger()

class TaskManager:
    def __init__(self):
        self.parser = DataParser(tmpl_manager=TemplateManager())
        self.progress_manager = ProgressManager(base_dir=conf["screenshot_dir"])
        self.upload_manager = UploadManager()
        
        self.executor = ThreadPoolExecutor(conf["max_workers"])
        

    def process_tasks(self, request_id: str, data: dict, task_id: str) -> list:
        """
            Multi-thread processing tasks
            
            MainThread(输入JSON -> 数据解析) 
                -> Thread(Prompt构建 -> 代码生成 -> 截屏渲染 -> 输出图片) 
            -> MainThread(结果保存)
        """
        start_time = time.time()
        
        # 1. Images save dir
        self.progress_manager.init_request(request_id, data, task_id)
        # logger.info(f"Request ID: {request_id} ->: 开始处理请求，状态文件存储路径：{file_path}")
        
        # 2. module-level tasks       
        try:
            tasks = self.parser.parse_module(request_id, data)
            logger.info(f"Request ID: {request_id}: 开始模块级别模板生成! 任务数量：{len(tasks)}")
            futures = [self.executor.submit(self._process_single_task, task) for task in tasks]
            gen_tmpls = [future.result() for future in futures]
        except KeyError as e:
            error_msg = f"【JSON解析错误】KeyError: {str(e)}"
            self.progress_manager.update_all_tasks(request_id, status=ProcessStatus.FAILED, url="", error=error_msg)

        # 3. page-level tasks
        tasks = self.parser.parse_page(request_id, data, gen_tmpls)
        futures = [self.executor.submit(self._process_single_task, task) for task in tasks]
        
        # traverse all tasks
        results = []  
        logger.info(f"Request ID: {request_id}: 开始页面级别代码生成！任务数量：{len(tasks)}")
        for future, task in zip(futures, tasks):
            try:
                result = future.result(timeout=conf["process_timeout"])
                
                if not result["status"]:
                    # fail
                    self.progress_manager.update_task_status(request_id, task["page_id"], ProcessStatus.FAILED, url="", error=result["message"])  
                else:
                    # try upload image
                    res = self.upload_manager.upload_single_file(result["message"])   #  upload image to file system
                    if res['code'] == 0:
                        download_url = conf["download_url_prefix"] + res["result"]
                        self.progress_manager.update_task_status(request_id,  task["page_id"],  ProcessStatus.SUCCESS, url=download_url)
                    else:
                        raise UploadError(res["message"])
                
            except TimeoutError as e:
                error_msg = f"【超时错误】TimeoutError： 超过任务最大时间：{conf["process_timeout"]} s"
                self.progress_manager.update_task_status(request_id, task["page_id"], ProcessStatus.FAILED, "", error_msg)

            except UploadError as e:
                error_msg = f"【上传错误】UploadError: {str(e)}"
                self.progress_manager.update_task_status(request_id, task["page_id"], ProcessStatus.FAILED, "", error_msg)
                
        logger.info(f"Request ID: {request_id} -> 处理请求完成！共耗时 {time.time() - start_time} s")
        return results
    

    def _process_single_task(self, task: dict) -> dict:
        # 1.  parse data
        request_id = task["request_id"]
        page_id = task["page_id"]
        return_code = task["return_code"]
        query = task["query"]
        logger.info(f"Request ID: {request_id} -> Task_{page_id}: ********* 任务 {page_id} 开始！*********")

        # 2. create messages
        messages = [{"role": 'system', "content": conf["system_prompt"]}]
        messages.append({"role": "user", "content": query})

        # Multi-turn generation
        render_success = False
        for turn in range(conf["max_retries"]):
            logger.info(f"Request ID: {request_id} -> Task_{page_id}: 进行第 {turn + 1} 轮尝试...")

            try:
                start_time = time.time()
                browser = None  
                driver = None   
                
                # 3. code generation
                res = call_chat_completion(messages)
                messages.append({"role": "assistant", "content": res})
                logger.info(
                    f"Request ID: {request_id} -> Task_{page_id}: 代码生成成功！耗时：{time.time() - start_time} s")

                # 4. Code check
                generated_files = get_generated_files(res)
                react_code = generated_files.get("index.tsx") or generated_files.get("index.jsx")

                # 4. Launch browser to render react
                port = get_random_available_port()  # a random port to bind with gradio
                logger.info(f"Request ID: {request_id} ->, Task ID: {page_id}, Gradio Port: {port}")

                browser_registry = Queue()  #  communication between main process and browser process
                browser_lock = Lock()

                browser = Process(target=launch_sandbox_demo,
                                  args=(request_id, page_id, res, port, browser_registry, browser_lock, logger), name="Browser Process")
                browser.start()

                # wait port connected (15s)
                if not wait_for_port(port, timeout=conf["connect_timeout"]):
                    raise ConnectionRefusedError("Gradio端口连接失败")
                logger.info(f"Request ID: {request_id} -> Task_{page_id}: Gradio 初始化成功！")

                # 5. Try screenshot
                driver = init_driver()
                driver.get(f'http://localhost:{port}')
                logger.info(f"Request ID: {request_id} -> Task_{page_id}: Chrome driver 初始化成功！")

                # wait rendering 
                for _ in range(conf["render_timeout"]):
                    with browser_lock:
                        logger.info(f"Request ID: {request_id} -> Task_{page_id}: 检查渲染状态...")
                        if not browser_registry.empty():
                            completed_flag = browser_registry.get()

                            if completed_flag != page_id:
                                # render / compile error
                                render_success = False
                                raise FrontendError(completed_flag)

                            if completed_flag == page_id:
                                # compile success
                                wait_rounds = 0
                                while wait_rounds < 3:
                                    logger.info(
                                        f"Request ID: {request_id} -> Task_{page_id}: 编译成功，等待渲染成功信号...")
                                    if not browser_registry.empty():
                                        new_flag = browser_registry.get()
                                        if new_flag != page_id:
                                            raise FrontendError(new_flag)
                                    wait_rounds += 1
                                    time.sleep(1)

                                logger.info(f"Request ID: {request_id} -> Task_{page_id}: 【渲染成功】 前端代码渲染成功！")
                                if not return_code:
                                    img_path = capture_screenshot(request_id, page_id, driver, save_dir=self.progress_manager._get_request_dir(request_id))
                                    logger.info(f"Request ID: {request_id} -> Task ID_{page_id}: Selenium 截图已保存至 {img_path}")
                                
                                render_success = True
                                break
                    time.sleep(1)

                if not render_success:
                    raise TimeoutError("Gradio渲染超时！")

            except FrontendError as e:
                logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【前端代码错误】{e}")
                messages.append({"role": "user", "content": str(e)})
            except TimeoutError as e:
                logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【Gradio渲染超时错误】{e}")
                messages.pop()  # exclude assistant generated code
            except ConnectionRefusedError as e:
                logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【Gradio端口连接错误】{e}")
            except (APIConnectionError, InternalServerError)  as e:
                logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【OpenAI服务端连接错误】{e}")
            except Exception as e:
                logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【其他错误】{e}")
            finally:
                if browser:
                    browser.kill()
                    logger.info(
                        f"Request ID: {request_id} -> Task_{page_id}: Gradio浏览器 退出! 错误码: {browser.exitcode}")

                if driver:
                    driver.close()
                    driver.quit()
                    logger.info(f"Request ID: {request_id} -> Task_{page_id}: Chrome Driver 退出!")

            # exit judge
            if render_success:
                logger.info(f"Request ID: {request_id} -> Task_{page_id}: 第 {turn + 1} 轮成功！")
                break
            else:
                logger.info(f"Request ID: {request_id} -> Task_{page_id}: 第 {turn + 1} 轮失败！")

        
        if not render_success:
            return {"page_id": page_id, "status": False, "message": "任务超过最大重试次数"}
        
        if return_code:
            return {"page_id": page_id, "status": True, "message": react_code}    # module level task

        else:
            return {"page_id": page_id, "status": True, "message": img_path}      # page level task  
