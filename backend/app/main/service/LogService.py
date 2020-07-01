from app.main               import db
from app.main.model.fileLog import FileLog

import uuid

def saveLog(data: dict) -> str:
    """ 
    Adds a record of a new document to the database
    
    :param data: A dictionary with the data
    :return: publicId
    """

    publicId = str(uuid.uuid4())
    log = FileLog(
        publicId = publicId,
        name     = data['name'],
        folder   = data['folder'],
        isDelete = data['isdelete'],
        filetype = data['filetype']
    )
    commit(log)
    return publicId


def getAllLog():
    """
    Returns all records.
    :return: list of FileLog
    """

    return FileLog.query.all()


def getByPublicId(id: str):
    """  
    Returns a particular register.
    :param id: public id in string
    :return: FileLog
    """

    return FileLog.query.filter_by(publicId=id).first()


def getFileToDelete():
    """ 
    Gets all the files that are candidates for deletion.
    :return: list of FileLog
    """

    return FileLog.query.filter_by(isDelete=True).all()


def updateDelete(publicId: str, isDelete: bool):
    """  
    Update a record and mark it as a candidate for deletion
    :param publicId: public id
    :param isDelete: boolean
    """

    log = FileLog.query.filter_by(publicId=publicId).first()
    log.isDelete = isDelete
    db.session.commit()


def commit(log):
    db.session.add(log)
    db.session.commit()
