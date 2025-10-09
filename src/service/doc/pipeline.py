from pathlib import Path
import os
import docx

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
            print(f"创建新文档: {file_path}")
        
        # init styles
        self.style_controller.init_doc_style(doc)
        return doc

    def generate_paper(self, title: str):
        
        doc_folder = self.cache_dir / title

        # create folder
        if not doc_folder.exists():
            os.mkdir(doc_folder)

        # structure
        structure_path = doc_folder / self.STRUCTURE_JSON_FILE
        if structure_path.exists():
            structure = load_json(structure_path)
            print(f"结构使用缓存文件：{structure_path}")
        else:
            structure = self.json_generator.generate_paper_structure(query=f"请分析论文题目《{title}》，按要求生成对应JSON。", 
                                                save=True, save_path=structure_path)
            print(f"结构生成成功！存储路径：{structure_path}")

        # abstract
        abstract_path = doc_folder / self.ABSTRACT_JSON_FILE
        if abstract_path.exists():
            abstract = load_json(abstract_path)
            print(f"引言使用缓存文件：{abstract_path}")
        else:
            abstract = self.json_generator.generate_abstract_json(query=f"请分析论文题目《{title}》，按要求生成对应JSON。", 
                                            save=True, save_path=abstract_path)
            print(f"引言生成成功！存储路径：{abstract_path}")

        # tables description
        tables_desc_path = doc_folder / self.TABLES_DESC_JSON_FILE
        if tables_desc_path.exists():
            tables_desc = load_json(tables_desc_path)
            print(f"表格描述使用缓存文件：{tables_desc_path}")
        else:
            tables_desc = self.json_generator.generate_table_desc_json(query=f"请分析论文题目 《{title}》，按照提供的论文章节目录设计所需的表格映射表。本论文所有【论文章节】包括: 【{parse_section_titles(structure)}】",
                                            save=True, save_path=tables_desc_path)
            print(f"表格描述生成成功！存储路径：{tables_desc_path}")

        # main body
        main_body_path = doc_folder / self.MAIN_BODY_JSON_FILE
        if main_body_path.exists():
            main_body = load_json(main_body_path)
            print(f"文章内容使用缓存文件：{main_body_path}")
        else:
            main_body = generate_main_body_text(title, structure, tables_desc, save=True, save_path=main_body_path)
            print(f"文章内容生成成功！存储路径：{main_body_path}")

        # tables
        tables_path = doc_folder / self.TABLES_JSON_FILE
        if tables_path.exists():
            tables = load_json(tables_path)
            print(f"表格使用缓存文件：{tables_path}")
        else:
            tables = generate_tables(title, tables_desc, save = True, save_path=tables_path)
            print(f"表格生成成功！{tables_path}")


        # create a docx file
        doc_path = doc_folder / f"{title}.docx"
        doc = self._init_doc(doc_path)

        # compose content
        self.doc_composer.compose_all(doc, title, abstract, structure, main_body, tables)
        
        doc.save(doc_path)
        print(f"论文生成成功，文章保存路径：{doc_path}")