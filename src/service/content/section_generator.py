from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from typing import List
import asyncio

from src.utils.common import parse_section_titles
from src.llm.prompt import PAPER_MAIN_BODY_PROMPT, PAPER_TABLE_PROMPT
from src.llm.client import call_chat_completion_async


async def generate_main_body_text(title: str=None, structure: dict=None, tables_desc: dict=None):

    async def _generate_section_text(query: str) -> List[str]:
        messages = [
            {'role': 'assistant', 'content': PAPER_MAIN_BODY_PROMPT},
            {'role': 'user', 'content': query}
        ]    
        res = await call_chat_completion_async(messages)
        res = res.split("\n\n")
        return res
    
    def _generate_query(section: str, section_table_map: dict=None) -> str:
        if section not in section_table_map:
            return f"请分析论文题目《{title}》，当前需要生成的章节为： {section}。你可参考该论文的论文结构：{str(parse_section_titles(structure))}"
        else:
            return f"请分析论文题目《{title}》，当前需要生成的章节为： {section}。当前章节包含图表：{section_table_map[section]},你需要在生成的内容中通过 ``见表X-X``的方式来引用表中的内容。 本论文的论文结构为：{str(parse_section_titles(structure))}。"

    # parsing table
    section_table_map = {}
    for k, v in tables_desc.items():
        table_info = "".join([f"【表id: {table["id"]} 表描述： {table["desc"]}】" for table in v])
        section_table_map[k] = table_info

    # pasing into tasks
    tasks = {}
    for chapter in structure["chapters"]:
        # 1-level
        if "sections" not in chapter:
            query = _generate_query(chapter["title"], section_table_map)
            tasks[chapter["title"]] = asyncio.create_task(_generate_section_text(query))

        # 2-level
        else:
            for section in chapter["sections"]:
                if "subsections" not in section:
                    query = _generate_query(f"{section['title']}", section_table_map)
                    tasks[section['title']] = asyncio.create_task(_generate_section_text(query))

                # 3-level 
                else:
                    for subsection in section["subsections"]:
                        query = _generate_query(f"{subsection['title']}", section_table_map)
                        tasks[subsection["title"]] = asyncio.create_task(_generate_section_text(query))

    # async execute tasks
    keys = list(tasks.keys())
    values = await asyncio.gather(*list(tasks.values()))
    res_map = {}
    for k, v in zip(keys, values):
        res_map[k] = v

    return res_map


async def generate_tables(title: str=None, tables_desc: dict=None):
    
    def _generate_query(table: dict) -> str:
        return f"请分析论文题目《{title}》，根据需求生成对应的表数据。当前需要生成的表ID为：【{table['id']}】, 该表描述为：{table['desc']}"
    
    async def _generate_table(query: str | List ):
        if isinstance(query, str):
            query = [query]

        res = []
        for q in query:
            messages = [
                {'role': 'assistant', 'content': PAPER_TABLE_PROMPT},
                {'role': 'user', 'content': q}
            ] 
            try:
                ret_str = await call_chat_completion_async(messages)
                ret_json = json.loads(ret_str)
                res.append(ret_json)
            except Exception: 
                print("JSON解析失败")
        return res
    
    
    # generate tables (JSON-format) based on corresponding description  
    # parsing to tasks
    tasks = {}
    for k, v in tables_desc.items():
        query = [_generate_query(table) for table in v]
        tasks[k] = asyncio.create_task(_generate_table(query))

    # execute
    res_map = {}
    keys = list(tasks.keys())
    values = await asyncio.gather(*list(tasks.values()))
    for k, v in zip(keys, values):
        res_map[k] = v
    
    return res_map


