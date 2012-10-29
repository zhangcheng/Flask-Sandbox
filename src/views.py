import json

from flask import request, redirect, url_for, render_template, session, make_response
from app import app, weiboClient


@app.route('/login')
def login():
    print request.args
    code = request.args.get('code') or None
    resp = None
    if code:
#        import ipdb; ipdb.set_trace()
        try:
            weiboClient.set_code(code)
        except Exception, e:
            print e
            resp = make_response('', 501)
        else:
            print weiboClient.token_info
            resp = make_response(json.dumps(weiboClient.token_info), 200)
        finally:
            pass
    return resp
