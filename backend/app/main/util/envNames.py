UPLOAD_FOLDER = 'storageFiles'
VERSION = "1.3 beta"
ALLOWED_EXTENSIONS = ['docx', 'pdf','xlsx', 'xlsm', 'xls', 'html', 'txt']

import os
path = os.path.join(os.getcwd(), UPLOAD_FOLDER)