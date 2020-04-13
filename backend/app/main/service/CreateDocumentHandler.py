from abc import ABC, abstractmethod
from app.main.service.DocumentHandler import DocumentHandler
from app.main.service.DocumentHandlerTxt import DocumentHandlerTxt
from app.main.service.DocumentHandlerSpreadsheets import DocumentHandlerExcel,DocumentHandlerCsv
from app.main.service.DocumentHandlerPdf import DocumentHandlerPdf
from app.main.service.DocumentHandlerDocx import DocumentHandlerDocx
from app.main.service.DocumentHandlerHtml import DocumentHandlerHtml


def getCreatorDocumentHandler(filename: str, typeFile: str, destiny: str = ""):
    if   typeFile == 'docx':
        return CreatorDocumentHandlerDocx(filename, destiny)
    elif typeFile == 'pdf':
        return CreatorDocumentHandlerPdf(filename, destiny)
    elif typeFile in ['xlsx', 'xlsm', 'xls']:
        return CreatorDocumentHandlerExcel(filename, destiny)
    elif typeFile == 'csv':
        return CreatorDocumentHandlerCsv(filename, destiny)
    elif typeFile == 'html':
        return CreatorDocumentHandlerHtml(filename, destiny)
    elif typeFile == 'txt':
        return CreatorDocumentHandlerTxt(filename, destiny)
    else:
        raise RuntimeError("Error CreatorDocumentHandler: type %s do not recognize" % (typeFile))


class CreatorDocumentHandler(ABC):

    def __init__(self, path: str, destiny: str):
        self.path = path
        self.destiny = destiny

    @abstractmethod
    def create(self):
        pass


class CreatorDocumentHandlerDocx(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerDocx(self.path, self.destiny)

class CreatorDocumentHandlerExcel(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerExcel(self.path, self.destiny)

class CreatorDocumentHandlerPdf(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerPdf(self.path, self.destiny)

class CreatorDocumentHandlerCsv(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerCsv(self.path, self.destiny)

class CreatorDocumentHandlerHtml(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerHtml(self.path, self.destiny)

class CreatorDocumentHandlerTxt(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerTxt(self.path, self.destiny)
