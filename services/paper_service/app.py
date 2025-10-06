from src.service.gen_funcs import generate_figure_json, generate_paper_structure
from src.service.composer import compose_doc_toc
from src.utils.common import load_structure_from_json

if __name__== "__main__":
    title = "基于Android+XAMPP+MySQL的家校互动平台设计与实现"
    
    # structure = generate_paper_structure( 
    #     title=title,
    #     save=True,
    #     save_path="test/structure_test.json")

    structure = load_structure_from_json("test/structure_test.json")
    
    compose_doc_toc(structure, "test/demo.docx")
    print("Success")
    
    # generate_figure_json(
    #     title=title,
    #     save=True,
    #     save_path="test/figure_json_test.json"
    # )
    