from flask import Request
from werkzeug.utils import secure_filename
from app.main.util.fileUtils import giveFileNameUnique, giveTypeOfFile, allowedFile
from app.main.util.envNames import ALLOWED_EXTENSIONS,UPLOAD_FOLDER
from app.main.service.personalDataSearch import PersonalData

import os


class RequestEvaluator:
    def __init__(self, request:Request):
        self.request      = request
        self.filename     = None
        self.fakeFilename = None
        self.success      = False
        self.error        = None
        self.filetype     = ""
        self.personalData = None
    
    def isRequestSuccesfull(self) -> bool:
        typeData = str(self.request.args['personalData'])
        if typeData == "names":
            self.personalData = PersonalData.name
        elif typeData == "idCards":
            self.personalData = PersonalData.idCards
        elif typeData == "all":
            self.personalData = PersonalData.all
        else:
            self.error = "type of personal data incorrect"
            self.success = False
            return self.success
        
        if 'file' not in self.request.files:
            self.error = "No file part"
            return self.success
        file = self.request.files['file']

        if file.filename == '':
            self.error = "No file selected for uploading"
            return self.success

        self.filename = secure_filename(file.filename)
        if not (file and allowedFile(file.filename)):
            self.error = "Allowed file types are %s" % (','.join(ALLOWED_EXTENSIONS))
            return self.success
        
        self.filetype = giveTypeOfFile(file.filename)
        self.fakeFilename = giveFileNameUnique(self.filetype)
        file.save(os.path.join(UPLOAD_FOLDER, self.fakeFilename))
        self.success = True

        return self.success

    def giveResponse(self) -> dict:
        return {
            "filename" : self.filename,
            "success"  : self.success,
            "error"    : self.error
        }