# -*- coding: utf-8 -*-

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from handlers import modules_handler
from handlers import content_handler

SETTINGS = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret = b'QPhy1d30S9yC47omLeLYqPMXcxJUhUIqqOq/EWwXpx4=',
    # xsrf_cookies = True,
    login_url = '/login',
    ui_modules = {
        'head_module': modules_handler.HeadModule,
        'header_module': modules_handler.HeaderModule,
        'footer_module': modules_handler.FooterModule,
        'duoshuo_module': modules_handler.DuoshuoModule,
        'post_module': modules_handler.PostModule,
        'recent_post_module': modules_handler.RecentPostMenuModule,
        'post_list_module': modules_handler.PostListModule,
    },
    debug = True,
)

application = tornado.web.Application(
    handlers = [
        (r'/', content_handler.IndexHandler),
        (r'/page/(\d+)', content_handler.PageHandler),
        (r'/archives/?.*', content_handler.ArchivesHandler),
        (r'/post/(\d+)', content_handler.PostHandler),
        (r'/admin', content_handler.AdminHandler),
        (r'/edit/(\d+)', content_handler.EditHandler),
        (r'/about', content_handler.AboutHandler),
        (r'/login', content_handler.LoginHandler),
        (r'/logout', content_handler.LogoutHandler),
        (r'/new', content_handler.NewHandler),
        (r'/delete/(\d+)', content_handler.DeleteHandler),
        (r'/init', content_handler.InitHandler),
    ],
    **SETTINGS
)
