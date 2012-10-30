#from flask import app

from flask.ext.script import Shell, Manager

from app import app, db

def shell_context():
    return dict(app=app, db=db)

manager = Manager(app)
manager.add_command("shell", Shell(make_context=shell_context))
manager.run()
