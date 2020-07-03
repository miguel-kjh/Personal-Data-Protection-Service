from ..util.NameSearchDto                import NameSearchDto
from ..util.envNames                     import VERSION, UPLOAD_FOLDER, path
from ..service.LogService                import updateDelete, saveLog, getByPublicId
from ..service.languageBuilder           import LanguageBuilder
from ..service.CreateDocumentHandler     import getCreatorDocumentHandler
from ..util.RequestEvaluator             import RequestEvaluator
from ..util.fileUtils                    import giveFileNameUnique
from ..util.anonymizationFunctions       import encode,markInHtml,disintegration,dataObfuscation
from app.main.service.personalDataSearch import PersonalData



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

def registerOperation(evaluator: RequestEvaluator, function:classmethod, nameOperation:str, personalData: PersonalData):
    """ 
    Records the documents in the database and processes them.

    :param evaluator: The RequestEvaluator object with the information about the request
    :param function: the function to process the data
    :param nameOperation: String to indicate the name of the operation performed
    :param personalData: The type of data to search for
    :return: A dictionary with document id and document type
    """
    
    publicId = saveLog(
                {
                    'name'    : evaluator.fakeFilename,
                    'folder'  : path,
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
    dh.documentsProcessing(personalData)
    updateDelete(publicId, True)
    publicId = saveLog(
        {
            'name'    : nameOfNewDocument,
            'folder'  : path,
            'isdelete': False,
            'filetype': evaluator.filetype
        }
    )
    return {"id":publicId, "fileType":evaluator.filetype}

@api.route("/file/encode")
@api.param('personalData', 'type of personal data to be extracted from the document')
class Anonimization(Resource):

    @api.doc(
        'returns an id that indicates to the file sent with \
        the anonymized data in the database and the type of the file'
    )
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            return registerOperation(evaluator,encode, "anonymized",evaluator.personalData)
        else:
            return evaluator.giveResponse(), 400

@api.route("/file/disintegration")
@api.param('personalData', 'type of personal data to be extracted from the document')
class Disintegration(Resource):

    @api.doc(
        'returns an id that indicates to the file sent with \
        the disintegrated data in the database and the type of the file'
    )
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            return registerOperation(evaluator,disintegration,"disintegrated",evaluator.personalData)
        else:
            return evaluator.giveResponse(), 400

@api.route("/file/obfuscation")
@api.param('personalData', 'type of personal data to be extracted from the document')
class Obfuscation(Resource):

    @api.doc(
        'returns an id that indicates to the file sent with \
        the obfuscated data in the database and the type of the file'
    )
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            return registerOperation(evaluator,dataObfuscation,"obfuscated", evaluator.personalData)
        else:
            return evaluator.giveResponse(), 400


@api.route('/file/extract-data/json')
@api.param('personalData', 'type of personal data to be extracted from the document')
class extractDataJson(Resource):
    @api.doc('returns a json object with the requested data')
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            publicId = saveLog(
                {
                    'name'    : evaluator.fakeFilename,
                    'folder'  : path,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
            creator = getCreatorDocumentHandler(
                os.path.join(path, evaluator.fakeFilename),
                evaluator.filetype
            )
            dh = creator.create()
            names,idCards = dh.extractData(evaluator.personalData)
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
@api.param('personalData', 'type of personal data to be extracted from the document')
class extractDataJsonFile(Resource):

    @api.doc('returns a json file with the requested data')
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            publicId = saveLog(
                {
                    'name': evaluator.fakeFilename,
                    'folder': path,
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
            dh.createDataJsonFile(evaluator.personalData)
            updateDelete(publicId, True)
            publicId = saveLog(
                {
                    'name': nameOfNewDocument,
                    'folder': path,
                    'isdelete': False,
                    'filetype': 'json'
                }
            )
            return {"id":publicId, "fileType":'json'}
        else:
            return evaluator.giveResponse(), 400


@api.route('/file/extract-data/csv')
@api.param('personalData', 'type of personal data to be extracted from the document')
class extractDataCsv(Resource):

    @api.doc('returns a csv file with the requested data')
    def post(self):
        evaluator = RequestEvaluator(request)
        if evaluator.isRequestSuccesfull():
            publicId = saveLog(
                {
                    'name': evaluator.fakeFilename,
                    'folder': path,
                    'isdelete': False,
                    'filetype': evaluator.filetype
                }
            )
            nameOfNewDocument = evaluator.fakeFilename.replace('.' + evaluator.filetype, "_ext.csv")
            creator = getCreatorDocumentHandler(
                os.path.join(path, evaluator.fakeFilename),
                evaluator.filetype,
                os.path.join(path, nameOfNewDocument)
            )
            dh = creator.create()
            dh.createDataCsvFile(evaluator.personalData)
            updateDelete(publicId, True)
            publicId = saveLog(
                {
                    'name': nameOfNewDocument,
                    'folder': path,
                    'isdelete': False,
                    'filetype': 'csv'
                }
            )
            return {"id":publicId, "fileType":'csv'}
        else:
            return evaluator.giveResponse(), 400


@api.route('/file/download')
@api.param('id', 'public id for a document')
class getDocument(Resource):

    @api.doc('return a document using your public id')
    def get(self):
        publicId  = str(request.args['id'])
        docuemnt  = getByPublicId(publicId)
        if docuemnt:
            fileSend = send_from_directory(docuemnt.folder, docuemnt.name, as_attachment=True)
            updateDelete(publicId, True)
            return fileSend
        else:
            return {"error": "the documento with id %s does not exist" %(publicId)}, 400


@api.route('/file/operation-web')
@api.param('url', 'Url form a web site')
@api.param('op',  'Operation to a html file')
class operationWeb(Resource):

    def _json(self, url: str, personalData: PersonalData):
        name    = giveFileNameUnique('json')
        creator = getCreatorDocumentHandler(
                url,
                'html',
                os.path.join(path, name),
                isUrl=True
        )
        try:
            dh = creator.create()
            dh.createDataJsonFile(personalData)
            publicId = saveLog(
                {
                    'name'    : name,
                    'folder'  : path,
                    'isdelete': False,
                    'filetype': 'json'
                }
            )
            return {"id":publicId, "fileType":'json'}
        except Exception:
            return {
                "url": url,
                "success" : False,
                "error"   : "bad url"
            }, 400

    def _csv(self, url: str, personalData: PersonalData):
        name    = giveFileNameUnique('csv')
        creator = getCreatorDocumentHandler(
                url,
                'html',
                os.path.join(path, name),
                isUrl=True
        )
        try:
            dh = creator.create()
            dh.createDataCsvFile(personalData)
            publicId = saveLog(
                {
                    'name'    : name,
                    'folder'  : path,
                    'isdelete': False,
                    'filetype': 'csv'
                }
            )
            return {"id":publicId, "fileType":'csv'}
        except Exception:
            return {
                "url": url,
                "success" : False,
                "error"   : "bad url"
            }, 400

    def _encode(self,url:str, anonymizationFunction, personalData: PersonalData):
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
            dh.documentsProcessing(personalData)
            publicId = saveLog(
                {
                    'name'    : name,
                    'folder'  : path,
                    'isdelete': False,
                    'filetype': 'html'
                }
            )
            return {"id": publicId, "fileType": 'html'}
        except Exception:
            return {
                "url": url,
                "success" : False,
                "error"   : "bad url"
            }, 500

    
    @api.doc(
        'depending on the sent parameters it performs some of the \
        allowed operations of the service for a web page in html format'
    )
    def get(self):
        typeData = str(request.args['personalData'])
        if typeData == "names":
            personalData = PersonalData.names
        elif typeData == "idCards":
            personalData = PersonalData.idCards
        elif typeData == "all":
            personalData = PersonalData.all
        else:
            return {
                "success" : False,
                "error"   : "type of personal data incorrect"
            }, 400
        url  = str(request.args['url']) 
        op   = str(request.args['op'])
        if op == 'csv':
            return self._csv(url, personalData)
        elif op == 'json':
            return self._json(url, personalData)
        elif op == 'encode':
            return self._encode(url, encode, personalData)
        elif op == 'ofuscation':
            return self._encode(url, dataObfuscation, personalData)
        elif op == 'disgergation':
            return self._encode(url, disintegration, personalData)
        elif op == 'target':
            return self._encode(url, markInHtml, personalData)
        return {
                "op"      : url,
                "success" : False,
                "error"   : "bad operation"
            }, 400
        
