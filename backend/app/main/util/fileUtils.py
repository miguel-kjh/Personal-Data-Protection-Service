from app.main.util.envNames import ALLOWED_EXTENSIONS
from app.main.util.heuristicMeasures import LINE_BREAK_DENSITY
from app.main.util.semanticWordLists import lettersOfDni

from datetime import datetime

from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table, _Row
from docx.text.paragraph import Paragraph

from pdfminer.high_level import extract_text
from nltk.tokenize import sent_tokenize

from typing import Text
import re


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
    text = extract_text(path)
    for token in sent_tokenize(text):
        countLineBreak = token.count('\n')
        if countLineBreak/len(token) <= LINE_BREAK_DENSITY:
            yield token

def isDni(dni:str) -> bool:
    number = re.search(r'\d{8}', dni)
    if not number:
        return False
    
    if lettersOfDni[int(number[0]) % 23] != dni[-1].upper():
        return False
    
    return True