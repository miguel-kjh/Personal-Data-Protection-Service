from flask_restplus import Namespace

class NameSearchDto:
    api = Namespace('NameSearch', description='name search in documents')