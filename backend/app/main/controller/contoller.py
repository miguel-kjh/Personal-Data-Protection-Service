from ..util.NameSearchDto            import NameSearchDto
from ..util.envNames                 import VERSION, UPLOAD_FOLDER, path
from ..service.LogService            import updateDelete, saveLog
from ..service.languageBuilder       import LanguageBuilder
from ..service.CreateDocumentHandler import getCreatorDocumentHandler
from ..util.RequestEvaluator         import RequestEvaluator
from ..util.fileUtils                import giveFileNameUnique
from ..util.anonymizationFunctions   import encode,markInHtml,disintegration,dataObfuscation


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

def registerOperation(evaluator: RequestEvaluator, function:classmethod, nameOperation:str):
    publicId = saveLog(
                {
                    'name'    : evaluator.fakeFilename,
                    'folder'  : UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
    nameOfNewDocument = '%s_%s' %(nameOperation, evaluator.fakeFilename)
    creator = getCreatorDocumentHandler(
        os.path.join(path, evaluator.fakeFilename),
        evaluator.filetype,
        os.path.join(path, nameOfNewDocument),
        function
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

@api.route("/file/encode")
class Anonimization(Resource):

    @api.doc('return a file with names encoded')
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            return registerOperation(evaluator,encode, "anom")
        else:
            return evaluator.giveResponse(), 400

@api.route("/file/disintegration")
class Disintegration(Resource):

    @api.doc('return a file with names encoded')
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            return registerOperation(evaluator,disintegration,"dis")
        else:
            return evaluator.giveResponse(), 400

@api.route("/file/obfuscation")
class Obfuscation(Resource):

    @api.doc('return a file with names encoded')
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            return registerOperation(evaluator,dataObfuscation,"ofus")
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


@api.route('/file/extract-data/csv')
class extractDataCsv(Resource):
    @api.doc('return a csv files with all data founded')
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
            nameOfNewDocument = evaluator.fakeFilename.replace('.' + evaluator.filetype, ".csv")
            creator = getCreatorDocumentHandler(
                os.path.join(path, evaluator.fakeFilename),
                evaluator.filetype,
                os.path.join(path, nameOfNewDocument)
            )
            dh = creator.create()
            dh.createDataCsvFile()
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


@api.route('/file/operation-web')
@api.param('url', 'Url form a web site')
@api.param('op',  'Operation to a html file')
class operationWeb(Resource):

    def _json(self, url:str):
        name    = giveFileNameUnique('json')
        creator = getCreatorDocumentHandler(
                url,
                'html',
                os.path.join(path, name),
                isUrl=True
        )
        try:
            dh = creator.create()
            dh.createDataJsonFile()
            publicId = saveLog(
                {
                    'name'    : name,
                    'folder'  : UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': 'json'
                }
            )
            fileSend = send_from_directory(path, name, as_attachment=True)
            updateDelete(publicId, True)
            return fileSend
        except Exception:
            return {
                "url": url,
                "success" : False,
                "error"   : "bad url"
            }, 400

    def _csv(self, url:str):
        name    = giveFileNameUnique('csv')
        creator = getCreatorDocumentHandler(
                url,
                'html',
                os.path.join(path, name),
                isUrl=True
        )
        try:
            dh = creator.create()
            dh.createDataCsvFile()
            publicId = saveLog(
                {
                    'name'    : name,
                    'folder'  : UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': 'csv'
                }
            )
            fileSend = send_from_directory(path, name, as_attachment=True)
            updateDelete(publicId, True)
            return fileSend
        except Exception:
            return {
                "url": url,
                "success" : False,
                "error"   : "bad url"
            }, 400

    def _encode(self,url:str, anonymizationFunction):
        name  = giveFileNameUnique('html')
        creator = getCreatorDocumentHandler(
            url,
            'html',
            os.path.join(path, name),
            anonymizationFunction,
            isUrl=True
        )
        try:
            dh = creator.create()
            dh.documentsProcessing()
            publicId = saveLog(
                {
                    'name'    : name,
                    'folder'  : UPLOAD_FOLDER,
                    'isdelete': False,
                    'filetype': 'html'
                }
            )
            fileSend = send_from_directory(path, name, as_attachment=True)
            updateDelete(publicId, True)
            return fileSend
        except Exception:
            return {
                "url": url,
                "success" : False,
                "error"   : "bad url"
            }, 400

    def get(self):
        url  = str(request.args['url']) 
        op   = str(request.args['op'])
        print(url,op)
        if op == 'csv':
            return self._csv(url)
        elif op == 'json':
            return self._json(url)
        elif op == 'encode':
            return self._encode(url, encode)
        elif op == 'target':
            return self._encode(url, markInHtml)
        return {
                "op"      : url,
                "success" : False,
                "error"   : "bad operation"
            }, 400
        
