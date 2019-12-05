import os
import urllib.request
from app import app,version,UPLOAD_FOLDER
from flask import Flask, flash, request, redirect, render_template,send_file
from werkzeug.utils import secure_filename

import spacy
import re
from DocumentHandler import DocumentHandler,DocumentHandlerDocx,DocumentHandlerExe,DocumentHandlerHTML,DocumentHandlerPDF
from utils import giveTypeOfFile,allowedFile
from ConnectionFilesInformationDB import ConnectionFilesInformation

nlp = spacy.load("es_core_news_sm")
print("model load")

def giveDocumentHandler(filename:str,destiny:str="") -> DocumentHandler:
    typeFile = giveTypeOfFile(filename)
    filename =  UPLOAD_FOLDER + "/" + filename
    destiny = destiny
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
            typeOfFile = giveTypeOfFile(file.filename)
            con = ConnectionFilesInformation()
            identifie = con.insertDataFiles(file.filename,UPLOAD_FOLDER,False,typeOfFile)
            print(identifie)
            if type(identifie) != bool:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                result['filename'] = filename
                result['succes'] = True
                result['error'] = None
                result['type'] = typeOfFile
                result['id'] = identifie
            else:
                result['succes'] = False
                result['error'] = "Error in serve storage"
        else:
            result['error'] = "Allowed file types are docx, pdf, xlsx, xlsm, xls, html"
            return result
    return result


@app.route('/')
def main():
    return "hello, version " + version

@app.route('/version')
def getVersion():
    return {
        "version":version
    }

@app.route('/file/encode', methods=['POST'])
def getFileEncode():
    jsonResult = uploadFile()
    if jsonResult['succes']:
        path =  UPLOAD_FOLDER + "/encode_" + jsonResult["filename"]
        dh = giveDocumentHandler(jsonResult["filename"], path)
        dh.documentsProcessing()
        con = ConnectionFilesInformation()
        identifie = con.insertDataFiles("encode_" + jsonResult["filename"],UPLOAD_FOLDER,False,jsonResult['type'])
        print(identifie)
        return send_file(path, as_attachment=True)
    return jsonResult

@app.route('/file/list-names', methods=['POST'])
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

@app.route('/file/tagger-html', methods=['POST'])
def getHtmlFilesWithNameMarked():
    jsonResult = uploadFile()
    if jsonResult['succes']:
        if giveTypeOfFile(jsonResult["filename"]) == "html":
            path = UPLOAD_FOLDER + "/mark_" + jsonResult["filename"]
            dh = DocumentHandlerHTML("files_to_processing/" + jsonResult["filename"],nlp,destiny=path) 
            dh.documentTagger()
            return send_file(path, as_attachment=True)
        else:
            jsonResult['succes'] = False
            jsonResult['error'] = "This operation can only exist for html files"
    return jsonResult

@app.route('/file/csv-file', methods=['POST'])
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