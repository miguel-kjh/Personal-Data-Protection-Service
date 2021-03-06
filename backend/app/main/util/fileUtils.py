from app.main.util.envNames          import ALLOWED_EXTENSIONS

import uuid

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
    return str(uuid.uuid4()).replace(".", "") + "." + fileType

def itemIterator(parent):
    """
    Browse the elements of a docx document
    :param parent: a python-docx Document
    :yield: a python-docx object (Paragraph or Table)
    """

    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    elif isinstance(parent, _Row):
        parent_elm = parent._tr
    else:
        raise ValueError("the Docx document have object what didn't implemented in the iterator")
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def readPdf(path:str) -> tuple:
    """
    Read a pdf iterating about the tables and texts
    :param path: file path
    :yield: tuple(text, list of tables)
    """
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

lettersOfDni = "TRWAGMYFPDXBNJZSQVHLCKE"
def isDni(dni:str) -> bool:
    """
    Find out if the entry string is an DNI or not
    :param dni: string
    :return: boolean
    """
    number = ''.join(filter(str.isdigit, dni))
    if not number or lettersOfDni[int(number) % 23] != dni[-1].upper():
        return False
    
    return True

def normalizeUnicode(string: str) -> str:
    """
    Normalizes a string to a unicode by skipping the 'ñ'
    :param string: string
    :return: normalize string
    """
    letersÑ = list(filter(lambda x: string[x].lower() == 'ñ', range(0,len(string))))
    if not letersÑ:
        return unidecode(string)
    result = unidecode(string)
    return ''.join(['ñ' if index in letersÑ else char for index,char in enumerate(result)])
    

MAX_NAME_OF_QUERY = 4000
def generateWordsAsString(words:list) -> str:
    """
    Converts a maximum number of words in a list into a string by 
    separating them by commas and with parentheses.
    :param: list of string
    :yield: string
    """
    if len(words) < MAX_NAME_OF_QUERY:
        yield "('" + '\',\''.join(words) + "')"
        return
    
    intial = 0
    for numberRange in range(MAX_NAME_OF_QUERY,len(words),MAX_NAME_OF_QUERY):
        yield "('" + '\',\''.join(words[intial:numberRange]) + "')"
        intial = numberRange

    yield "('" + '\',\''.join(words[intial:]) + "')"

def replaceUnnecessaryCharacters(text:str) -> str:
    return re.sub(r'\(|\)|\[|\]|\|', '', text)