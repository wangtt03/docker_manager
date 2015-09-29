#Encoding=UTF8

import tornado.web
import mongo_helper
import json
import logger

class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('status')
