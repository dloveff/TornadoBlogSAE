# -*- coding: utf-8 -*-
from peewee import *
import configurations as conf
import re
from datetime import datetime

# mysql_db = MySQLDatabase('test',host='localhost',port=3306,user='root',password='weaming')
mysql_db = MySQLDatabase(conf.deploy_settings['db_name'],host=conf.deploy_settings['db_host'],port=conf.deploy_settings['db_port'],user=conf.deploy_settings['db_user'],password=conf.deploy_settings['db_passwd'])

class BaseModel(Model):
    class Meta:
        database = mysql_db

class User(BaseModel):
    uid = PrimaryKeyField()
    login_name = CharField(unique=True) # 必填
    screen_name = CharField(default=login_name)
    email = CharField(unique=True) # 必填
    password = CharField() # 必填
    birth = DateField(null=True)
    url = CharField(default=uid)
    created = DateTimeField(default=datetime.now())
    logged = DateField(null=True)
    activated = BooleanField(default=True)


class Content(BaseModel):
    cid = PrimaryKeyField()
    uid = ForeignKeyField(User,related_name='uid_id',default=1) # 非空
    title = CharField(default='Custom title')
    text = TextField() # 非空
    archive = CharField(default='default')
    created = DateTimeField(default=datetime.now())
    modified = DateTimeField(default=datetime.now())
    status = CharField(default='post')
    password = CharField(null=True)
    allow_comment = BooleanField(default=True)
    allow_feed = BooleanField(default=True)

class Settings(BaseModel):
    sid = PrimaryKeyField()
    title = CharField(default=conf.blog_settings['title'])
    logo = CharField(default=conf.blog_settings['logo'])

def db_link(func):
    def wrapper(*args, **kw):
        mysql_db.connect()
        # mysql_db.get_conn()
        rt = func(*args, **kw)
        mysql_db.close()
        return rt
    return wrapper

###########
# 封装方法 #
###########
@db_link
def get_post(cid):# 参数为cid
    try:
        content = Content.get(Content.cid == cid)
        return content
    except DoesNotExist as e:
        print 'Post not exist'

@db_link
def get_posts(num=20):# 参数为要获取的文章数
    try:
        contents = Content.select(Content,User).join(User).where(Content.uid == User.uid).order_by(Content.cid.desc()).limit(num)
        return contents
    except:
        print 'Get post list fail'

@db_link
def get_page(page=1):# 参数为要获取的页数
    try:
        contents = Content.select(Content,User).join(User).where(Content.uid == User.uid).order_by(Content.cid.desc()).paginate(page, conf.ppp)
        return contents
    except:
        print 'Get post list fail'

@db_link
def new_post(**kw):# 参数为新文章的数据库的键值对,uid,title,text
    try:
        content = Content.insert(**kw).execute()
        print 'New post success'
        return content
    except:
        print 'New post fail'

@db_link
def update_post(**kw):# 参数为新文章的数据库的键值对以及要更新的文章cid
    try:
        content = Content.update(title=kw['title'],text=kw['text'],modified=datetime.now()).where(Content.cid == kw['cid'])
        updated_num = content.execute()
        return updated_num
    except:
        print('更新文章失败！')

@db_link
def delete_post(cid):# 参数为新文章的数据库的键值对以及要更新的文章cid
    try:
        content = Content.delete().where(Content.cid==cid)
        updated_num = content.execute()
        return updated_num
    except:
        print('更新文章失败！')

@db_link
def get_user(uid=None,login_name=None): #
    try:
        if uid:
            user = User.get(User.uid == uid)
            return user
        elif login_name:
            user = User.get(User.login_name == login_name)
            return user
    except:
        print 'Get user fail'

@db_link
def create_user(**kw):
    try:
        new_user = User.insert(**kw).execute()
        print 'New user success'
        return new_user
    except:
        print 'New user fail'


def init(force=False):
    def create():
        mysql_db.create_tables([User,Content,Settings])
        create_user(login_name='admin',screen_name='管理员',email='iweaming@gmail.com',password='weaming',url='admin')
        create_user(login_name='visitor',screen_name='访客',email='123@guest',password='123456')
        Settings.create().save()
        new_post(title='First Post',text='Hello world',uid=1)

    if not (User.table_exists() and Content.table_exists() and Settings.table_exists()):
        try:
            create()
            print 'init success'
        except:
            print 'init db fail'
    else:
        print '已经初始化过了!'
        if force:
            try:
                mysql_db.drop_tables([User,Content,Settings])
                print '已经清空数据库'
                create()
                print '在已清空数据库上初始化完成'
            except:
                print 'BAD ERROR'

@db_link
def login(account='',password=''):
    # print 'account:'+account+'   password:'+password
    pattern = re.compile('\w+?@\w+?\.\w+',re.I)
    email = re.search(pattern,account)
    now_s = str(datetime.now())[0:19]
    if email:
        print 'account:'+account+'tring email login'
        try:
            user = User.select().where(User.email == account).get()
            if user.password == password:
                return(user)
        except:
            return('User not exist')
    else:
        print 'User: '+account+' use login_name '
        try:
            user = User.select().where(User.login_name == account).get()
            if user.password == password:
                return(user)
        except:
            return('User not exist')

# For test
if __name__=='__main__':
    # init()
    pass
