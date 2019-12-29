from app.main.util.envNames import ALLOWED_EXTENSIONS
from datetime import datetime

def allowedFile(filename:str) -> bool:
	return giveTypeOfFile(filename) in ALLOWED_EXTENSIONS

def giveTypeOfFile(filename:str) -> str:
    return '.' in filename and filename.rsplit('.', 1)[1].lower()

def giveFileNameUnique(filename:str, fileType:str) -> str:
    #filename = filename + str(datetime.now().timestamp())
    #sha = hashlib.sha256(filename.encode())
    #return sha.hexdigest() + "." + fileType
    return str(datetime.now().timestamp()).replace(".","") + "." + fileType