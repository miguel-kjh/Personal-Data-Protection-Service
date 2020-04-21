from app.test.base import BaseTestCase
from app.main.service.CreateDocumentHandler       import getCreatorDocumentHandler
from app.main.service.DocumentHandler             import DocumentHandler
from app.main.service.DocumentHandlerDocx         import DocumentHandlerDocx
from app.main.service.DocumentHandlerTxt          import DocumentHandlerTxt
from app.main.service.DocumentHandlerHtml         import DocumentHandlerHtml
from app.main.service.DocumentHandlerPdf          import DocumentHandlerPdf
from app.main.service.DocumentHandlerSpreadsheets import DocumentHandlerCsv,DocumentHandlerExcel
from app.test.fileVariables                       import pathTables,pathTexts,pathWeb
from app.main.util.anonymizationFunctions         import encode

import unittest


class TestDocumentHandler(BaseTestCase):
    
    def test_creator(self):
        creator = getCreatorDocumentHandler( pathTables + "1.xls",'xls')
        self.assertTrue(isinstance(creator.create(), DocumentHandler))
        self.assertTrue(isinstance(creator.create(), DocumentHandlerExcel))

        creator = getCreatorDocumentHandler("file.pdf",'pdf')
        self.assertTrue(isinstance(creator.create(), DocumentHandlerPdf))

        creator = getCreatorDocumentHandler("file.txt",'txt')
        self.assertTrue(isinstance(creator.create(), DocumentHandlerTxt))

        creator = getCreatorDocumentHandler(pathTexts + "1.docx",'docx')
        self.assertTrue(isinstance(creator.create(), DocumentHandlerDocx))

        creator = getCreatorDocumentHandler(pathWeb + "1.html",'html')
        self.assertTrue(isinstance(creator.create(), DocumentHandlerHtml))

        

        creator = getCreatorDocumentHandler( pathTables + "1.xls",'xls', encode)
        self.assertTrue(isinstance(creator.create(), DocumentHandler))
        self.assertTrue(isinstance(creator.create(), DocumentHandlerExcel))

        creator = getCreatorDocumentHandler("file.pdf",'pdf',encode)
        self.assertTrue(isinstance(creator.create(), DocumentHandlerPdf))

        creator = getCreatorDocumentHandler("file.txt",'txt',encode)
        self.assertTrue(isinstance(creator.create(), DocumentHandlerTxt))

        creator = getCreatorDocumentHandler(pathTexts + "1.docx",'docx',encode)
        self.assertTrue(isinstance(creator.create(), DocumentHandlerDocx))

        creator = getCreatorDocumentHandler(pathWeb + "1.html",'html',encode)
        self.assertTrue(isinstance(creator.create(), DocumentHandlerHtml))

    def test_handler(self):
        dh = DocumentHandlerPdf(pathTexts + "1.pdf")
        self.assertTrue(len(dh.extractData()) > 0)

        dh = DocumentHandlerPdf(pathTexts + "1.pdf",encode)
        self.assertTrue(len(dh.extractData()) > 0)

        dh = DocumentHandlerDocx(pathTexts + "1.docx")
        self.assertTrue(len(dh.extractData()) > 0)

        dh = DocumentHandlerDocx(pathTexts + "1.docx",encode)
        self.assertTrue(len(dh.extractData()) > 0)

        dh = DocumentHandlerTxt(pathTexts + "1.txt")
        self.assertTrue(len(dh.extractData()) > 0)

        dh = DocumentHandlerTxt(pathTexts + "1.txt",encode)
        self.assertTrue(len(dh.extractData()) > 0)

        dh = DocumentHandlerHtml(pathWeb + "6.html")
        self.assertTrue(len(dh.extractData()) > 0)

        dh = DocumentHandlerHtml(pathWeb + "6.html", encode)
        self.assertTrue(len(dh.extractData()) > 0)

        dh = DocumentHandlerExcel(pathTables + "1.xls")
        self.assertTrue(len(dh.extractData()) > 0)

        dh = DocumentHandlerExcel(pathTables + "1.xls", encode)
        self.assertTrue(len(dh.extractData()) > 0)

if __name__ == "__main__":
    unittest.main()

