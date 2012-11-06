#-*- coding: utf-8 -*-

import pytz

from datetime import datetime
from dateutil import parser
from flask import request
from flask.ext.restful import abort, fields, marshal, marshal_with, reqparse, Resource

from app import db
from vendor import uptoken


photoParser = reqparse.RequestParser()
photoParser.add_argument('key', type=unicode, location='form', required=True)
photoParser.add_argument('name', type=unicode, location='form')
photoParser.add_argument('created_at', type=unicode, location='form')

serviceParser = reqparse.RequestParser()
serviceParser.add_argument('name', type=unicode, location='form', required=True)
serviceParser.add_argument('id', type=unicode, location='form', required=True)
serviceParser.add_argument('access_token', type=unicode, location='form', required=True)

userParser = reqparse.RequestParser()
userParser.add_argument('type', type=int, location='form')
userParser.add_argument('device_id', type=unicode, location='form')


class Object(Resource):
	def get(self, objectId):
		obj = db.Reference.one({'_id': objectId})
		if obj:
			if obj.type == 1:
				return db.User.one({'_id': objectId})
			elif obj.type == 2:
				return marshal(db.Photo.one({'_id': objectId}), photo_fields)
		abort(404)

	def post(self, objectId):
		args = userParser.parse_args()
		if len(args) == 0: return None
		obj = db.Object.one({'_id': objectId})
		if obj and obj.type == "user":
			user = db.User.one({'_id': objectId})
			for key in args.keys():
				user[key] = args[key]
			user.save()
			return user
		return None

	def delete(self, objectId):
		obj = db.Reference.one({'_id': objectId})
		if obj:
			if obj.type == 1:
				thisObj = db.User.one({'_id': objectId})
				thisObj.delete()
			elif obj.type == 2:
				thisObj = db.Photo.one({'_id': objectId})
				thisObj.delete()
			obj.delete()
		return {}


class QiniuUrlField(fields.Raw):
    def format(self, value):
        return "http://upload.dn.qbox.me/%s" % value

class ISO8601DateTimeField(fields.Raw):
    def format(self, value):
    	fmt = '%Y-%m-%dT%H:%M:%S%z'
    	if value.tzinfo is not None:
    		return value.strftime(fmt)
    	else:
        	return pytz.utc.localize(value).strftime(fmt)

photo_fields = {
    'id': fields.String(attribute='_id'),
    'key': QiniuUrlField,
    'created_at': ISO8601DateTimeField,
}


class Photos(Resource):
	@marshal_with(photo_fields)
	def get(self, objectId):
		user = db.User.find_one({'user_id': objectId})
		if user:
			return list(db.Photo.find({'user_id': objectId}))
		return None

	@marshal_with(photo_fields)
	def post(self, objectId):
		args = photoParser.parse_args()
		args.pop('objectId')
		if args.has_key('created_at'):
			args['created_at'] = parser.parse(args['created_at']).astimezone(pytz.utc)
		print args
		user = db.User.find_one({'user_id': objectId})
		if not user:
			abort(404)
		obj = db.reference.find_and_modify({'type': 0}, {'$set': {'type': 2}})
		photo = db.Photo()
		photo._id = obj['_id']
		photo.user_id = long(objectId)
		for key in args.keys():
			photo[key] = args[key]
		photo.save()
		return photo


class Services(Resource):
	def get(self, objectId):
		return db.User.find_one({'_id': objectId}).services

	def post(self, objectId):
		args = serviceParser.parse_args()
		if len(args) == 0: return None
		user = db.User.find_one({'_id': objectId})
		if user:
			if user.services.has_key(args['name']):
				# assert third-party service uid remains same
				pass
			else:
				user.services[args['name']] = {}
			user.services[args['name']]['id'] = args['id']
			user.services[args['name']]['access_token'] = args['access_token']
			user.save()
			return {args['name'] : user.services[args['name']]}
		return None


class UploadToken(Resource):
	def get(self):
		expire_in = 86400
		token = uptoken.UploadToken('upload', expire_in)
		return {'token': token.generate_token(), 'expire_in': expire_in}


class Users(Resource):
	def get(self):
		return list(db.User.find())

	def post(self):
		args = userParser.parse_args()
		obj = db.object.find_and_modify({ 'type': { '$exists' : False } }, { '$set' : { 'type' : u'user' }})
		user = db.User()
		user._id = obj['_id']
		for key in args.keys():
			user[key] = args[key]
		user.save()
		return user
