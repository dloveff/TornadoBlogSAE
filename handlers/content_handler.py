# -*- coding: utf-8 -*-

import markdown as md
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import configurations as conf
from utils import db

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("login_name")

def current_cookie_user(self):
    try:
        cookie_user = self.current_user
        return db.get_user(login_name=cookie_user).screen_name
    except:
        return None

class IndexHandler(BaseHandler):
    def get(self):
        pst = db.get_page()
        self.render(
            'index.html',
            page = 1,
            posts = pst,
            md = md.markdown,
            blog_settings = conf.blog_settings,
        )

class PageHandler(BaseHandler):
    def get(self, page):
        pst = db.get_page(int(page))
        if pst == []:
            self.render('404.html')
        if int(page) <= 0:
            self.render('404.html')
        for p in pst:
            p.text = md.markdown(p.text)
        self.render(
            'index.html',
            posts = pst,
            md = md.markdown,
            page = int(page),
            blog_settings = conf.blog_settings,
        )

class ArchivesHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render(
            'archives.html',
            # post = db.get_posts(),
            user = current_cookie_user(self),
            blog_settings = conf.blog_settings,
        )

class PostHandler(BaseHandler):
    def get(self, cid):
        self.render(
            'post.html',
            post = db.get_post(cid),
            md = md.markdown,
            blog_settings = conf.blog_settings,
        )

class AboutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render(
            'about.html',
            blog_settings = conf.blog_settings,
        )

class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render(
            'login.html',
            user = current_cookie_user(self),
            blog_settings = conf.blog_settings,
        )

    def post(self, *args, **kwargs):
        account = self.get_argument('account')
        password = self.get_argument('password')
        login_info = db.login(account=account, password=password)
        if not isinstance(login_info,str):
            self.set_secure_cookie("login_name", login_info.login_name)
            self.redirect('/admin')
        else:
            self.redirect("/login")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("login_name")
        self.redirect('/')

class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if current_cookie_user(self):
            self.render(
                'list.html',
                posts = db.get_posts(30),
                user = current_cookie_user(self),
                admin_screen_name = db.get_user(login_name='admin').screen_name,
                blog_settings = conf.blog_settings,
            )
        else:
            self.redirect('/login')

class EditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, cid):
        if current_cookie_user(self):
            self.render(
                'edit.html',
                post = db.get_post(cid),
                blog_settings = conf.blog_settings,
            )
        else:
            self.redirect('/login')

    @tornado.web.authenticated
    def post(self, cid):
        if current_cookie_user(self):
            db.update_post(
                cid = cid,
                title = self.get_argument('post_title'),
                text = self.get_argument('post_text'),
            )
            self.redirect('/post/'+str(cid))
        else:
            print('fail')
            self.redirect('/edit/'+str(cid))

class NewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if current_cookie_user(self):
            self.render(
                'new.html',
                blog_settings = conf.blog_settings,
            )
        else:
            self.redirect('/login')

    @tornado.web.authenticated
    def post(self):
        if current_cookie_user(self):
            db.new_post(
                title = self.get_argument('post_title'),
                text = self.get_argument('post_text'),
            )
            self.redirect('/admin')
        else:
            self.redirect('/new')

class DeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, cid):
        if current_cookie_user(self):
            db.delete_post(cid)
            self.redirect('/admin')
        else:
            self.redirect('/login')

class InitHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if current_cookie_user(self):
            user = current_cookie_user(self)
            admin_screen_name = db.get_user(login_name='admin').screen_name
            if user == admin_screen_name:
                db.init(force=True)
            self.redirect('/')
        else:
            self.redirect('/admin')
