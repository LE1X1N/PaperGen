from pathlib import Path
import os
import json
import docx
import time
from docx2pdf import convert

from src.service.content import JSONGenerator
from src.service.content import generate_main_body_text, generate_tables
from src.service.doc import DocComposer, StyleController
from src.utils.common import load_json, parse_section_titles

class Pipeline:

    def __init__(self):
        self.json_generator = JSONGenerator()
        self.style_controller = StyleController()
        self.doc_composer = DocComposer()

        self.cache_dir = Path("cache/")

        self.STRUCTURE_JSON_FILE = "structure.json"
        self.ABSTRACT_JSON_FILE =  "abstract.json"
        self.TABLES_DESC_JSON_FILE = "tables_desc.json"
        self.TABLES_JSON_FILE = "tables.json"
        self.MAIN_BODY_JSON_FILE = "main_body.json"

    def _init_doc(self, file_path: str=None):
        # initialize a doc object 
        if os.path.exists(file_path):
            doc = docx.Document(file_path)
            print(f"打开文档: {file_path}")
        else:
            doc = docx.Document()
        
        # init styles
        self.style_controller.init_doc_style(doc)
        return doc
    

    def _get_or_generate(self, path, generate_func, save, *args, **kwargs):
        if path.exists():
            content = load_json(path)
            print(f"命中缓存文件：{path}")
            return content
        else:
            start_time = time.time()
            content = generate_func(*args, **kwargs)
            if save:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2, ensure_ascii=False)
            print(f"生成成功！存储路径：{path}, 耗时 {time.time() - start_time} s")
            return content


    def generate_paper(self, title: str):
        # create folder
        doc_folder = self.cache_dir / title
        if not doc_folder.exists():
            os.mkdir(doc_folder)

        # structure
        structure_path = doc_folder / self.STRUCTURE_JSON_FILE
        structure = self._get_or_generate(structure_path, self.json_generator.generate_paper_structure, True,
                                          query=f"请分析论文题目《{title}》，按要求生成对应JSON。")

        # abstract
        abstract_path = doc_folder / self.ABSTRACT_JSON_FILE
        abstract = self._get_or_generate(abstract_path, self.json_generator.generate_abstract_json, True,
                                          query=f"请分析论文题目《{title}》，按要求生成对应JSON。")

        # tables description
        tables_desc_path = doc_folder / self.TABLES_DESC_JSON_FILE
        tables_desc = self._get_or_generate(tables_desc_path, self.json_generator.generate_table_desc_json, True,
                                          query=f"请分析论文题目 《{title}》，按照提供的论文章节目录设计所需的表格映射表。本论文所有【论文章节】包括: 【{parse_section_titles(structure)}】")

        # main body
        main_body_path = doc_folder / self.MAIN_BODY_JSON_FILE
        main_body = self._get_or_generate(main_body_path, generate_main_body_text, True,
                                          title, structure, tables_desc)

        # tables
        tables_path = doc_folder / self.TABLES_JSON_FILE
        tables = self._get_or_generate(tables_path, generate_tables, True,
                                          title, tables_desc)


        # create a docx file
        doc_path = doc_folder / f"{title}.docx"
        doc = self._init_doc(doc_path)

        # compose content
        self.doc_composer.compose_all(doc, title, abstract, structure, main_body, tables)
        doc.save(doc_path)

        # convert to pdf
        convert(doc_path, doc_folder / f"{title}.pdf")

        print(f"论文生成成功，文章保存路径：{doc_path}")