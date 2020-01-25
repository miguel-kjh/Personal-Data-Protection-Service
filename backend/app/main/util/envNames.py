UPLOAD_FOLDER = 'storageFiles'
VERSION = "1.2 beta"
ALLOWED_EXTENSIONS = ['docx', 'pdf', 'doc','xlsx', 'xlsm', 'xls', 'html']

import os
path = os.path.join(os.getcwd(), UPLOAD_FOLDER)