#Encoding=UTF8

import tornado.web
import mongo_helper
import json
import logger
import utils

class VMHandler(tornado.web.RequestHandler):
    def get(self):
        vms = utils.list_vm()
        output = [k for k in vms if k['OSDisk']['operatingSystem'] == 'Linux']
        self.write(json.dumps(output))
        
    def put(self):
        pass
        
    def delete(self):
        pass
