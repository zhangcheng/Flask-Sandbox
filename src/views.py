#-*- coding: utf-8 -*-

import json

from datetime import datetime, timedelta
from flask import request, redirect, url_for, render_template, session, make_response
from flask.views import MethodView
from app import app, weiboClient, db
import models


@app.route('/login', methods=["POST"])
def login():
    print request.form
    resp = make_response('', 200)
    loginType = request.form.get('type') or None
    deviceId = request.form.get('device_id') or None
    if loginType == 'temp':
        user = db.User.one({'device_id': deviceId})
        if not user:
            user = db.User()
            user.device_id = deviceId
            user.save()

    elif loginType == 'weibo':
        code = request.form.get('code') or None
#        import ipdb; ipdb.set_trace()
        try:
            weiboClient.set_code(code)
        except Exception, e:
            print e
            resp = make_response('', 501)
        else:
            print weiboClient.token_info
#            resp = make_response(json.dumps(weiboClient.token_info), 200)
            user = db.User.one({ 'services.weibo.id' : '1' })
            if not user:
                user = db.User()
                user.services.weibo.id = '1'
                user.services.weibo.access_token = weiboClient.token_info['access_token']
                user.save()
            else:
                user.services.weibo.access_token = weiboClient.token_info['access_token']
                user.save()
        finally:
            pass

    if resp.status_code == 200:
        token = db.AccessToken.one({ 'user_id': user._id })
        now = datetime.utcnow()
        if not token:
            token = db.AccessToken()
            token.token = unicode(models.KeyGenerator(32)())
            token.user_id = user._id
            token.save()
        elif token.expire_at <= now:
            token.token = unicode(models.KeyGenerator(32)())
            token.issued_at = now
            token.expire_at = now + timedelta(seconds=3600)
            token.save()

        resp = make_response(token.to_json(), 200)

    return resp


@app.route('/token', methods=["GET", "POST"])
def token():
    if request.method == 'POST':
        token = db.AccessToken()
        token.token = unicode(models.KeyGenerator(32)())
        token.save()
        return make_response(token.to_json(), 200)
    return make_response('', 200)
