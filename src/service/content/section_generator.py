from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from typing import List

from src.llm.prompt import PAPER_MAIN_BODY_PROMPT, PAPER_TABLE_PROMPT
from src.llm.client import call_chat_completion


async def generate_main_body_text(title: str=None, structure: dict=None, tables_desc: dict=None):

    def _generate_section_text(query: str) -> List[str]:
        messages = [
            {'role': 'assistant', 'content': PAPER_MAIN_BODY_PROMPT},
            {'role': 'user', 'content': query}
        ]    
        res = call_chat_completion(messages)
        res = res.split("\n\n")
        return res
    
    def _generate_query(section: str, section_table_map: dict=None) -> str:
        if section not in section_table_map:
            return f"请分析论文题目《{title}》，当前需要生成的章节为： {section}。你可参考该论文的论文结构：{str(structure)}"
        else:
            return f"请分析论文题目《{title}》，当前需要生成的章节为： {section}。当前章节包含图表：{section_table_map[section]},你需要在生成的内容中通过 ``见表X-X``的方式来引用表中的内容。 本论文的论文结构为：{str(structure)}。"

    # parsing table
    section_table_map = {}
    for k, v in tables_desc.items():
        table_info = "".join([f"【表id: {table["id"]} 表描述： {table["desc"]}】" for table in v])
        section_table_map[k] = table_info

    tasks = {}
    res_map = {}
    
    # pasing into tasks
    for chapter in structure["chapters"]:
        # 1-level
        if "sections" not in chapter:
            tasks[chapter["title"]] = _generate_query(chapter["title"], section_table_map)
            
        # 2-level
        else:
            for section in chapter["sections"]:
                if "subsections" not in section:
                    tasks[section["title"]] = _generate_query(f"{section['title']}", section_table_map)

                # 3-level 
                else:
                    for subsection in section["subsections"]:
                        tasks[subsection["title"]] = _generate_query(f"{subsection['title']}", section_table_map)
    
    # multithread
    future_to_keys = {}
    task_execuator = ThreadPoolExecutor(max_workers=10)
    for k, v in tasks.items():
        future = task_execuator.submit(_generate_section_text, v)
        future_to_keys[future] = k

    for future in as_completed(future_to_keys):
        res = future.result()
        res_map[future_to_keys[future]] = res
    return res_map


async def generate_tables(title: str=None, tables_desc: dict=None):
    
    def _generate_query(table: dict) -> str:
        return f"请分析论文题目《{title}》，根据需求生成对应的表数据。当前需要生成的表ID为：【{table['id']}】, 该表描述为：{table['desc']}"
    
    def _generate_table(query: str | List ):

        if isinstance(query, str):
            query = [query]

        res = []
        for q in query:
            messages = [
                {'role': 'assistant', 'content': PAPER_TABLE_PROMPT},
                {'role': 'user', 'content': q}
            ] 
            try:
                ret_json = json.loads(call_chat_completion(messages))
                res.append(ret_json)
            except Exception: 
                print("JSON解析失败")
        return res
    
    
    # generate tables (JSON-format) based on corresponding description  
    tasks = {}
    res_map = {}

    # parsing to tasks
    for k, v in tables_desc.items():
        query = [_generate_query(table) for table in v]
        tasks[k] = query

    # execute
    future_to_keys = {}
    task_execuator = ThreadPoolExecutor(max_workers=10)
    for k, v in tasks.items():
        future = task_execuator.submit(_generate_table, v)
        future_to_keys[future] = k

    for future in as_completed(future_to_keys):
        res = future.result()
        res_map[future_to_keys[future]] = res
    
    return res_map


