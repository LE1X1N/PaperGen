from src.service.gen_funcs import generate_image_json, generate_paper_structure


if __name__== "__main__":
    title = "基于Android+XAMPP+MySQL的家校互动平台设计与实现"
    
    generate_image_json(
        title,
        save=True,
        save_path="services/paper_service/test/image_json_test.json"
    )
    
    generate_paper_structure( 
        title,
        save=True,
        save_path="services/paper_service/test/structure_test.json")