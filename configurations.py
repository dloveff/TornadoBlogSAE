# -*- coding: utf-8 -*-
__author__ = 'weaming'
import sae


ppp = 10

blog_settings = {
    'title':'阮家灯的博客',
    'logo':'img/logo.png',  # used function static_url() in HTML files
    'email':'iweaming@gmail.com',
    'login':False,
    'allow_register':False,
}

deploy_settings = {
    'domain':'gitmind.sinaapp.com',
    'db_name':sae.const.MYSQL_DB,
    'db_port':int(sae.const.MYSQL_PORT),
    'db_host':sae.const.MYSQL_HOST,
    'db_user':sae.const.MYSQL_USER,
    'db_passwd':sae.const.MYSQL_PASS,
}
