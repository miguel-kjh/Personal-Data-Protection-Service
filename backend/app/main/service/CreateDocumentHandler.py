from abc import ABC,abstractmethod
from app.main.service.DocumentHandler import DocumentHandler,DocumentHandlerDocx,DocumentHandlerExcel,DocumentHandlerHTML,DocumentHandlerPDF

def getCreatorDocumentHandler(filename:str,typeFile:str,destiny:str=""):
    if typeFile == "docx":
        return CreatorDocumentHandlerDocx(filename,destiny)
    elif typeFile == "pdf":
        return CreatorDocumentHandlerPdf(filename,destiny)
    elif typeFile in ['xlsx', 'xlsm', 'xls']:
        return CreatorDocumentHandlerExcel(filename,destiny)
    elif typeFile == "html":
        return CreatorDocumentHandlerHtml(filename,destiny)
    else:
        raise ValueError("type recorder without")

class CreatorDocumentHandler(ABC):

    def __init__(self, path:str,destiny:str):
        self.path = path
        self.destiny = destiny
    
    @abstractmethod
    def create(self):
        pass

class CreatorDocumentHandlerDocx(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerDocx(self.path,self.destiny)

class CreatorDocumentHandlerExcel(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerExcel(self.path,self.destiny)

class CreatorDocumentHandlerPdf(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerPDF(self.path,self.destiny)

class CreatorDocumentHandlerHtml(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerHTML(self.path,self.destiny)
