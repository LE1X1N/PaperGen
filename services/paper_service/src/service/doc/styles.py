from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx import Document

TOC_HEAD_STYLE = "目录"
TOC_STYLE_1 = "目录 1"
TOC_STYLE_2 = "目录 2"
TOC_STYLE_3 = "目录 3"
NORMAL_STYLE = "正文"
HEADING_STYLE_2 = "标题 2"
HEADING_STYLE_3 = "标题 3"
HEADING_STYLE_4 = "标题 4"


def _modify_toc_styles(doc: Document):
    if TOC_HEAD_STYLE in doc.styles:
        style = doc.styles[TOC_HEAD_STYLE]
    else:
        style = doc.styles.add_style(TOC_HEAD_STYLE, WD_STYLE_TYPE.PARAGRAPH)

    style.font.name = "Times New Roman"
    style.font.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    style.font.size = Pt(16)
    style.font.bold = True
    style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    if TOC_STYLE_1 in doc.styles:
        style = doc.styles[TOC_STYLE_1]
    else:
        style = doc.styles.add_style(TOC_STYLE_1, WD_STYLE_TYPE.PARAGRAPH)

    style.font.size = Pt(12)  # 12磅（小四）
    style.font.bold = True
    style.font.name = "Times New Roman"
    style.font._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    style.paragraph_format.line_spacing = 1.25
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)

    if TOC_STYLE_2 in doc.styles:
        style = doc.styles[TOC_STYLE_2]
    else:
        style = doc.styles.add_style(TOC_STYLE_2, WD_STYLE_TYPE.PARAGRAPH)

    style.font.size = Pt(12)  # 12磅（小四）
    style.font.bold = False
    style.font.name = "Times New Roman"
    style.font._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    style.paragraph_format.line_spacing = 1.25
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.left_indent = Pt(20)

    if TOC_STYLE_3 in doc.styles:
        style = doc.styles[TOC_STYLE_3]
    else:
        style = doc.styles.add_style(TOC_STYLE_3, WD_STYLE_TYPE.PARAGRAPH)

    style.font.size = Pt(12)  # 12磅（小四）
    style.font.bold = False
    style.font.name = "Times New Roman"
    style.font._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    style.paragraph_format.line_spacing = 1.25
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.left_indent = Pt(40)


def _modify_normal_style(doc: Document):

    if NORMAL_STYLE in doc.styles:
        style = doc.styles[NORMAL_STYLE]
    else:
        style = doc.styles.add_style(NORMAL_STYLE, WD_STYLE_TYPE.PARAGRAPH)
        
    # font style
    font_size = Pt(12)
    style.font.size = font_size
    style.font.bold = False
    style.font.name = "Times New Roman"
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

    # jusify alignment, first line indent 2 characters
    style.paragraph_format.first_line_indent = font_size * 2 
    style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

def _modify_heading_styles(doc: Document):

    if HEADING_STYLE_2 in doc.styles:
        style = doc.styles[HEADING_STYLE_2]
    else:
        style = doc.styles.add_style(HEADING_STYLE_2, WD_STYLE_TYPE.PARAGRAPH)

    # font
    style.font.size = Pt(16)
    style.font.bold = True
    style.font.name = "Times New Roman"
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    # para
    style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    style.paragraph_format.space_before = Pt(13)

    if HEADING_STYLE_3 in doc.styles:
        style = doc.styles[HEADING_STYLE_3]
    else:
        style = doc.styles.add_style(HEADING_STYLE_3, WD_STYLE_TYPE.PARAGRAPH)

    # font
    style.font.size = Pt(14)
    style.font.bold = True
    style.font.name = "Times New Roman"
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    # para
    style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    style.paragraph_format.space_before = Pt(13)


    if HEADING_STYLE_4 in doc.styles:
        style = doc.styles[HEADING_STYLE_4]
    else:
        style = doc.styles.add_style(HEADING_STYLE_4, WD_STYLE_TYPE.PARAGRAPH)

    # font
    style.font.size = Pt(12)
    style.font.bold = True
    style.font.name = "Times New Roman"
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    # para
    style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    style.paragraph_format.space_before = Pt(13)