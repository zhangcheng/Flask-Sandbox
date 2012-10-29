from flask import Flask
from flask_environments import Environments
from weibo import Client


app = Flask(__name__)
env = Environments(app)

env.from_object('config-devel')
print app.config

weiboClient = Client(app.config['WEIBO_API_KEY'],
					 app.config['WEIBO_API_SECRET'],
					 app.config['WEIBO_API_REDIRECT_URI'])
