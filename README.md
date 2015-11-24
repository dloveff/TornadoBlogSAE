我的第一个Tornado博客
==
2015.11.24

增加分页

start @2015.09.11

成功部署到SAE
--
2015.10.15

围观地址：http://gitmind.sinaapp.com  
SAE代码（python2.7）地址：https://github.com/weaming/TornadoBlogSAE  
本地开发代码（python3.4）地址：https://github.com/weaming/TornadoBlog  

SAE部署过程记录
==
Mysql数据库配置：http://www.lovehxy.com/5

SAE文档参考：http://www.sinacloud.com/doc/sae/python/tutorial.html#tornado

config.yaml
```
name: pylabs
version: 1

worker: tornado
```
index.wsgi
```
import tornado.web
from tornado.httpclient import AsyncHTTPClient

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://wiki.westeros.org", callback=self._callback)
        self.write("Hello to the Tornado world! ")
        self.flush()

    def _callback(self, response):
        self.write(response.body)
        self.finish()

settings = {
    "debug": True,
}

# application should be an instance of `tornado.web.Application`,
# and don't wrap it with `sae.create_wsgi_app`
application = tornado.web.Application([
    (r"/", MainHandler),
], **settings)
```

2015.10.14

放弃了markdown编辑，先实现简单的编辑功能。
