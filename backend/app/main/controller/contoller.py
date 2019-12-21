from flask import request
from flask_restplus import Resource
from werkzeug.utils import secure_filename


from ..util.NameSearchDto import NameSearchDto
from ..util.envNames import VERSION,UPLOAD_FOLDER
from ..service.LogService import getAllLog,getFileToDelete,saveLog
from ..util.fileUtils import giveFileNameUnique,giveTypeOfFile,allowedFile
import os

api = NameSearchDto.api

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
            filename = giveFileNameUnique(RealFilename,typeOfFile)
            print(os.path.join(UPLOAD_FOLDER, filename))
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            result['filename'] = filename
            result['realFilename'] = RealFilename
            result['succes'] = True
            result['error'] = None
            result['type'] = typeOfFile
        else:
            result['error'] = "Allowed file types are docx, pdf, xlsx, xlsm, xls, html"
            return result
    return result

@api.route("/")
class index(Resource):
    @api.doc('initial web page')
    def get(self):
        return "Name Search web Service"

@api.route("/version")
class version(Resource):
    @api.doc('show the api version')
    def get(self):
        return {"version":VERSION}

@api.route("/file/encode")
class encode(Resource):
    def post(self):
        return uploadFile()
