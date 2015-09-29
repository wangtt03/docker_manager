#Encoding=UTF8

import tornado.web
import mongo_helper
import json
import logger

class RegistryHandler(tornado.web.RequestHandler):
    def get(self):
        images = mongo_helper.get_images()
        self.write(json.dumps(images))
        
    def post(self):
        self.write('test')
