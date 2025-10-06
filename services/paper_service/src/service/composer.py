from docx import Document
from docx.shared import Pt
from docx.text.paragraph import Paragraph
import os

def compose_doc_toc(structure: dict, file_path: str=None):
    # generate table of contents in a docx
    if os.path.exists(file_path):
        doc = Document(file_path)
    else:
        doc = Document()
    
    for chapter in structure["chapters"]:
        # 1-level
        para = doc.add_paragraph(chapter["title"])
        _set_toc_style(doc, para, 1)
        # 2-level
        if "sections" in chapter:
            for section in chapter["sections"]:
                para = doc.add_paragraph(section["title"])
                _set_toc_style(doc, para, 2)
                # 3-level 
                if "subsections" in section:
                    for subsection in section["subsections"]:
                        para = doc.add_paragraph(subsection["title"]) 
                        _set_toc_style(doc, para, 3)

    doc.save(file_path)                


def _set_toc_style(doc: Document, paragraph: Paragraph, level: int):
    if level == 1:
        # 一级标题：宋体、小三号、加粗、段前18磅、段后12磅
        paragraph.style = doc.styles["Heading 1"]
        paragraph.style.font.name = "宋体"
        paragraph.style.font.size = Pt(15)  # 15磅
        paragraph.style.font.bold = True
        paragraph.paragraph_format.space_before = Pt(18)
        paragraph.paragraph_format.space_after = Pt(12)
    elif level == 2:
        # 二级标题：宋体、四号、加粗、段前12磅、段后6磅
        paragraph.style = doc.styles["Heading 2"]
        paragraph.style.font.name = "宋体"
        paragraph.style.font.size = Pt(14)  # 14磅
        paragraph.style.font.bold = True
        paragraph.paragraph_format.space_before = Pt(12)
        paragraph.paragraph_format.space_after = Pt(6)
    elif level == 3:
        # 三级标题：宋体、小四号、加粗、段前6磅、段后3磅
        paragraph.style = doc.styles["Heading 3"]
        paragraph.style.font.name = "宋体"
        paragraph.style.font.size = Pt(12)  # 12磅
        paragraph.style.font.bold = True
        paragraph.paragraph_format.space_before = Pt(6)
        paragraph.paragraph_format.space_after = Pt(3)
    
    