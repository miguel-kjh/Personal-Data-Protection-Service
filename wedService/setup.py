import os
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template,send_file
from werkzeug.utils import secure_filename

import spacy
import re
from DocumentHandler import DocumentHandler,DocumentHandlerDocx,DocumentHandlerExe,DocumentHandlerHTML,DocumentHandlerPDF

nlp = spacy.load("es_core_news_md")
print("model load")

version = "alpha 1.0"
ALLOWED_EXTENSIONS = set(['docx', 'pdf', 'xlsx', 'xlsm', 'xls', 'html'])
def allowedFile(filename:str) -> bool:
	return giveTypeOfFile(filename) in ALLOWED_EXTENSIONS

def giveTypeOfFile(filename:str) -> str:
    return '.' in filename and filename.rsplit('.', 1)[1].lower()

def giveDocumentHandler(filename:str,destiny:str="") -> DocumentHandler:
    typeFile = giveTypeOfFile(filename)
    filename = "files_to_processing/" + filename
    destiny = destiny
    print(destiny)
    if typeFile == "docx":
        dh = DocumentHandlerDocx(filename,nlp,destiny=destiny)
    elif typeFile == "pdf":
        dh = DocumentHandlerPDF(filename,nlp,destiny=destiny)
    elif typeFile in ['xlsx', 'xlsm', 'xls']:
        dh = DocumentHandlerExe(filename,nlp,destiny=destiny)
    elif typeFile == "html":
        dh = DocumentHandlerHTML(filename,nlp,destiny=destiny)
    return dh

def uploadFile() -> dict:
    result = {
        "filename":None,
        "succes":False,
        "error": "do not send with POST"
    }
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            result['error'] = "No file part"
            return result
        file = request.files['file']
        if file.filename == '':
            result['error'] = "No file selected for uploading"
            return result
        if file and allowedFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result['filename'] = filename
            result['succes'] = True
            result['error'] = None
        else:
            result['error'] = "Allowed file types are docx, pdf, xlsx, xlsm, xls, html"
            return result
    return result


@app.route('/')
def main():
    return "hello, version aplha 1.0"

@app.route('/version')
def getVersion():
    return {
        "version":version
    }

@app.route('/file')
def getOperations():
    return {
        "operations":"encode,target,give list of names and give csv of names"
    }

@app.route('/file/encode', methods=['POST'])
def getFileEncode():
    jsonResult = uploadFile()
    if jsonResult['succes']:
        path = "files_to_delete/encode_" + jsonResult["filename"]
        dh = giveDocumentHandler(jsonResult["filename"], path)
        dh.documentsProcessing()
        return send_file(path, as_attachment=True)
    return jsonResult

@app.route('/file/listNames', methods=['POST'])
def getListOfNames():
    jsonResult = uploadFile()
    if jsonResult["succes"]:
        dh = giveDocumentHandler(jsonResult["filename"])
        result = {
            "error":None,
            "succes": True,
            "Names": dh.giveListNames()
        }
        return result
    return jsonResult

@app.route('/file/target/htmlFile', methods=['POST'])
def getHtmlFilesWithNameMarked():
    jsonResult = uploadFile()
    if jsonResult['succes']:
        if giveTypeOfFile(jsonResult["filename"]) == "html":
            path = "files_to_delete/mark_" + jsonResult["filename"]
            dh = DocumentHandlerHTML("files_to_processing/" + jsonResult["filename"],nlp,destiny=path) 
            dh.documentTagger()
            return send_file(path, as_attachment=True)
        else:
            jsonResult['succes'] = False
            jsonResult['error'] = "This operation can only exist for html files"
    return jsonResult

@app.route('/file/giveCsvFile', methods=['POST'])
def giveCsvFile():
    jsonResult = uploadFile()
    if jsonResult['succes']:
        dh = giveDocumentHandler(
            jsonResult["filename"],
            "files_to_delete/" + jsonResult["filename"].replace(
                "."+giveTypeOfFile(jsonResult["filename"]),
                "_data.csv"))
        path = dh.createFileOfName()
        print(path)
        return send_file(path, as_attachment=True)
    return jsonResult

if __name__ == "__main__":
    app.run(debug = True)