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
            info = mongo_helper.get_project_info(project_id)
            self.write(json.dumps(info))
        
    def put(self):
        pname = self.get_argument('name', '')
        if not pname:
            return
        arch = self.get_argument('arch', '')
        proj = {"name": pname, "arch": arch}
        mongo_helper.save_project(proj)
            
    def post(self):
        project_id = self.get_argument('project_id', '')
        if not project_id:
            return
        pname = self.get_argument('name', '')
        arch = self.get_argument('arch', '')
        proj = {"name": pname, "arch": arch}
        mongo_helper.update_project(proj)

    def delete(self):
        project_id = self.get_argument('project_id', '')
        if not project_id:
            return
        mongo_helper.delete_project(project_id)