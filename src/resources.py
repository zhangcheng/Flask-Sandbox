#-*- coding: utf-8 -*-

import time

from flask import request
from flask.ext.restful import Resource
from vendor import uptoken


photos = {}

class Photos(Resource):
	def get(self, id):
		return {id: [1, 2, 3]}

	def put(self, id):
		photos[id] = request.form['data']
		return {id: photos[id]}


class UploadToken(Resource):
	def get(self):
		expire_in = 86400
		token = uptoken.UploadToken('upload', expire_in)
		return {'token': token.generate_token(), 'expire_in': expire_in}
