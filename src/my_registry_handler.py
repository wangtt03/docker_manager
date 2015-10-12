#Encoding=UTF8

import tornado.web
import mongo_helper
import json
import logger

class MyRegistryHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.get_argument('user', 'contoso')
        images = mongo_helper.get_my_images(user)
        self.write(json.dumps(images))
        
    def put(self):
        user = self.get_argument('user', 'contoso')
        name = self.get_argument('name', '')
        if not name:
            return
        
        image = {'user': user, 'name': name}
        mongo_helper.save_my_images(image)
        
    def delete(self):
        user = self.get_argument('user', 'contoso')
        name = self.get_argument('name', '')
        if not name:
            return
        
        mongo_helper.delete_my_images(user, name)
