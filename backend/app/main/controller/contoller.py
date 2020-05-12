from ..util.NameSearchDto            import NameSearchDto
from ..util.envNames                 import VERSION, UPLOAD_FOLDER, path
from ..service.LogService            import updateDelete, saveLog
from ..service.languageBuilder       import LanguageBuilder
from ..service.CreateDocumentHandler import getCreatorDocumentHandler
from ..util.RequestEvaluator         import RequestEvaluator
from ..util.anonymizationFunctions   import encode,markInHtml


from flask import request, send_from_directory
from flask_restplus import Resource

import os

api = NameSearchDto.api

# Load model before a conections
lb = LanguageBuilder()
lb.defineRulesOfNames()


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
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            publicId = saveLog(
                {
                    'name'    : evaluator.fakeFilename,
                    'folder'  : UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
            nameOfNewDocument = "encode_" + evaluator.fakeFilename
            creator = getCreatorDocumentHandler(
                os.path.join(path, evaluator.fakeFilename),
                evaluator.filetype,
                os.path.join(path, nameOfNewDocument),
                encode
            )
            dh = creator.create()
            dh.documentsProcessing()
            updateDelete(publicId, True)
            publicId = saveLog(
                {
                    'name'    : nameOfNewDocument,
                    'folder'  : UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
            fileSend = send_from_directory(path, nameOfNewDocument, as_attachment=True)
            updateDelete(publicId, True)
            return fileSend
        else:
            return evaluator.giveResponse(), 400


@api.route('/file/extract-data/json')
class extractDataJson(Resource):
    @api.doc('give a list of name in the document')
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            publicId = saveLog(
                {
                    'name'    : evaluator.fakeFilename,
                    'folder'  : UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
            creator = getCreatorDocumentHandler(
                os.path.join(path, evaluator.fakeFilename),
                evaluator.filetype
            )
            dh = creator.create()
            names,idCards = dh.extractData()
            updateDelete(publicId, True)
            return {
                       "error"  : None,
                       "success": True,
                       "Names"  : names,
                       "IdCards": idCards
                   }
        else:
            return evaluator.giveResponse(), 400

@api.route('/file/extract-data/json-file')
class extractDataJsonFile(Resource):
    @api.doc('return a json file with all data found')
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            publicId = saveLog(
                {
                    'name': evaluator.fakeFilename,
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
            nameOfNewDocument = evaluator.fakeFilename.replace('.' + evaluator.filetype, ".json")
            creator = getCreatorDocumentHandler(
                os.path.join(path, evaluator.fakeFilename),
                evaluator.filetype,
                os.path.join(path, nameOfNewDocument)
            )
            dh = creator.create()
            dh.createDataJsonFile()
            updateDelete(publicId, True)
            publicId = saveLog(
                {
                    'name': nameOfNewDocument,
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
            fileSend = send_from_directory(path, nameOfNewDocument, as_attachment=True)
            updateDelete(publicId, True)
            return fileSend
        else:
            return evaluator.giveResponse(), 400


@api.route('/file/extract-data/zip')
class extractDataZip(Resource):
    @api.doc('return a zip folder with all data found grouped in CSV files')
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            publicId = saveLog(
                {
                    'name': evaluator.fakeFilename,
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
            nameOfNewDocument = evaluator.fakeFilename.replace('.' + evaluator.filetype, ".zip")
            creator = getCreatorDocumentHandler(
                os.path.join(path, evaluator.fakeFilename),
                evaluator.filetype,
                os.path.join(path, nameOfNewDocument)
            )
            dh = creator.create()
            dh.createDataZipFolder()
            updateDelete(publicId, True)
            publicId = saveLog(
                {
                    'name': nameOfNewDocument,
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
            fileSend = send_from_directory(path, nameOfNewDocument, as_attachment=True)
            updateDelete(publicId, True)
            return fileSend
        else:
            return evaluator.giveResponse(), 400


@api.route('/file/tagger-html')
class TargetHtml(Resource):
    @api.doc('return a html file with the names targeted with a mark')
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            if evaluator.filetype != 'html':
                filename = os.path.join(UPLOAD_FOLDER, evaluator.fakeFilename)
                if os.path.exists(filename):
                    os.remove(filename)
                return {
                           "filename": evaluator.filename,
                           "success": False,
                           "error": "this operation is aviable only for html file"
                       }, 400
            publicId = saveLog(
                {
                    'name': evaluator.fakeFilename,
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
            nameOfNewDocument = "mark_" + evaluator.fakeFilename
            creator = getCreatorDocumentHandler(
                os.path.join(path, evaluator.fakeFilename),
                evaluator.filetype,
                os.path.join(path, nameOfNewDocument),
                markInHtml
            )
            dh = creator.create()
            dh.documentsProcessing()
            updateDelete(publicId, True)
            publicId = saveLog(
                {
                    'name': nameOfNewDocument,
                    'folder': UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
            fileSend = send_from_directory(path, nameOfNewDocument, as_attachment=True)
            updateDelete(publicId, True)
            return fileSend
        else:
            return evaluator.giveResponse(), 400
