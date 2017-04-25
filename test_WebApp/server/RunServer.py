#-*- coding: utf-8 -*-
import os.path
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class PageHandler(tornado.web.RequestHandler):
    def get(self,input):
        self.render('pages/'+input)

def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/researcher', IndexHandler), (r'/pages/(.*?)', PageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print("Server start!")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()