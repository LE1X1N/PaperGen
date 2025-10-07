from src.service.content import generate_figure_json, generate_paper_structure, generate_main_body_text
from src.service.doc import compose_toc, compose_main_body, init_doc
from src.utils.common import load_structure_from_json

if __name__== "__main__":
    title = "基于Android+XAMPP+MySQL的家校互动平台设计与实现"
    
    # structure = generate_paper_structure( 
    #     title=title,
    #     save=True,
    #     save_path="test/structure_test.json")

    structure = load_structure_from_json("test/structure_test.json")
    main_body = generate_main_body_text(title, structure)
    
    doc = init_doc("test/demo.docx")

    compose_toc(doc, structure)
    compose_main_body(doc, structure, main_body)
    
    doc.save("test/demo.docx")

    print("Success")
    

    # generate_figure_json(
    #     title=title,
    #     save=True,
    #     save_path="test/figure_json_test.json"
    # )
    