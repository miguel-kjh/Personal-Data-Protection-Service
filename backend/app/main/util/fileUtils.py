from app.main.util.envNames import ALLOWED_EXTENSIONS
from app.main.util.heuristicMeasures import MINIMAL_WHITE_SPACE_DENSITY
from app.main.util.semanticWordLists import lettersOfDni

from datetime import datetime

from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table, _Row
from docx.text.paragraph import Paragraph

import io
import pdfplumber
import pandas as pd

from typing import Text
import re
import string


def allowedFile(filename: str) -> bool:
    return giveTypeOfFile(filename) in ALLOWED_EXTENSIONS


def giveTypeOfFile(filename: str) -> str:
    return '.' in filename and filename.rsplit('.', 1)[1].lower()


def giveFileNameUnique(filename: str, fileType: str) -> str:
    # filename = filename + str(datetime.now().timestamp())
    # sha = hashlib.sha256(filename.encode())
    # return sha.hexdigest() + "." + fileType
    return str(datetime.now().timestamp()).replace(".", "") + "." + fileType


def encode(text: str):
    return "*" * len(text)


def markInHtml(text: str):
    return '<mark style="background: #7aecec;">' + text + '</mark>'


def itemIterator(parent):
    """
    Generate a reference to each paragraph and table child within *parent*,
    in document order. Each returned value is an instance of either Table or
    Paragraph. *parent* would most commonly be a reference to a main
    Document object, but also works for a _Cell object, which itself can
    contain paragraphs and tables.
    """
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    elif isinstance(parent, _Row):
        parent_elm = parent._tr
    else:
        raise ValueError("something's not right")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def readPdf(path:str) -> Text:
    #with open(path, 'rb') as fh:
    #    for page in PDFPage.get_pages(fh, 
    #                                  caching=True,
    #                                  check_extractable=True):
    #        resource_manager = PDFResourceManager()
    #        fake_file_handle = io.StringIO()
    #        converter = TextConverter(resource_manager, fake_file_handle)
    #        page_interpreter = PDFPageInterpreter(resource_manager, converter)
    #        page_interpreter.process_page(page)
    #        
    #        text = fake_file_handle.getvalue()
    #        if text.count(' ')/len(text) > MINIMAL_WHITE_SPACE_DENSITY: 
    #            yield text
    #
    #        # close open handles
    #        converter.close()
    #        fake_file_handle.close()
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text   = page.extract_text()
            tables = []
            for pdf_table in page.extract_tables():
                table = []
                cells = []
                for row in pdf_table:
                    if not any(row):
                        if any(cells):
                            table.append(cells)
                            cells = []
                    elif all(row):
                        if any(cells):
                            table.append(cells)
                            cells = []
                        table.append(row)
                    else:
                        if len(cells) == 0:
                            cells = row
                        else:
                            for i in range(len(row)):
                                if row[i] is not None:
                                    cells[i] = row[i] if cells[i] is None else cells[i] + row[i]
                for regex in map(lambda row: ".*" + ".*".join(row) + ".*", table):
                    text = re.sub(regex,'',text)
                tables.append(table)
            yield (text, tables)

def isDni(dni:str) -> bool:
    number = re.search(r'\d{2}.?\d{2}.?\d{2}.?\d{2}', dni)
    if not number:
        return False
    number = ''.join(filter(str.isdigit, dni))
    if lettersOfDni[int(number) % 23] != dni[-1].upper():
        return False
    
    return True