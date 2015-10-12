#Encoding=UTF8

import tornado.web
import mongo_helper
import json
import logger
import utils
import config

class DeployHandler(tornado.web.RequestHandler):
    def post(self):
        project_id = self.get_argument('project_id', '')
        if not id:
            self.write('{status:false}')
        else:
            info = mongo_helper.get_project_info(project_id)
            #arch = info['arch']
            arch = {"nodes":[{"image":"vophoto-test.chinacloudapp.cn:5000/mongo", 'name':'mymongodb', 'args':'--name mymongodb -d'}, \
                             {"image":"vophoto-test.chinacloudapp.cn:5000/petstore", 'name':'petstore', 'args':'--link mymongodb:mymongodb -d -p 80:80'}, \
                             ]}
            # pull images
            nodes = [n for n in arch['nodes']]
            for node in nodes:
                logger.debug('pulling image: ' + node['image'])
                utils.run_command(config.config['demo_server'], 'sudo docker -H tcp://0.0.0.0:2376 pull ' + node['image'])
                
            #stop running containers
            for node in nodes:
                utils.scale_out_container(config.config['demo_server'], node['image'], '', 0)
                
            # start containers
            for node in nodes:
                utils.scale_out_container(config.config['demo_server'], node['image'], node['args'], 1)
                
            self.write(json.dumps(info))
