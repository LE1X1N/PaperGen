import os
import docx
from pathlib import Path

from src.service.content import JSONGenerator
from src.service.content import generate_main_body_text, generate_tables
from src.service.doc import DocComposer
from src.utils.common import load_json, parse_section_titles

def init_doc(file_path: str=None):
    # initialize a doc object and styles
    if os.path.exists(file_path):
        doc = docx.Document(file_path)
        print(f"打开文档: {file_path}")
    else:
        doc = docx.Document()
        print(f"创建新文档: {file_path}")
    return doc


if __name__== "__main__":
    title = "基于物联网的智能家居系统设计"

    doc_folder = Path(f"data/{title}")

    # create folder
    if not doc_folder.exists():
        os.mkdir(doc_folder)


    json_generator = JSONGenerator()

    structure = json_generator.generate_paper_structure(query=f"请分析论文题目《{title}》，按要求生成对应JSON。", 
                                         save=True, save_path= doc_folder / "structure.json")

    # structure = load_json(doc_folder / "structure.json")
    print("结构生成成功！")


    abstract = json_generator.generate_abstract_json(query=f"请分析论文题目《{title}》，按要求生成对应JSON。", 
                                      save=True, save_path= doc_folder / "abstract.json")

    # abstract = load_json(doc_folder / "abstract.json")
    print("引言生成成功！")


    tables_desc = json_generator.generate_table_desc_json(query=f"请分析论文题目 《{title}》，按照提供的论文章节目录设计所需的表格映射表。本论文所有【论文章节】包括: 【{parse_section_titles(structure)}】",
                                     save=True, save_path=doc_folder / "tables_desc.json")
    # tables_desc = load_json(doc_folder / "tables_desc.json")
    print("表格描述生成成功！")

    main_body = generate_main_body_text(title, structure, tables_desc, save=True, save_path = doc_folder / "main_body.json")
    # main_body = load_json(doc_folder / "main_body.json")
    print("文章内容生成成功！")
    

    tables = generate_tables(title, tables_desc, save = True, save_path = doc_folder / "tables.json")
    # tables = load_json(doc_folder / "tables.json")
    print("表格生成成功！")

    doc_path = doc_folder / f"{title}.docx"
    doc = init_doc(doc_path)

    doc_composer = DocComposer(doc)
    doc_composer.compose_all(title, abstract, structure, main_body, tables)
    
    doc.save(doc_path)

    print(f"论文生成成功，文章保存路径：{doc_path}")
    
    