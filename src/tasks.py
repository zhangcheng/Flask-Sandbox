#-*- coding: utf-8 -*-

from celery import Celery

celery = Celery('tasks', broker='mongodb://localhost/')

celery.conf.update(
	CELERY_RESULT_BACKEND = "mongodb",
	CELERY_MONGODB_BACKEND_SETTINGS = {
	    "database": "flask",
	    "taskmeta_collection": "my_taskmeta_collection",
	}
)

@celery.task
def add(x, y):
    return x + y
