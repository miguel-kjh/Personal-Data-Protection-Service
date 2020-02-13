from flask import request, send_from_directory
from flask_restplus import Resource
from werkzeug.utils import secure_filename

from ..util.NameSearchDto import NameSearchDto
from ..util.envNames import VERSION, UPLOAD_FOLDER, path, ALLOWED_EXTENSIONS
from ..service.LogService import updateDelete, saveLog
from ..service.languageBuilder import LanguageBuilder
from ..service.CreateDocumentHandler import getCreatorDocumentHandler
from ..util.fileUtils import giveFileNameUnique, giveTypeOfFile, allowedFile
import os

api = NameSearchDto.api

lb = LanguageBuilder()
lb.defineNameEntity()  # Load model before a conections


def uploadFile() -> dict:
    result = {
        "filename": None,
        "success": False,
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
        realFilename = secure_filename(file.filename)
        result['filename'] = realFilename
        if file and allowedFile(file.filename):
            typeOfFile = giveTypeOfFile(file.filename)
            filename = giveFileNameUnique(realFilename, typeOfFile)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            result['filename'] = filename
            result['realFilename'] = realFilename
            result['success'] = True
            result['error'] = None
            result['type'] = typeOfFile
        else:
            result['error'] = "Allowed file types are %s" % (','.join(ALLOWED_EXTENSIONS))
            return result
    return result


@api.route("/")
class Index(Resource):
    @api.doc('initial operation')
    def get(self):
        return "Name Search web Service"


@api.route("/version")
class Version(Resource):
    @api.doc('show the api version')
    def get(self):
        return {"version": VERSION}


@api.route("/file/encode")
class Encode(Resource):
    @api.doc('return a file with names encoded')
    def post(self):
        res = uploadFile()
        if res['success']:
            publicId = saveLog(
                {
                    'name': res['filename'],
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': res['type']
                }
            )
            nameOfNewDocument = "encode_" + res["filename"]
            creator = getCreatorDocumentHandler(
                os.path.join(path, res["filename"]),
                res['type'],
                os.path.join(path, nameOfNewDocument)
            )
            dh = creator.create()
            dh.documentsProcessing()
            updateDelete(publicId, True)
            publicId = saveLog(
                {
                    'name': nameOfNewDocument,
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': res['type']
                }
            )
            fileSend = send_from_directory(path, nameOfNewDocument, as_attachment=True)
            updateDelete(publicId, True)
            return fileSend
        else:
            return res, 400


@api.route('/file/list-names')
class ListNames(Resource):
    @api.doc('give a list of name in the document')
    def post(self):
        res = uploadFile()
        if res['success']:
            publicId = saveLog(
                {
                    'name': res['filename'],
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': res['type']
                }
            )
            creator = getCreatorDocumentHandler(
                os.path.join(path, res["filename"]),
                res['type']
            )
            dh = creator.create()
            names = dh.giveListNames()
            updateDelete(publicId, True)
            return {
                       "error": None,
                       "success": True,
                       "Names": names
                   }
        else:
            return res, 400


@api.route('/file/csv-file')
class CsvFile(Resource):
    @api.doc('return a csv file with names of file sent')
    def post(self):
        res = uploadFile()
        if res['success']:
            publicId = saveLog(
                {
                    'name': res['filename'],
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': res['type']
                }
            )
            nameOfNewDocument = res["filename"].replace('.' + res['type'], ".csv")
            creator = getCreatorDocumentHandler(
                os.path.join(path, res["filename"]),
                res['type'],
                os.path.join(path, nameOfNewDocument)
            )
            dh = creator.create()
            dh.createFileOfName()
            updateDelete(publicId, True)
            publicId = saveLog(
                {
                    'name': nameOfNewDocument,
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': res['type']
                }
            )
            fileSend = send_from_directory(path, nameOfNewDocument, as_attachment=True)
            updateDelete(publicId, True)
            return fileSend
        else:
            return res, 400


@api.route('/file/tagger-html')
class TargetHtml(Resource):
    @api.doc('return a html file with the names targeted with a mark')
    def post(self):
        res = uploadFile()
        if res['success']:
            if res['type'] != 'html':
                filename = os.path.join(UPLOAD_FOLDER, res['filename'])
                if os.path.exists(filename):
                    os.remove(filename)
                return {
                           "filename": res['realFilename'],
                           "success": False,
                           "error": "this operation is aviable only for html file"
                       }, 400
            publicId = saveLog(
                {
                    'name': res['filename'],
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': res['type']
                }
            )
            nameOfNewDocument = "mark_" + res["filename"]
            creator = getCreatorDocumentHandler(
                os.path.join(path, res["filename"]),
                res['type'],
                os.path.join(path, nameOfNewDocument)
            )
            dh = creator.create()
            dh.documentTagger()
            updateDelete(publicId, True)
            publicId = saveLog(
                {
                    'name': nameOfNewDocument,
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': res['type']
                }
            )
            fileSend = send_from_directory(path, nameOfNewDocument, as_attachment=True)
            updateDelete(publicId, True)
            return fileSend
        else:
            return res, 400
