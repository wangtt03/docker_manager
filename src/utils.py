#Encoding=UTF8

import paramiko
from paramiko import SSHClient
import os
import json
import config
import urllib.request
import httplib2

def run_command(server, cmd):
    if config.config['debug']:
        print(str(server) + ": " + cmd)
        return
    
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server[0], username=server[1], password=server[2])
    stdin, stdout, stderr = client.exec_command(cmd)
    lines = stdout.readlines()
    client.close()
    return ''.join(lines)
    
def list_vm():
    server = config.config['config_server']
    azure_account = config.config['azure_account']
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server[0], username=server[1], password=server[2])
    stdin, stdout, stderr = client.exec_command('sudo docker run --rm microsoft/azure-cli /bin/bash -c "azure login -u %s -p %s -e AzureChinaCloud && azure vm list --json"' % (azure_account[0], azure_account[1]))
    lines = stdout.readlines()
    lines = [line for line in lines if not line.startswith('info:')]
    client.close()
    return json.loads(''.join(lines))

def create_vm(server):
    pass

def list_nodes():
    pass

def inspect_container(server, name):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server[0], username=server[1], password=server[2])
    stdin, stdout, stderr = client.exec_command('sudo docker inspect %s' % name)
    lines = stdout.readlines()
    client.close()
    return ''.join(lines)
    
def get_container_status(server, name):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server[0], username=server[1], password=server[2])
    stdin, stdout, stderr = client.exec_command('sudo docker ps -af "name=%s" --format "{{.Status}}"' % name)
    lines = stdout.readlines()
    client.close()
    if len(lines) > 0:
        status = lines[0]
        if status.startswith('Up'):
            return 0
        elif status.startswith('Exit'):
            return 1
    
    return -1

def start_container(server, name, args):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server[0], username=server[1], password=server[2])
    stdin, stdout, stderr = client.exec_command('sudo docker -H tcp://0.0.0.0:2376 run %s %s' % (args, name))
    lines = stdout.readlines()
    client.close()
    if len(lines) > 0:
        return lines[0][0:11]
    
    return ''

def stop_container(server, name):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server[0], username=server[1], password=server[2])
    stdin, stdout, stderr = client.exec_command('sudo docker -H tcp://0.0.0.0:2376 rm -f %s' % name)
    errors = stderr.readlines()
    client.close()
    if len(errors) > 0:
        return -1
    
    return 1

def pull_image(server, name):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server[0], username=server[1], password=server[2])
    stdin, stdout, stderr = client.exec_command('sudo docker pull %s' % name)
    errors = stderr.readlines()
    client.close()
    if len(errors) > 0:
        return -1
    
    return 1

def scale_out_container(server, image_name, args, count):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server[0], username=server[1], password=server[2])
    name_list = get_container_list(server, image_name)
    diff = count - len(name_list)
    if diff > 0:
        for i in range(diff):
            stdin, stdout, stderr = client.exec_command('sudo docker -H tcp://0.0.0.0:2376 run %s %s' % (args, image_name))
    elif diff < 0:
        for i in range(-diff):
            stdin, stdout, stderr = client.exec_command('sudo docker -H tcp://0.0.0.0:2376 rm -f %s' % name_list[i])
        
    client.close()
    
def update_load_balancer(server, image_name):
    stop_load_balancer(server)
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server[0], username=server[1], password=server[2])
    name_list = get_container_list(server, image_name)
    links = ['--link %s:%s' % (name, name) for name in name_list]
    stdin, stdout, stderr = client.exec_command('sudo docker run -d --name haproxy -p 80:80 %s tutum/haproxy' % ' '.join(links))
    errors = stderr.readlines()
    client.close()
    if len(errors) > 0:
        return -1
    
    return 1

def get_container_list(server, image_name):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server[0], username=server[1], password=server[2])
    stdin, stdout, stderr = client.exec_command("sudo docker -H tcp://0.0.0.0:2376 ps --format '{{.Image}} {{.Names}}' | grep '%s' | awk '{print $2}'" % image_name)
    lines = stdout.readlines()
    client.close()
    
    return [line.strip() for line in lines]

def stop_load_balancer(server):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server[0], username=server[1], password=server[2])
    stdin, stdout, stderr = client.exec_command('sudo docker rm -f haproxy')
    errors = stderr.readlines()
    client.close()
    if len(errors) > 0:
        return -1
    
    return 1

#################### cluster API ###############################

def get_cluster_info():
    f = urllib.request.urlopen(config.config['swarm_cluster_url'] + "/info")
    content = f.read().decode()
    f.close()
    return content

def list_cluster_containers():
    f = urllib.request.urlopen(config.config['swarm_cluster_url'] + "/containers/json?all=1")
    content = f.read().decode()
    f.close()
    return json.loads(content)

def inspect_cluster_container(cid):
    f = urllib.request.urlopen(config.config['swarm_cluster_url'] + "/containers/%s/json" % cid)
    content = f.read().decode()
    f.close()
    return content

def get_cluster_container_logs(cid):
    f = urllib.request.urlopen(config.config['swarm_cluster_url'] + "/containers/%s/logs?stderr=1&stdout=1" % cid)
    content = f.read().decode()
    f.close()
    return content

def get_cluster_container_status(cid):
    f = urllib.request.urlopen(config.config['swarm_cluster_url'] + "/containers/%s/stats" % cid)
    content = f.read().decode()
    f.close()
    return content

def get_cluster_images():
    f = urllib.request.urlopen(config.config['swarm_cluster_url'] + "/images/json")
    content = f.read().decode()
    f.close()
    return content

def kill_cluster_container(cid):
    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request(config.config['swarm_cluster_url'] + "/containers/%s/kill" % cid, "POST")
    
if __name__ == "__main__":
#     print(start_container('vophoto-test.chinacloudapp.cn', 'vophoto-test.chinacloudapp.cn:5000/ubuntu', '-d --name ubuntu'))
#     stop_container('vophoto-test.chinacloudapp.cn', 'ubuntu')
#     print(pull_image('vophoto-test.chinacloudapp.cn', 'memcached'))
#     print(inspect_container('vophoto-test.chinacloudapp.cn', 'ubuntu'))
#     print(list_vm('vophoto-test.chinacloudapp.cn'))
#     scale_out_container('vophoto-test.chinacloudapp.cn', 'petstore', '-d', 1)
#     update_load_balancer('vophoto-test.chinacloudapp.cn', 'petstore')
    print(('test', 'lat') in [('test', 'la2t')])         
#     print(list_cluster_containers())

