from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn


class StyleController:
    def __init__(self):
        self.TOC_HEAD_STYLE = "论文_目录"
        self.TOC_STYLE_1 = "论文_目录 1"
        self.TOC_STYLE_2 = "论文_目录 2"
        self.TOC_STYLE_3 = "论文_目录 3"
        self.NORMAL_STYLE = "论文_正文"
        self.HEADING_STYLE_1 = "论文_标题 1"
        self.HEADING_STYLE_2 = "论文_标题 2"
        self.HEADING_STYLE_3 = "论文_标题 3"

    def init_doc_style(self, doc: Document):
        self._modify_toc_head_styles(doc)
        self._modify_toc_l1_styles(doc)
        self._modify_toc_l2_styles(doc)
        self._modify_toc_l3_styles(doc)
        self._modify_normal_style(doc)
        self._modify_heading_l1_styles(doc)
        self._modify_heading_l2_styles(doc)
        self._modify_heading_l3_styles(doc)

    def _modify_toc_head_styles(self, doc: Document):
        if self.TOC_HEAD_STYLE in doc.styles:
            style = doc.styles[self.TOC_HEAD_STYLE]
        else:
            style = doc.styles.add_style(self.TOC_HEAD_STYLE, WD_STYLE_TYPE.PARAGRAPH)

        style.font.name = "Times New Roman"
        style.font.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
        style.font.size = Pt(16)
        style.font.bold = True
        style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    def _modify_toc_l1_styles(self, doc: Document):
        if self.TOC_STYLE_1 in doc.styles:
            style = doc.styles[self.TOC_STYLE_1]
        else:
            style = doc.styles.add_style(self.TOC_STYLE_1, WD_STYLE_TYPE.PARAGRAPH)

        style.font.size = Pt(12)  # 12磅（小四）
        style.font.bold = True
        style.font.name = "Times New Roman"
        style.font._element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
        style.paragraph_format.line_spacing = 1.25
        style.paragraph_format.space_before = Pt(0)
        style.paragraph_format.space_after = Pt(0)

    def _modify_toc_l2_styles(self, doc: Document):
        if self.TOC_STYLE_2 in doc.styles:
            style = doc.styles[self.TOC_STYLE_2]
        else:
            style = doc.styles.add_style(self.TOC_STYLE_2, WD_STYLE_TYPE.PARAGRAPH)

        style.font.size = Pt(12)  # 12磅（小四）
        style.font.bold = False
        style.font.name = "Times New Roman"
        style.font._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        style.paragraph_format.line_spacing = 1.25
        style.paragraph_format.space_before = Pt(0)
        style.paragraph_format.space_after = Pt(0)
        style.paragraph_format.left_indent = Pt(20)

    def _modify_toc_l3_styles(self, doc: Document):
        if self.TOC_STYLE_3 in doc.styles:
            style = doc.styles[self.TOC_STYLE_3]
        else:
            style = doc.styles.add_style(self.TOC_STYLE_3, WD_STYLE_TYPE.PARAGRAPH)

        style.font.size = Pt(12)  # 12磅（小四）
        style.font.bold = False
        style.font.name = "Times New Roman"
        style.font._element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
        style.paragraph_format.line_spacing = 1.25
        style.paragraph_format.space_before = Pt(0)
        style.paragraph_format.space_after = Pt(0)
        style.paragraph_format.left_indent = Pt(40)

    def _modify_normal_style(self, doc: Document):
        if self.NORMAL_STYLE in doc.styles:
            style = doc.styles[self.NORMAL_STYLE]
        else:
            style = doc.styles.add_style(self.NORMAL_STYLE, WD_STYLE_TYPE.PARAGRAPH)
            
        # font style
        font_size = Pt(12)
        style.font.size = font_size
        style.font.bold = False
        style.font.name = "Times New Roman"
        style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')

        # jusify alignment, first line indent 2 characters
        style.paragraph_format.first_line_indent = font_size * 2 
        style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

    def _modify_heading_l1_styles(self, doc: Document):
        if self.HEADING_STYLE_1 in doc.styles:
            style = doc.styles[self.HEADING_STYLE_1]
        else:
            style = doc.styles.add_style(self.HEADING_STYLE_1, WD_STYLE_TYPE.PARAGRAPH)

        # font
        style.font.size = Pt(16)
        style.font.bold = True
        style.font.name = "Times New Roman"
        style.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

        # paragraph
        style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        style.paragraph_format.space_before = Pt(13)

    def _modify_heading_l2_styles(self, doc: Document):
        if self.HEADING_STYLE_2 in doc.styles:
            style = doc.styles[self.HEADING_STYLE_2]
        else:
            style = doc.styles.add_style(self.HEADING_STYLE_2, WD_STYLE_TYPE.PARAGRAPH)

        # font
        style.font.size = Pt(14)
        style.font.bold = True
        style.font.name = "Times New Roman"
        style.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

        # paragraph
        style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        style.paragraph_format.space_before = Pt(13)

    def _modify_heading_l3_styles(self, doc: Document):
        if self.HEADING_STYLE_3 in doc.styles:
            style = doc.styles[self.HEADING_STYLE_3]
        else:
            style = doc.styles.add_style(self.HEADING_STYLE_3, WD_STYLE_TYPE.PARAGRAPH)

        # font
        style.font.size = Pt(12)
        style.font.bold = True
        style.font.name = "Times New Roman"
        style.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

        # paragraph
        style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        style.paragraph_format.space_before = Pt(13)
