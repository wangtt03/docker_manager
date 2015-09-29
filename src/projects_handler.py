#Encoding=UTF8

import tornado.web
import mongo_helper
import json
import logger

class ProjectsHandler(tornado.web.RequestHandler):
    def get(self):
        project_id = self.get_argument('project_id', '')
        if not project_id:
            images = mongo_helper.get_projects()
            self.write(json.dumps(images))
        else:
            info = mongo_helper.get_project_info(int(project_id))
            self.write(json.dumps(info))
        
    def post(self):
        self.write('test')
