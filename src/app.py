#-*- coding: utf-8 -*-

from flask import Flask
from flask.ext.environments import Environments
from flask.ext.mongokit import MongoKit
from flask.ext.restful import Resource, Api
from models import AccessToken, Object, User
import resources
from weibo import Client


app = Flask(__name__)
env = Environments(app)

env.from_object('config-devel')
#print app.config

weiboClient = Client(app.config['WEIBO_API_KEY'],
					 app.config['WEIBO_API_SECRET'],
					 app.config['WEIBO_API_REDIRECT_URI'])

db = MongoKit(app)
db.register([AccessToken, Object, User])

api = Api(app)
api.add_resource(resources.Photo, '/photos/<string:id>')
