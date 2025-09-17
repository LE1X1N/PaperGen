import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from multiprocessing import Process, Lock, Queue

from src.errors import *
from src.config import conf
from src.llm import call_chat_completion, SYSTEM_PROMPT
from src.browser import launch_sandbox_demo, wait_for_render
from src.browser import  capture_screenshot, open_browser_page
from src.utils import get_random_available_port, wait_for_port, get_generated_files

from .data_processing import DataParser
from .progress import ProgressManager, ProgressStatus
from .storage import save_code, save_img, get_local_request_dir
from PIL import Image


def IsSolidColorImage(image_path, max_size=400, tolerance=0.92):
        
    with Image.open(image_path) as img:
        
        width, height = img.size
        if max(width, height) > max_size:
        
            scale = max_size / max(width, height)
            new_width = int(width * scale)
            new_height = int(height * scale)
        
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        gray_img = img.convert('L')  
        
        pixels = list(gray_img.getdata())
        total_pixels = len(pixels)
        pixel_counts = {}
        for p in pixels:
            pixel_counts[p] = pixel_counts.get(p, 0) + 1
        
        if not pixel_counts:
            return True
        
        max_count = max(pixel_counts.values())
        peak_ratio = max_count / float(total_pixels)
        
        return peak_ratio >= tolerance

class TaskManager:
    def __init__(self, logger=None):
        self.parser = DataParser(logger=logger)
        self.progress_manager = ProgressManager(logger=logger)
        self.logger = logger
        
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

        # 1. ini request status dict and dir
        self.progress_manager.init_request(request_id, self.parser.parse_page_ids(data), task_id)
        request_dir = get_local_request_dir(request_id)
        self.logger.info(f"Request ID: {request_id} ->: 状态JSON上传MongoDB成功") 
        self.logger.info(f"Request ID: {request_id} ->: 本地文件存储路径：{request_dir}") 
        
        # 2. module-level tasks       
        tasks = self.parser.parse_module(request_id, data)
        self.logger.info(f"Request ID: {request_id}: 开始模块级别模板生成! 任务数量：{len(tasks)}")
        futures = [TaskManager.global_executor.submit(self._process_single_task, task) for task in tasks]
        gen_tmpls = [future.result() for future in futures]

        # 3. page-level tasks
        tasks = self.parser.parse_page(request_id, data, gen_tmpls)
        future_to_task = {}
        for task in tasks:
            future = TaskManager.global_executor.submit(self._process_single_task, task) 
            future_to_task[future] = task
            
        # traverse all tasks
        self.logger.info(f"Request ID: {request_id}: 开始页面级别代码生成！任务数量：{len(tasks)}")
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            
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
            except MaxRetriesExceededError as e:
                error_msg = f"【重试次数超限错误】{e}"
            except Exception as e:
                error_msg = f"【其他错误】{e}"
                
            finally:
                # update task status
                if error_msg:
                    self.progress_manager.update_task_status(request_id, task["page_id"], ProgressStatus.FAILED, url="", error=error_msg) # fail
                else:
                    self.progress_manager.update_task_status(request_id,  task["page_id"],  ProgressStatus.SUCCESS, url=res)    # success
                    
        self.logger.info(f"Request ID: {request_id} -> 处理请求完成！共耗时 {time.time() - start_time} s")
    

    def _process_single_task(self, task: dict) -> dict:
        
        # 1. parse data
        request_id = task["request_id"]
        page_id = task["page_id"]
        return_code = task["return_code"]
        query = task["query"]
        self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: ********* 任务 {page_id} 开始！*********")

        # 2. create messages
        messages = [{"role": 'system', "content": SYSTEM_PROMPT}]
        messages.append({"role": "user", "content": query})

        # Multi-turn generation
        for turn in range(conf["service"]["max_retries"]):
            self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: 进行第 {turn + 1} 轮尝试...")

            try:
                start_time = time.time()
                gradio_process = None  
                playwright = None
                browser = None
                
                # 3. code generation
                res = call_chat_completion(messages)
                messages.append({"role": "assistant", "content": res})
                self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: 代码生成成功！耗时：{time.time() - start_time} s")

                # 4. Code check
                generated_files = get_generated_files(res)
                react_code = generated_files.get("index.tsx") or generated_files.get("index.jsx")
                
                # 5. Launch browser to render react code
                browser_registry = Queue()      #  communication between main process and browser process
                browser_lock = Lock()

                port = get_random_available_port()        # random port
                gradio_process = Process(target=launch_sandbox_demo,
                                  args=(request_id, page_id, react_code, port, browser_registry, browser_lock, self.logger), name="BrowserProcess")
                gradio_process.start()

                # 6. wait port connected (15s)
                wait_for_port(port, timeout=conf["service"]["connect_timeout_sec"])
                self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: Gradio 初始化成功！绑定端口: {port}")

                # 7. init chrome driver
                playwright, browser, page = open_browser_page(port)
                self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: Playwright Chrome 初始化成功！")

                # 8.  wait rendering (25s)
                wait_for_render(request_id, page_id, conf["service"]["render_timeout_sec"], browser_registry, browser_lock, self.logger)
                self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: 第 {turn + 1} 轮成功！")
                
                # 9. save jsx code
                code_path = save_code(request_id, page_id, react_code)
                self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: jsx 代码已保存至 {code_path}")

                if return_code:
                    return react_code  
                
                # 10. capture screenshot and save png image
                screenshot_img = capture_screenshot(page)
                img_path = save_img(request_id, page_id, screenshot_img)
                self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: 截图已保存至 {img_path}")

                if IsSolidColorImage(img_path):
                    self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: 是纯色图，未渲染成功")
                    raise
                
                return img_path

            except FormatError as e:
                self.logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【输出格式错误】{e}")
                messages.append({"role": "user", "content": str(e)})
            except PortTimeoutError as e:
                self.logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【Gradio端口连接错误】{e}")    
            except FrontendError as e:
                self.logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【前端代码错误】{e}")
                messages.append({"role": "user", "content": str(e)})
            except RenderTimeoutError as e:
                self.logger.error(f"Request ID: {request_id} -> Task_{page_id}: 【Gradio渲染超时错误】{e}")
                
            except OpenAIError:
                raise
            except ChromeError:    
                raise
            except FileSystemError:
                raise
            except Exception:
                raise
             
            finally:
                if gradio_process:
                    gradio_process.kill()
                    self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: Gradio进程退出! ")
                        
                if browser:
                    browser.close()
                if playwright:
                    playwright.stop()
                    self.logger.info(f"Request ID: {request_id} -> Task_{page_id}: Playwright退出!")

                    
        raise MaxRetriesExceededError(f"任务超过最大重试次数: {conf["service"]["max_retries"]}")
