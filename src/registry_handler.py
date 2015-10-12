#Encoding=UTF8

import tornado.web
import mongo_helper
import json
import logger

class RegistryHandler(tornado.web.RequestHandler):
    def get(self):
        images = mongo_helper.get_images()
        self.write(json.dumps(images))
        
    def put(self):
        name = self.get_argument('name', '')
        if not name:
            return
        
        image = {'name': name}
        mongo_helper.save_images(image)
        
    def delete(self):
        name = self.get_argument('name', '')
        if not name:
            return
        
        mongo_helper.delete_images(name)
