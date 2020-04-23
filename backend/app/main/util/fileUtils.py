from app.main.util.envNames          import ALLOWED_EXTENSIONS
from app.main.util.semanticWordLists import lettersOfDni

from datetime import datetime

from docx.document            import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table          import CT_Tbl
from docx.table               import _Cell, Table, _Row
from docx.text.paragraph      import Paragraph

import io
import pdfplumber
import pandas as pd

from typing import Text
import re
import string

from unidecode import unidecode



def allowedFile(filename: str) -> bool:
    return giveTypeOfFile(str(filename)) in ALLOWED_EXTENSIONS

def giveTypeOfFile(filename: str):
    return isinstance(filename,str) and '.' in filename and filename.rsplit('.', 1)[1].lower()


def giveFileNameUnique(fileType: str) -> str:
    return str(datetime.now().timestamp()).replace(".", "") + "." + fileType

def itemIterator(parent):
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
    try:
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
    except Exception:
        return

def isDni(dni:str) -> bool:
    number = ''.join(filter(str.isdigit, dni))
    if not number or lettersOfDni[int(number) % 23] != dni[-1].upper():
        return False
    
    return True

def normalizeUnicode(string: str) -> str:
    letersÑ = list(filter(lambda x: string[x].lower() == 'ñ', range(0,len(string))))
    if not letersÑ:
        return unidecode(string)
    result = unidecode(string)
    return ''.join(['ñ' if index in letersÑ else char for index,char in enumerate(result)])
    

MAX_NAME_OF_QUERY = 4000
def generateWordsAsString(words:list) -> str:
        if len(words) < MAX_NAME_OF_QUERY:
            yield "('" + '\',\''.join(words) + "')"
            return
        
        intial = 0
        for numberRange in range(MAX_NAME_OF_QUERY,len(words),MAX_NAME_OF_QUERY):
            yield "('" + '\',\''.join(words[intial:numberRange]) + "')"
            intial = numberRange
    
        yield "('" + '\',\''.join(words[intial:]) + "')"