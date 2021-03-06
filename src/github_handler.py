#Encoding=UTF8

import tornado.web
import mongo_helper
import json
import logger
import os
import datetime
import utils
import config
import threading
from queue import Queue

ROOT = '/tmp'

class GitHubHandler(tornado.web.RequestHandler):      
    def post(self):
        body = json.loads(self.request.body.decode())
        logger.debug(body)
        repo = body['repository']['name']
        url = body['repository']['clone_url']
        user = body['repository']['owner']['name']
        date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        path = ROOT + '/' + repo + date
        tag = mongo_helper.get_image_version(user, repo)
        
        context = {'path': path, 'url': url, 'repo': repo, 'user': user, 'tag': (tag + 1)}
        t = threading.Thread(target=start_build, args=(context,))
        t.start()

def start_build(context):
    path = context['path']
    url = context['url']
    repo = context['repo']
    user = context['user']
    tag = context['tag']
    str_tag = '.'.join(str(tag))
    
    cmd = 'mkdir ' + path + ' && ' + \
        'cd ' + path + ' && ' + \
        'git clone ' + url + ' && ' + \
        'cd ' + repo + ' && ' + \
        'sudo docker build -t vophoto-test.chinacloudapp.cn:5000/' + user + "/" + repo + ":" + str_tag + " ." + ' && ' + \
        'sudo docker push vophoto-test.chinacloudapp.cn:5000/' + user + "/" + repo + ":" + str_tag + ' && ' + \
        'sudo rm -fr ' + path
    
    utils.run_command(config.config['config_server'], cmd)
#     utils.run_command(config.config['config_server'], 'cd ' + path + " && " + 'git clone ' + url)
#     utils.run_command(config.config['config_server'], 'cd ' + path + "/" + repo + " && " \
#                       + 'sudo docker build -t vophoto-test.chinacloudapp.cn:5000/' + user + "/" + repo + ":" + str_tag + " .")
#     utils.run_command(config.config['config_server'], 'sudo docker push vophoto-test.chinacloudapp.cn:5000/' + user + "/" + repo + ":" + str_tag)
#     utils.run_command(config.config['config_server'], 'sudo rm -fr ' + path)
    
    image = {'user': user, 'name': repo, 'version': tag}
    mongo_helper.save_my_images(image)

if __name__ == "__main__":
    context = {'path': 'path', 'url': 'url', 'repo': 'repo', 'user': 'user', 'tag': '100'}
    path = context['path']
    url = context['url']
    repo = context['repo']
    user = context['user']
    tag = context['tag']
    str_tag = '.'.join(str(tag))
    
    cmd = 'mkdir ' + path + ' && ' + \
        'cd ' + path + ' && ' + \
        'git clone ' + url + ' && ' + \
        'cd ' + repo + ' && ' + \
        'sudo docker build -t vophoto-test.chinacloudapp.cn:5000/' + user + "/" + repo + ":" + str_tag + " ." + ' && ' + \
        'sudo docker push vophoto-test.chinacloudapp.cn:5000/' + user + "/" + repo + ":" + str_tag + ' && ' + \
        'sudo rm -fr ' + path
        
    print(cmd)