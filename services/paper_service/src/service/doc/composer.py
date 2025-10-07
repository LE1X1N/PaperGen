from docx import Document
import os
from src.service.doc.styles import _modify_heading_styles, _modify_normal_style, _modify_toc_styles
from src.service.doc.styles import TOC_HEAD_STYLE, TOC_STYLE_1, TOC_STYLE_2, TOC_STYLE_3
from src.service.doc.styles import HEADING_STYLE_2, HEADING_STYLE_3, HEADING_STYLE_4
from src.service.doc.styles import NORMAL_STYLE

def init_doc(file_path: str=None):
    # initialize a doc object and styles
    if os.path.exists(file_path):
        doc = Document(file_path)
        print(f"打开文档: {file_path}")
    else:
        doc = Document()
        print(f"创建新文档: {file_path}")

    _modify_toc_styles(doc)
    _modify_normal_style(doc)
    _modify_heading_styles(doc)

    return doc

def compose_toc(doc: Document, structure: dict):
    # generate table of contents in a docx
    doc.add_paragraph("目录", style=TOC_HEAD_STYLE)

    for chapter in structure["chapters"]:
        # 1-level
        doc.add_paragraph(chapter["title"], style=TOC_STYLE_1)

        # 2-level
        if "sections" in chapter:
            for section in chapter["sections"]:
                doc.add_paragraph(section["title"], style=TOC_STYLE_2)

                # 3-level 
                if "subsections" in section:
                    for subsection in section["subsections"]:
                        doc.add_paragraph(subsection["title"], style=TOC_STYLE_3) 
    doc.add_page_break() 


def compose_main_body(doc: Document, structure: dict, main_body: dict):
    
    for chapter in structure["chapters"]:
        # 1-level Handling
        doc.add_paragraph(chapter["title"], style=HEADING_STYLE_2)

        if "sections" not in chapter:
            # Main Body     
            texts = main_body[chapter['title']]
            for text in texts:
                doc.add_paragraph(text, style=NORMAL_STYLE) 

        # 2-level
        else:
            for section in chapter["sections"]:
                # 2-level Handling
                doc.add_paragraph(section['title'], style=HEADING_STYLE_3)

                if "subsections" not in section:
                    # Main Body
                    texts = main_body[section['title']]
                    for text in texts:
                        doc.add_paragraph(text, style=NORMAL_STYLE)

                # 3-level 
                else:
                    for subsection in section["subsections"]:
                        # 3-level Handling
                        doc.add_paragraph(subsection['title'], style=HEADING_STYLE_4)
                        # Main Body
                        texts = main_body[subsection['title']]
                        for text in texts:
                            doc.add_paragraph(text, style=NORMAL_STYLE)

        doc.add_page_break() 
