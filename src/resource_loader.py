#-*- coding: utf-8 -*-

import resources
from flask.ext.restful import Resource, Api

from app import app


api = Api(app)

api.add_resource(resources.Object, '/<int:objectId>')
api.add_resource(resources.UploadToken, '/system/upload_token')

api.add_resource(resources.Photos, '/<int:objectId>/photos')
api.add_resource(resources.Services, '/<int:objectId>/services')
api.add_resource(resources.Users, '/users')
