#-*- coding: utf-8 -*-

import socket
import struct
import time

from flask.ext.script import Command, Manager

from app import app, db
from models import Object


class Hello(Command):
	def run(self):
		s = socket.socket()
		host = '10.18.121.202'
		port = 4444
		s.connect((host, port))

		while True:
			if db.Object.find({ 'type': { '$exists' : False } }).count() < 3:
				s.sendall('\x03')
				data = s.recv(1024)
				idList = list(struct.unpack('!QQQ', data))
				for id in idList:
					obj = db.Object()
					obj['_id'] = long(id)
					obj.save()
			time.sleep(10)


manager = Manager(app)
manager.add_command("hello", Hello())
manager.run()
