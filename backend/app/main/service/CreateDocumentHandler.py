from app.main.service.DocumentHandler             import DocumentHandler
from app.main.service.DocumentHandlerTxt          import DocumentHandlerTxt
from app.main.service.DocumentHandlerSpreadsheets import DocumentHandlerExcel,DocumentHandlerCsv
from app.main.service.DocumentHandlerPdf          import DocumentHandlerPdf
from app.main.service.DocumentHandlerDocx         import DocumentHandlerDocx
from app.main.service.DocumentHandlerHtml         import DocumentHandlerHtml

from abc import ABC, abstractmethod



def getCreatorDocumentHandler(filename: str, typeFile: str, destiny: str = "", anonymizationFunction = None, isUrl:bool = False):
    """  
    Analyzes the file and returns a suitable object CreatorDocumentHandler according to its characteristics.

    :param filename: file path
    :param typeFile: type of file
    :param destiny: destination file path
    :param anonymizationFunction: data encryption function
    :param isUrl: whether or not it's a url
    :return: CreatorDocumentHandler
    """
    if isUrl:
        return CreatorDocumentHandlerHtml(filename, destiny,anonymizationFunction, isUrl)

    if   typeFile == 'docx':
        return CreatorDocumentHandlerDocx(filename, destiny,anonymizationFunction)
    elif typeFile == 'pdf':
        return CreatorDocumentHandlerPdf(filename, destiny,anonymizationFunction)
    elif typeFile in ['xlsx', 'xlsm', 'xls']:
        return CreatorDocumentHandlerExcel(filename, destiny,anonymizationFunction)
    elif typeFile == 'csv':
        return CreatorDocumentHandlerCsv(filename, destiny,anonymizationFunction)
    elif typeFile == 'html':
        return CreatorDocumentHandlerHtml(filename, destiny,anonymizationFunction)
    elif typeFile == 'txt':
        return CreatorDocumentHandlerTxt(filename, destiny,anonymizationFunction)
    else:
        raise RuntimeError("Error CreatorDocumentHandler: type %s do not recognize" % (typeFile))


class CreatorDocumentHandler(ABC):

    def __init__(self, path: str, destiny: str, anonymizationFunction):
        self.path                  = path
        self.destiny               = destiny
        self.anonymizationFunction = anonymizationFunction

    @abstractmethod
    def create(self):
        """
        Creates a suitable HandlerDocument object.
        """
        pass


class CreatorDocumentHandlerDocx(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerDocx(self.path, self.destiny,self.anonymizationFunction)

class CreatorDocumentHandlerExcel(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerExcel(self.path, self.destiny,self.anonymizationFunction)

class CreatorDocumentHandlerPdf(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerPdf(self.path, self.destiny,self.anonymizationFunction)

class CreatorDocumentHandlerCsv(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerCsv(self.path, self.destiny,self.anonymizationFunction)

class CreatorDocumentHandlerHtml(CreatorDocumentHandler):
    def __init__(self,path: str, destiny: str, anonymizationFunction, isUrl = False):
        super().__init__(path, destiny, anonymizationFunction)
        self.isUrl = isUrl
    
    def create(self) -> DocumentHandler:
        return DocumentHandlerHtml(self.path, self.destiny,self.anonymizationFunction,self.isUrl)

class CreatorDocumentHandlerTxt(CreatorDocumentHandler):
    def create(self) -> DocumentHandler:
        return DocumentHandlerTxt(self.path, self.destiny,self.anonymizationFunction)
