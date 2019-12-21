import uuid

from app.main import db
from app.main.model.fileLog import FileLog
from flask_sqlalchemy import SQLAlchemy

def saveLog(data: dict):
    log = FileLog(
        public_id=str(uuid.uuid4()),
        name=data['name'],
        folder=data['folder'],
        isDelete=data['isdelete'],
        filetype=data['filetype']
    )
    commit(log)
    response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
    return response_object, 201

def getAllLog():
    return FileLog.query.all()

def getFileToDelete():
    return FileLog.query.filter_by(isDelete=True)

def updateDelete(public_id:str,boolean:bool):
    log = FileLog.query.filter_by(public_id=public_id).first()
    log.isDelete = boolean
    db.session.commit()

def commit(log):
    db.session.add(log)
    db.session.commit()