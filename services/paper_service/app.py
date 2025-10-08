import os
import docx

from src.service.content import JSONGenerator
from src.service.doc import DocComposer
from src.utils.common import load_json

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
    title = "基于Android+XAMPP+MySQL的家校互动平台设计与实现"
    doc_path = f"test/{title}.docx"

    json_generator = JSONGenerator()

    # structure = json_generator.generate_paper_structure(query=f"请分析论文题目《{title}》，按要求生成对应JSON。", 
    #                                      save=True, save_path="test/structure_test.json")

    # abstract = json_generator.generate_abstract_json(query=f"请分析论文题目《{title}》，按要求生成对应JSON。", 
    #                                   save=True, save_path="test/abstract_test.json")

    # tables_map = json_generator.generate_table_desc_json(query=f"请分析论文题目 《{title}》，按照提供的论文章节目录设计所需的表格映射表。论文目录JSON为: {structure}",
    #                                  save=True, save_path="test/tables_map_test.json")

    abstract = load_json("test/abstract_test.json")
    structure = load_json("test/structure_test.json")  



    # main_body = generate_main_body_text(title, structure)
    
    doc = init_doc(doc_path)

    doc_composer = DocComposer(doc)
    doc_composer.compose_all(title, abstract, structure)

    
    doc.save(doc_path)

    print("Success")
    
    