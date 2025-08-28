import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from multiprocessing import Process, Lock, Queue

from src.errors import *
from src.config import conf
from src.llm import call_chat_completion, SYSTEM_PROMPT
from src.browser import launch_sandbox_demo, wait_for_render
from src.browser import  init_driver, capture_screenshot
from src.utils import get_random_available_port, wait_for_port, get_logger, get_generated_files

from .data_processing.json_parser import DataParser
from .progress_manager import ProgressManager, ProgressStatus
from .storage import upload_single_file

logger = get_logger()


class TaskManager:
    def __init__(self):
        self.parser = DataParser()
        self.progress_manager = ProgressManager(base_dir=conf["service"]["local_file_dir"])
        
        # global thread pool
        if not hasattr(TaskManager, 'global_executor'):
            TaskManager.global_executor = ThreadPoolExecutor(conf["service"]["max_workers"], thread_name_prefix="GlobalThreadPool-")
        
    def process_tasks(self, request_id: str, data: dict, task_id: str):
        """
            Multi-thread processing tasks
            
            MainThread(输入JSON -> 数据解析) 
                -> Thread(Prompt构建 -> 代码生成 -> 截屏渲染 -> 输出图片) 
            -> MainThread(结果保存)
        """
        start_time = time.time()

        # 1. Images save dir
        self.progress_manager.init_request(request_id, data, task_id)
            
        # 2. module-level tasks       
        tasks = self.parser.parse_module(request_id, data)
        logger.info(f"Request ID: {request_id}: 开始模块级别模板生成! 任务数量：{len(tasks)}")
        futures = [TaskManager.global_executor.submit(self._process_single_task, task) for task in tasks]
        gen_tmpls = [future.result() for future in futures]

        # 3. page-level tasks
        tasks = self.parser.parse_page(request_id, data, gen_tmpls)
        futures = [TaskManager.global_executor.submit(self._process_single_task, task) for task in tasks]
            
        # traverse all tasks
        logger.info(f"Request ID: {request_id}: 开始页面级别代码生成！任务数量：{len(tasks)}")
        for future, task in zip(futures, tasks):
            try:
                res = future.result(timeout=conf["service"]["process_timeout_sec"])
                error_msg = None
            
            except OpenAIError as e:
                error_msg = f"【OpenAI错误】{e}"
            except ChromeError as e:    
                error_msg = f"【Chrome错误】{e}"  
            except FileSystemError as e:
                error_msg = f"【DFS错误】{e}"  
            except TimeoutError as e:
                error_msg = f"【超时错误】： 生成超过任务最大时间 {conf["service"]["process_timeout_sec"]} s"
            except UploadError as e:
                error_msg = f"【上传错误】{e}"
            except MaxRetriesExceededError as e:
                error_msg = f"【重试次数超限错误】{e}"
            except Exception as e:
                error_msg = f"【其他错误】{e}"
                
            finally:
                # update task status
                if error_msg:
                    self.progress_manager.update_task_status(request_id, task["page_id"], ProgressStatus.FAILED, url="", error=error_msg)
                else:
                    self.progress_manager.update_task_status(request_id,  task["page_id"],  ProgressStatus.SUCCESS, url=res)
                    
        logger.info(f"Request ID: {request_id} -> 处理请求完成！共耗时 {time.time() - start_time} s")
    

    def _process_single_task(self, task: dict) -> dict:
         
        # 1. parse data
        request_id = task["request_id"]
        page_id = task["page_id"]
        return_code = task["return_code"]
        query = task["query"]
        logger.info(f"Request ID: {request_id} -> Task_{page_id}: ********* 任务 {page_id} 开始！*********")

        # 2. create messages
        messages = [{"role": 'system', "content": SYSTEM_PROMPT}]
        messages.append({"role": "user", "content": query})

        # Multi-turn generation
        for turn in range(conf["service"]["max_retries"]):
            logger.info(f"Request ID: {request_id} -> Task_{page_id}: 进行第 {turn + 1} 轮尝试...")

            try:
                start_time = time.time()
                browser = None  
                driver = None   
                
                # 3. code generation
                res = call_chat_completion(messages)
                messages.append({"role": "assistant", "content": res})
                logger.info(f"Request ID: {request_id} -> Task_{page_id}: 代码生成成功！耗时：{time.time() - start_time} s")

                # 4. Code check
                generated_files = get_generated_files(res)
                react_code = generated_files.get("index.tsx") or generated_files.get("index.jsx")
                
                # 5. Launch browser to render react code
                browser_registry = Queue()      #  communication between main process and browser process
                browser_lock = Lock()

                port = get_random_available_port()        # random port
                browser = Process(target=launch_sandbox_demo,
                                  args=(request_id, page_id, react_code, port, browser_registry, browser_lock, logger), name="BrowserProcess")
                browser.start()

                # 6. wait port connected (15s)
                wait_for_port(port, timeout=conf["service"]["connect_timeout_sec"])
                logger.info(f"Request ID: {request_id} -> Task_{page_id}: Gradio 初始化成功！绑定端口: {port}")

                # 7. init chrome driver
                driver = init_driver()
                driver.get(f'http://localhost:{port}')
                logger.info(f"Request ID: {request_id} -> Task_{page_id}: Chrome driver 初始化成功！")

                # 8. wait rendering (25s)
                wait_for_render(request_id, page_id, conf["service"]["render_timeout_sec"], browser_registry, browser_lock, logger)
                logger.info(f"Request ID: {request_id} -> Task_{page_id}: 第 {turn + 1} 轮成功！")
                
                # 9. module level task, return generated module-level templates
                self.progress_manager.save_code(request_id, page_id, react_code)
                if return_code:
                    return react_code  
                
                # 10. capture screenshot and upload
                img_path = capture_screenshot(request_id, page_id, driver, save_dir=self.progress_manager._get_request_dir(request_id))
                logger.info(f"Request ID: {request_id} -> Task_{page_id}: Selenium 截图已保存至 {img_path}")
                res = upload_single_file(img_path)        #  upload to file system
                logger.info(f"Request ID: {request_id} -> Task_{page_id}: 【任务成功】上传文件访问路径：{res}")
                return res   

            except FormatError as e:
                logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【输出格式错误】{e}")
                messages.append({"role": "user", "content": str(e)})
            except PortTimeoutError as e:
                logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【Gradio端口连接错误】{e}")    
            except FrontendError as e:
                logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【前端代码错误】{e}")
                messages.append({"role": "user", "content": str(e)})
            except RenderTimeoutError as e:
                logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【Gradio渲染超时错误】{e}")
                
            except OpenAIError:
                raise
            except ChromeError:    
                raise
            except FileSystemError:
                raise
            except Exception:
                raise
             
            finally:
                if browser:
                    browser.kill()
                    logger.info(f"Request ID: {request_id} -> Task_{page_id}: Gradio浏览器 退出! 错误码: {browser.exitcode}")
                    
                if driver:
                    driver.close()
                    driver.quit()
                    logger.info(f"Request ID: {request_id} -> Task_{page_id}: Chrome Driver 退出!")
                    
                    
        raise MaxRetriesExceededError(f"任务超过最大重试次数: {conf["service"]["max_retries"]}")
