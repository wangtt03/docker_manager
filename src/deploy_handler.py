#Encoding=UTF8

import tornado.web
import mongo_helper
import json
import logger

class DeployHandler(tornado.web.RequestHandler):
    def post(self):
        project_id = self.get_argument('project_id', '')
        if not id:
            self.write('{status:false}')
        else:
            info = mongo_helper.get_project_info(int(project_id))
            self.write(json.dumps(info))
