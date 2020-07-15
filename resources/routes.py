from .readword import UploadFile
from .personnels import Personnels, Personnel


def initialize_routes(api):
    api.add_resource(UploadFile, '/api/upload-file/')
    api.add_resource(Personnels, '/api/personnel/')
    api.add_resource(Personnel, '/api/personnel/<id>/')