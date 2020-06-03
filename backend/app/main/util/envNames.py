UPLOAD_FOLDER      = 'storageFiles'
VERSION            = "1.0"
ALLOWED_EXTENSIONS = ['docx', 'pdf', 'xlsx', 'xlsm', 'xls', 'html', 'txt','csv']

import os

path = os.path.join(os.getcwd(), UPLOAD_FOLDER)
