from docx import Document
from docx.shared import Pt
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import os

def compose_doc_toc(structure: dict, file_path: str=None):
    # generate table of contents in a docx
    if os.path.exists(file_path):
        doc = Document(file_path)
    else:
        doc = Document()
    
    title = doc.add_paragraph("目录")
    title.style.font.name = "黑体"
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    
    for chapter in structure["chapters"]:
        # 1-level
        para1 = doc.add_paragraph(chapter["title"])
        _set_toc_style(para1, 1)
        # 2-level
        if "sections" in chapter:
            for section in chapter["sections"]:
                para2 = doc.add_paragraph(section["title"])
                _set_toc_style(para2, 2)
                # 3-level 
                if "subsections" in section:
                    for subsection in section["subsections"]:
                        para3 = doc.add_paragraph(subsection["title"]) 
                        _set_toc_style(para3, 3)

    doc.save(file_path)                


def _set_toc_style(paragraph: Paragraph, level: int):
    """
        目录（TOC）：段前段后0，行间距1.25
    """
    paragraph.style.font.size = Pt(12)  # 12磅（小四）
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)

    if level == 1:
        paragraph.style.font.name = "Times New Roman"
        paragraph.style.font.bold = True
    elif level == 2:
        # 目录二级标题：宋体、四号、加粗
        paragraph.style.font.name = "Times New Roman"
        paragraph.style.font.bold = True
    elif level == 3:
        # 目录三级标题：宋体、小四号、加粗
        paragraph.style.font.name = "Times New Roman"
        paragraph.style.font.bold = True 
    