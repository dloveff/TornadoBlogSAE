__author__ = 'garden'

import tornado.web
from tornado.httpclient import AsyncHTTPClient
from application import application as app
from utils import db

db.init()

application = app