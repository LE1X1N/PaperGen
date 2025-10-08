from src.service.content import generate_figure_json, generate_paper_structure, generate_main_body_text, generate_abstract_json
from src.service.doc import compose_toc, compose_main_body, init_doc, compose_cover, compose_abstract
from src.utils.common import load_json

if __name__== "__main__":
    title = "基于Android+XAMPP+MySQL的家校互动平台设计与实现"
    doc_path = f"test/{title}.docx"

    # structure = generate_paper_structure(title=title, save=True, save_path="test/structure_test.json")
    # abstract = generate_abstract_json(title=title, save=True, save_path="test/abstract_test.json")

    abstract = load_json("test/abstract_test.json")
    structure = load_json("test/structure_test_cut.json")  
    main_body = generate_main_body_text(title, structure)
    
    doc = init_doc(doc_path)

    compose_cover(doc, title)
    compose_abstract(doc, abstract)
    compose_toc(doc, structure)
    compose_main_body(doc, structure, main_body)
    
    doc.save(doc_path)

    print("Success")
    
    