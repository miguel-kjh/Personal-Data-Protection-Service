from flask_restplus import Api
from flask import Blueprint

from .main.controller.contoller import api as apiNS 
from .main.util.envNames import VERSION

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API',
          version=VERSION,
          description='Web service oriented to the location of names in documents'
          )

api.add_namespace(apiNS, path='/search')