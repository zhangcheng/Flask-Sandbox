#-*- coding: utf-8 -*-


from flask import request
from flask.ext.restful import Resource


photos = {}

class Photo(Resource):
	def get(self, id):
		return {id: photos[id]}

	def put(self, id):
		photos[id] = request.form['data']
		return {id: photos[id]}
