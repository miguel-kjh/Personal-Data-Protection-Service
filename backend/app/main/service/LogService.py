import uuid
import os

from app.main import db
from app.main.model.fileLog import FileLog
from flask_sqlalchemy import SQLAlchemy

def saveLog(data: dict):
    publicId = str(uuid.uuid4())
    log = FileLog(
        publicId=publicId,
        name=data['name'],
        folder=data['folder'],
        isDelete=data['isdelete'],
        filetype=data['filetype']
    )
    commit(log)
    return publicId

def getAllLog():
    return FileLog.query.all()

def getByPublicId(id:str):
    return FileLog.query.filter_by(publicId=id).first()

def getFileToDelete():
    return FileLog.query.filter_by(isDelete=True).all()

def updateDelete(public_id:str,boolean:bool):
    log = FileLog.query.filter_by(publicId=public_id).first()
    log.isDelete = boolean
    db.session.commit()

def commit(log):
    db.session.add(log)
    db.session.commit()