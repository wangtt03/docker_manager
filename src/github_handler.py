#Encoding=UTF8

import tornado.web
import mongo_helper
import json
import logger
import os
import datetime
from subprocess import call
import utils

ROOT = '/tmp'

class GitHubHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('test')
        
    def post(self):
        body = json.loads(self.request.body.decode())
        repo = body['repository']['name']
        url = body['repository']['git_url']
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        path = ROOT + '/' + repo + date
        print(utils.run_command('vophoto-test.chinacloudapp.cn', 'mkdir ' + path))
        print(utils.run_command('vophoto-test.chinacloudapp.cn', 'cd ' + path + " && " + 'git clone ' + url))
        print(utils.run_command('vophoto-test.chinacloudapp.cn', 'cd ' + path + "/" + repo + " && " + 'sudo docker build -t ' + repo + " ."))
        
#         call(['mkdir ' + path])
#         call(['cd ' + path + " && " + 'git clone ' + url])
#         call(['cd ' + path + "/" + repo + " && " + 'sudo docker build -t ' + repo + " ."])

if __name__ == "__main__":
    print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))