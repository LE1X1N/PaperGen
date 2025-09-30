from docx import Document
import os

def compose_doc_toc(structure: dict, file_path: str=None):
    # generate table of contents in a docx
    if os.path.exists(file_path):
        doc = Document(file_path)
    else:
        doc = Document()
    
    for chapter in structure["chapters"]:
        # 1-level
        doc.add_paragraph(chapter["title"])
        
        # 2-level
        if "sections" in chapter:
            for section in chapter["sections"]:
                doc.add_paragraph(section["title"])
                
                # 3-level 
                if "subsections" in section:
                    for subsection in section["subsections"]:
                        doc.add_paragraph(subsection["title"])    
                        
    doc.save(file_path)                
    
    