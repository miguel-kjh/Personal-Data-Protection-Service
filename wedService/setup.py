import os
import urllib.request
from app import app,version,UPLOAD_FOLDER
from flask import Flask, flash, request, redirect, render_template,send_file
from werkzeug.utils import secure_filename

import re
from DocumentHandler import DocumentHandler,DocumentHandlerDocx,DocumentHandlerExe,DocumentHandlerHTML,DocumentHandlerPDF
from utils import giveTypeOfFile,allowedFile,giveFileNameUnique
from ConnectionFileLog import ConnectionFileLog
from SearcherNamesTexts import SearcherNamesTexts

from languageBuilder import languageBuilder

nlp = languageBuilder().getlanguage()

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
        if 'file' not in request.files:
            result['error'] = "No file part"
            return result
        file = request.files['file']
        if file.filename == '':
            result['error'] = "No file selected for uploading"
            return result
        RealFilename = secure_filename(file.filename)
        result['filename'] = RealFilename
        if file and allowedFile(file.filename):
            typeOfFile = giveTypeOfFile(file.filename)
            con = ConnectionFileLog()
            filename = giveFileNameUnique(RealFilename,typeOfFile)
            identifie = con.insertFileLog(filename,UPLOAD_FOLDER,False,typeOfFile)
            if identifie:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                result['filename'] = filename
                result['realFilename'] = RealFilename
                result['succes'] = True
                result['error'] = None
                result['type'] = typeOfFile
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
        con = ConnectionFileLog()
        con.updateDelete(jsonResult["filename"])
        #TODO HACER ALGO CON LOS FICHEROS GENERADOS
        con.insertFileLog("encode_" + jsonResult["filename"],UPLOAD_FOLDER,False,jsonResult['type']) 
        fileSend = send_file(path, as_attachment=True)
        con.updateDelete("encode_" + jsonResult["filename"])
        return fileSend
    return jsonResult

@app.route('/file/list-names', methods=['POST'])
def getListOfNames():
    jsonResult = uploadFile()
    if jsonResult["succes"]:
        dh = giveDocumentHandler(jsonResult["filename"])
        con = ConnectionFileLog()
        con.updateDelete(jsonResult["filename"])
        return {
            "error":None,
            "succes": True,
            "Names": dh.giveListNames()
        }
    return jsonResult

@app.route('/file/tagger-html', methods=['POST'])
def getHtmlFilesWithNameMarked():
    jsonResult = uploadFile()
    if jsonResult['succes']:
        if jsonResult['type'] == "html":
            path = UPLOAD_FOLDER + "/mark_" + jsonResult["filename"]
            dh = DocumentHandlerHTML(UPLOAD_FOLDER + "/" + jsonResult["filename"],nlp,destiny=path) 
            dh.documentTagger()
            con = ConnectionFileLog()
            con.updateDelete(jsonResult["filename"])
            #TODO HACER ALGO CON LOS FICHEROS GENERADOS
            con.insertFileLog("mark_" + jsonResult["filename"],UPLOAD_FOLDER,False,jsonResult['type']) 
            fileSend = send_file(path, as_attachment=True)
            con.updateDelete("mark_" + jsonResult["filename"])
            return fileSend
        else:
            con = ConnectionFileLog()
            con.updateDelete(jsonResult["filename"])
            return {
                'succes':False,
                'error':"This operation can only exist for html files",
                'filename':jsonResult['realFilename'],
                'type':jsonResult['type']
            }
    return jsonResult

@app.route('/file/csv-file', methods=['POST'])
def giveCsvFile():
    jsonResult = uploadFile()
    if jsonResult['succes']:
        destiny = jsonResult["filename"].replace("."+jsonResult["type"],"_data.csv")
        path = UPLOAD_FOLDER + "/" + destiny
        dh = giveDocumentHandler(jsonResult["filename"],path)
        dh.createFileOfName()
        con = ConnectionFileLog()
        con.updateDelete(jsonResult["filename"])
        con.insertFileLog(destiny,UPLOAD_FOLDER,False,jsonResult['type']) 
        fileResult = send_file(path, as_attachment=True)
        con.updateDelete(destiny)
        return fileResult
    return jsonResult

@app.route('/name-search', methods=['GET'])
def nameSearch():
    try:
        sentence = request.args.get('sentence')     
    except:
        return {
            'succes':False,
            'error': "this URI use get"
        }
    if sentence != None:
        sn = SearcherNamesTexts(nlp)
        listName = sn.searchNames(str(sentence)) 
        return{
            'succes':True,
            'error':None,
            'names':[name['name'] for name in listName]
        }
    else:
        return {
            'succes':False,
            'error':"The parameter are not valid",
        }

if __name__ == "__main__":
    app.run(debug = True)