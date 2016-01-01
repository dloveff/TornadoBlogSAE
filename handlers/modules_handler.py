# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import configurations as conf

class HeadModule(tornado.web.UIModule):
    def render(self, settings):
        return self.render_string('modules/head.html', blog_settings=settings)

class HeaderModule(tornado.web.UIModule):
    def render(self, settings):
        return self.render_string('modules/header.html', blog_settings=settings)

class FooterModule(tornado.web.UIModule):
    def render(self, settings):
        return self.render_string('modules/footer.html', blog_settings=settings)

class DuoshuoModule(tornado.web.UIModule): # url留空则为首页，否则url参数为文章链接如'/post/4'
    def render(self, post=None):
        domain = conf.deploy_settings['domain']
        if post:
            cid = str(post.cid)
            url = domain+'/post/'+cid
            return self.render_string('modules/duoshuo.html',url=url,post=post)
        else:
            url = domain+'/'
            return self.render_string('modules/duoshuo.html',url=url,post=None)


class PostModule(tornado.web.UIModule):
    def render(self, post, md, duoshuo=False, link=True, isindex=False):
        return self.render_string('modules/post.html',post=post,md=md,duoshuo=duoshuo,link=link)

class RecentPostMenuModule(tornado.web.UIModule):
    def render(self, post):
        return self.render_string('modules/post_menu.html',post=post)

class PostListModule(tornado.web.UIModule):
    def render(self, post):
        return self.render_string('modules/post_list.html',post=post)
