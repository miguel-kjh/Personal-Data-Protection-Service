from flask import Flask

app = Flask(__name__)

UPLOAD_FOLDER = 'files_to_processing'
version = "alpha 1.0"
ALLOWED_EXTENSIONS = set(['docx', 'pdf', 'xlsx', 'xlsm', 'xls', 'html'])

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB