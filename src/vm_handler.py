#Encoding=UTF8

import tornado.web
import mongo_helper
import json
import logger
import utils

class VMHandler(tornado.web.RequestHandler):
    def get(self):
        clusters = mongo_helper.get_clusters()
        self.write(json.dumps(clusters))
        
    def put(self):
        pname = self.get_argument('name', '')
        if not pname:
            return
        proj = {"name": pname}
        mongo_helper.add_cluster(proj)
        
    def delete(self):
        pname = self.get_argument('name', '')
        if not pname:
            return
        mongo_helper.delete_cluster(pname)
