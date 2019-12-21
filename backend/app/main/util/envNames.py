UPLOAD_FOLDER = 'storageFiles'
VERSION = "1.0 beta"
ALLOWED_EXTENSIONS = set(['docx', 'pdf', 'xlsx', 'xlsm', 'xls', 'html'])

import os
path = os.path.join(os.getcwd(), UPLOAD_FOLDER)