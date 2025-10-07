from docx import Document
from docx.shared import Pt
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
import os
from tqdm import tqdm
from src.service.gen_funcs import generate_section_text

def compose_main_body(title: str, structure: dict, file_path: str=None):
    
    doc = Document(file_path)

    # generate main body of docx
    # tasks = []
    # for chapter in structure["chapters"]:
    #     # 1-level
    #     if "sections" not in chapter:
    #         tasks.append(chapter["title"])

    #     # 2-level
    #     else:
    #         for section in chapter["sections"]:
    #             if "subsections" not in section:
    #                 tasks.append(f"{chapter['title']} -> {section['title']}")

    #             # 3-level 
    #             else:
    #                 for subsection in section["subsections"]:
    #                     tasks.append(f"{chapter['title']} -> {section['title']} -> {subsection['title']}")
    

    for chapter in structure["chapters"]:
        # 1-level Handling
        doc.add_heading(chapter["title"], level=1)

        if "sections" not in chapter:
            # Main Body     
            texts = generate_section_text(title=title, section=chapter["title"], structure=structure)
            for text in texts:
                para = doc.add_paragraph(text) 
                _set_main_body_style(doc, para)

        # 2-level
        else:
            for section in chapter["sections"]:
                # 2-level Handling
                doc.add_heading(section['title'], level=2)

                if "subsections" not in section:
                    # Main Body
                    texts = generate_section_text(title=title, section=f"{chapter['title']} -> {section['title']}", structure=structure)
                    for text in texts:
                        para = doc.add_paragraph(text)
                        _set_main_body_style(doc, para)

                # 3-level 
                else:
                    for subsection in section["subsections"]:
                        # Handling
                        doc.add_heading(subsection['title'], level=3)
                        # Main Body
                        texts = generate_section_text(title=title, section=f"{chapter['title']} -> {section['title']} -> {subsection['title']}", structure=structure)
                        for text in texts:
                            para = doc.add_paragraph(text)
                            _set_main_body_style(doc, para)

        doc.add_page_break()   

    doc.save(file_path)


def _set_main_body_style(doc: Document, paragraph: Paragraph):
    style_name = "MainBodyStyle"

    if style_name not in doc.styles:
        style = doc.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)

        # font style
        font_size = Pt(12)
        style.font.size = font_size
        style.font.bold = False
        style.font.name = "Times New Roman"
        style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

        # jusify alignment, first line indent 2 characters
        style.paragraph_format.first_line_indent = font_size * 2 
        style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
        

    paragraph.style = doc.styles[style_name]
    

def compose_toc(structure: dict, file_path: str=None):
    # generate table of contents in a docx
    if os.path.exists(file_path):
        doc = Document(file_path)
    else:
        doc = Document()
    
    title = doc.add_paragraph("目录")
    title.runs[0].font.name = "Times New Roman"
    title.runs[0].element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    title.runs[0].font.size = Pt(14)
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
    doc.add_page_break()
    doc.save(file_path)                


def _set_toc_style(paragraph: Paragraph, level: int):
    """
        目录（TOC）：段前段后0，行间距1.25
    """
    run = paragraph.runs[0]

    run.font.size = Pt(12)  # 12磅（小四）
    run.font.name = "Times New Roman"
    paragraph.paragraph_format.line_spacing = 1.25
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)

    if level == 1:
        run.font.bold = True
        run.font._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    elif level == 2:
        run.font.bold = False
        run.font._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        paragraph.paragraph_format.left_indent = Pt(20)
    elif level == 3:
        run.font.bold = False
        run.font._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        paragraph.paragraph_format.left_indent = Pt(40)
    