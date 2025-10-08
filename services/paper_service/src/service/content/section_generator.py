from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from src.llm.prompt import PAPER_MAIN_BODY_PROMPT
from src.llm.client import call_chat_completion


def generate_main_body_text(title: str=None, structure: dict=None):

    def _generate_section_text(title: str=None, section: str=None, structure: dict=None) -> str:
        messages = [
            {'role': 'assistant', 'content': PAPER_MAIN_BODY_PROMPT},
            {'role': 'user', 'content': f"请分析论文题目《{title}》，当前需要生成的章节为： {section}。你可参考该论文的论文结构：{str(structure)}"}
        ]    
        res = call_chat_completion(messages)
        res = res.split("\n\n")
        return res

    start_time = time.time()

    # generate main body of docx
    tasks = {}
    
    for chapter in structure["chapters"]:
        # 1-level
        if "sections" not in chapter:
            tasks[chapter["title"]] = chapter["title"]

        # 2-level
        else:
            for section in chapter["sections"]:
                if "subsections" not in section:
                    tasks[section["title"]] = f"{chapter['title']} -> {section['title']}"

                # 3-level 
                else:
                    for subsection in section["subsections"]:
                        tasks[subsection["title"]] = f"{chapter['title']} -> {section['title']} -> {subsection['title']}"
    
    # multithread
    res_map = {}
    future_to_keys = {}
    task_execuator = ThreadPoolExecutor(max_workers=10)
    for k, v in tasks.items():
        future = task_execuator.submit(_generate_section_text, title=title, section=v, structure=structure)
        future_to_keys[future] = k

    for future in as_completed(future_to_keys):
        res = future.result()
        res_map[future_to_keys[future]] = res
    
    print(f"论文正文生成成功，耗时：{time.time() - start_time} s")
    return res_map


def generate_tables(title: str=None, table_desc: dict=None):
    pass
