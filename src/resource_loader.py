#-*- coding: utf-8 -*-

import resources
from flask.ext.restful import Resource, Api

from app import app


api = Api(app)
api.add_resource(resources.Photos, '/<int:id>/photos')
api.add_resource(resources.UploadToken, '/system/upload_token')
