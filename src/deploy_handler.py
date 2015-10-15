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
            arch = {
                  "id": "5aa12bcd-f905-6a32-91fe-4c5bd9440839",
                  "title": "MyDockerCluster1",
                  "containerCount": 6,
                  "containers": [
                    {
                      "id": "23742bbf-0b6c-7c71-61b2-c8b8a9f0dc58",
                      "tags": [ ],
                      "imageType": "vophoto-test.chinacloudapp.cn:5000/mongo:latest",
                      "serviceName": "catalog_mongo",
                      "portMap": [":27017"],
                      "name":"catalog_mongo",
                      "args": "-v /mnt/catalog:/data/db",
                      "node":["vophoto-demo-db"],
                      "x": 113,
                      "y": 204
                    },
                    {
                      "id": "33742bbf-0b6c-7c71-61b2-c8b8a9f0dc58",
                      "tags": [ ],
                      "imageType": "vophoto-test.chinacloudapp.cn:5000/mongo:latest",
                      "serviceName": "inventory_mongo",
                      "portMap": [":27017"],
                      "name":"inventory_mongo",
                      "args": "-v /mnt/inventory:/data/db",
                      "node":["vophoto-demo-db"],
                      "x": 113,
                      "y": 204
                    },
                    {
                      "id": "02f0063c-1697-0099-1df5-dd70ce5d56e1",
                      "tags": [ ],
                      "imageType": "vophoto-test.chinacloudapp.cn:5000/wangtt03/catalog:1.0.0",
                      "serviceName": "catalog",
                      "name": "catalog",
                      "args": "",
                      "portMap": [ ":8801" ],
                      "node":[],
                      "x": 178,
                      "y": 474
                    },
                    {
                      "id": "bf68af36-41dc-a4bc-42e6-d026e6bb7f9d",
                      "tags": [ ],
                      "imageType": "vophoto-test.chinacloudapp.cn:5000/wangtt03/inventory:1.0.8",
                      "serviceName": "inventory",
                      "name": "inventory",
                      "args": "",
                      "portMap": [ ":8802" ],
                      "node":[],
                      "x": 268,
                      "y": 310
                    },
                    {
                      "id": "1f68af36-41dc-a4bc-42e6-d026e6bb7f9d",
                      "tags": [ ],
                      "imageType": "vophoto-test.chinacloudapp.cn:5000/wangtt03/order:1.0.0",
                      "serviceName": "buy",
                      "args": "",
                      "name": "buy",
                      "portMap": [ ":8803" ],
                      "node":[],
                      "x": 268,
                      "y": 310
                    },
                    {
                      "id": "ec90427e-4739-42c9-bbf6-1a1399e0656c",
                      "tags": [ ],
                      "imageType": "vophoto-test.chinacloudapp.cn:5000/wangtt03/petstore:1.0.0",
                      "serviceName": "petstore",
                      "args": "",
                      "name": "petstore",
                      "portMap": [ ":8080" ],
                      "node":[],
                      "x": 224,
                      "y": 420
                    }
                  ],
                  "linkCount": 1,
                  "links": [
                    {
                      "from": "02f0063c-1697-0099-1df5-dd70ce5d56e1",
                      "to": "23742bbf-0b6c-7c71-61b2-c8b8a9f0dc58"
                    }
                  ]
            }

            # pull images
            nodes = arch['containers']
            for node in nodes:
                logger.debug('pulling image: ' + node['imageType'])
                utils.run_command(config.config['demo_server'], 'sudo docker -H tcp://0.0.0.0:2376 pull ' + node['imageType'])
                
            #stop running containers
            running = utils.list_cluster_containers()
            for cont in nodes:
                image_name = cont['imageType'][0:cont['imageType'].rfind(':')]
                version = cont['imageType'][cont['imageType'].rfind(':') + 1:]
                need_restart = True
                for n in running:
                    name = n['Image'][0:n['Image'].rfind(':')]
                    ver = n['Image'][n['Image'].rfind(':') + 1:]
                    if image_name == name and version == ver:
                        need_restart = False
                        break
                    elif image_name == name and version != ver:
                        utils.stop_container(config.config['demo_server'], n['Id'])
                
                if need_restart:
                    args = '-d'
                    if cont['name'] != '':
                        args = args + ' --name ' + cont['name']
                    if len(cont['portMap']) > 0:
                        args = args + ' ' + ' '.join(['-p %s' % n for n in cont['portMap']])
                    if cont['serviceName'] != '':
                        args = args + ' -e SERVICE_NAME=' + cont['serviceName']
                    if cont['args'] != '':
                        args = args + ' ' + cont['args']
                    if len(cont['node']) > 0:
                        args = args + ' ' + ' '.join(['-e constraint:node==%s' % n for n in cont['node']])
                    utils.start_container(config.config['demo_server'], cont['imageType'], args)
                
            self.write(json.dumps(info))
