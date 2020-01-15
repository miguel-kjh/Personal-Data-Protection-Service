import re
from datetime import datetime

import pandas as pd

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
import app.main.service.pdf_redactor as pdf_redactor

import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

from app.main.service.utils import proc_pdf3k, proc_docx, run_append, encode, iter_block_items, markInHtml
from app.main.service.NameSearchByGenerator import NameSearchByGenerator
from app.main.service.NameSearchByEntities import NameSearchByEntities


class DocumentHandler():

    def __init__(self, path:str,destiny:str = ""):
        self.path = path
        self.destiny = destiny
        self.nameSearch = NameSearchByGenerator()

    def documentsProcessing(self):
        pass

    #def documentTagger(self):
        #pass

    def createFileOfName(self):
        self.createCsv(self.giveListNames())

    def giveListNames(self):
        pass

    def createCsv(self, listNames:list):
        dataFrame = pd.DataFrame(listNames, columns=['Names'])
        export_csv = dataFrame.to_csv(self.destiny, index = None, header=True)
        print(export_csv)

#TODO? optimize
class DocumentHandlerPDF(DocumentHandler):

    def __init__(self, path:str,destiny:str = ""):
        super().__init__(path,destiny=destiny)
        self.options = pdf_redactor.RedactorOptions()
        self.options.metadata_filters = {
            "Title": [lambda value: value],

            "Producer": [lambda value: value],
            "CreationDate": [lambda value: datetime.utcnow()],

            "DEFAULT": [lambda value: None],
        }
        self.options.xmp_filters = [lambda xml: None]

    def giveListNames(self) -> list:
        fp = open(self.path, 'rb')
        parser = PDFParser(fp)
        fp.close()
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize('')
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        laparams.char_margin = 1.0
        laparams.word_margin = 1.0
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        listNames = []
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for lt_obj in layout:
                if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                    for text in lt_obj.get_text().split("\n"):
                        if text != '':
                            doc = self.nameSearch.searchNames(text)
                            for e in doc:
                                listNames.append(e['name'].strip("\n"))
        return list(set(listNames))

    def documentsProcessing(self):
        listNames = self.giveListNames()
        #print(listNames[:])
        if len(listNames) > 0:
            listNames.sort(
                key=lambda value: len(value),
                reverse=True
            )
            self.options.content_filters = [
                (
                    re.compile(listNames[0]),
                    lambda m: encode(listNames[0]).upper()
                )
            ]
            pdf_redactor.redactor(self.options, self.path, self.destiny)
            for name in listNames[1:]:
                self.options.content_filters = [
                    (
                        re.compile(name),
                        lambda m: encode(name).upper()
                    )
                ]
                pdf_redactor.redactor(self.options, self.destiny, self.destiny)
        


class DocumentHandlerDocx(DocumentHandler):

    def __init__(self, path:str,destiny:str = ""):
        super().__init__(path,destiny=destiny)
        self.document = docx.Document(self.path)

    def documentsProcessing(self):
        for block in iter_block_items(self.document):
            if isinstance(block, Paragraph):
                inline = block.runs
                for line in inline:
                    listNames = self.nameSearch.searchNames(line.text)
                    for name in listNames:
                        regexName = re.compile(name['name'])
                        if regexName.search(line.text):
                            text = regexName.sub(encode(name['name']), line.text)
                            line.text = text
            elif isinstance(block, Table):
                for row in block.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            inline = paragraph.runs
                            for line in inline:
                                listNames = self.nameSearch.searchNames(line.text)
                                for name in listNames:
                                    regexName = re.compile(name['name'])
                                    if regexName.search(line.text):
                                        text = regexName.sub(encode(name['name']), line.text)
                                        line.text = text    
            else:
                continue
        self.document.save(self.destiny)
         

    def giveListNames(self) -> list:
        doc = docx.Document(self.path)
        listNames = []
        for block in iter_block_items(doc):
            if isinstance(block, Paragraph):
                listOfMarks = self.nameSearch.searchNames(block.text)
                if listOfMarks != []:
                    listNames[len(listNames):] = [name['name'] for name in listOfMarks]
            elif isinstance(block, Table):
                for row in block.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            listOfMarks = self.nameSearch.searchNames(paragraph.text)
                            if listOfMarks != []:
                                listNames[len(listNames):] = [name['name'] for name in listOfMarks]
            else:
                continue
        return listNames
        

class DocumentHandlerExel(DocumentHandler):

    def __init__(self,path:str,destiny:str = ""):
        super().__init__(path,destiny=destiny)
        self.df = pd.read_excel(path)

    #TODO? save formules.
    def documentsProcessing(self):
        for key in self.df.keys():
            for index,ele in enumerate(self.df[key]):
                if self.nameSearch.isName(str(ele)):
                    self.df.at[index,key] = encode(str(ele))
        self.df.to_excel(self.destiny)

    def giveListNames(self):
        listNames = []
        for key in self.df.keys():
            for ele in self.df[key]:
                if self.nameSearch.isName(str(ele)):
                    listNames.append(str(ele))
        return listNames

class DocumentHandlerHTML(DocumentHandler):

    def __init__(self,path:str,destiny:str = ""):
        super().__init__(path,destiny=destiny)
        with open(self.path,"r", encoding="utf8") as f:
            self.soup = BeautifulSoup(f.read(), "lxml")

    def locateNames(self,sentence):
        listNames = self.nameSearch.searchNames(str(sentence))
        if listNames is []:
            return sentence
        newSentence = ""
        index = 0
        for name in listNames:
            newSentence += sentence[index:name['star_char']] + markInHtml(name['name'])
            index = name['end_char']
        if index <= len(sentence)-1:
            newSentence += sentence[index:]
        return newSentence

    def encodeNames(self,sentence):
        listNames = self.nameSearch.searchNames(str(sentence))
        if listNames is []:
            return sentence
        newSentence = ""
        index = 0
        for name in listNames:
            newSentence += sentence[index:name['star_char']] + encode(name['name'])
            index = name['end_char']
        if index <= len(sentence)-1:
            newSentence += sentence[index:]
        return newSentence

    def documentsProcessing(self):
        formatter = HTMLFormatter(self.encodeNames)
        with open(self.destiny,"w") as f:
            f.write(self.soup.prettify(formatter=formatter))

    def documentTagger(self):
        formatter = HTMLFormatter(self.locateNames)
        with open(self.destiny,"w") as f:
            f.write(self.soup.prettify(formatter=formatter))

    def giveListNames(self):
        listNames = []
        blacklist = [ '[document]' , 'noscript' , 'header' , 
        'html' , 'meta' , 'head' , 'input' , 'script', 'link', 'lang']
        for lable in self.soup.find_all(text=True):
            if lable not in blacklist:
                #print(lable)
                listOfMarks = self.nameSearch.searchNames(str(lable))
                listNames[len(listNames):] = [name['name'].replace("\n","") for name in listOfMarks]
        return listNames



