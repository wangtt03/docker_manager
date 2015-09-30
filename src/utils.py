#Encoding=UTF8

import paramiko
from paramiko import SSHClient
import os
import json
from tkinter import image_names

user_name = 'wangtiantian'
password='1qaz2wsx!QAZ@WSX'

azure_name = 'tiantiaw@cec.partner.onmschina.cn'
azure_pass = '1234qwerQWER'

def run_command(server, cmd):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server, username=user_name, password=password)
    stdin, stdout, stderr = client.exec_command(cmd)
    lines = stdout.readlines()
    client.close()
    return ''.join(lines)
    
def list_vm(server):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server, username=user_name, password=password)
    stdin, stdout, stderr = client.exec_command('sudo docker run --rm microsoft/azure-cli /bin/bash -c "azure login -u %s -p %s -e AzureChinaCloud && azure vm list --json"' % (azure_name, azure_pass))
    lines = stdout.readlines()
    lines = [line for line in lines if not line.startswith('info:')]
    client.close()
    return json.loads(''.join(lines))

def create_vm(server):
    pass

def inspect_container(server, name):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server, username=user_name, password=password)
    stdin, stdout, stderr = client.exec_command('sudo docker inspect %s' % name)
    lines = stdout.readlines()
    client.close()
    return ''.join(lines)
    
def get_container_status(server, name):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server, username=user_name, password=password)
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
    client.connect(server, username=user_name, password=password)
    stdin, stdout, stderr = client.exec_command('sudo docker run %s %s' % (args, name))
    lines = stdout.readlines()
    client.close()
    if len(lines) > 0:
        return lines[0][0:11]
    
    return ''

def stop_container(server, name):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server, username=user_name, password=password)
    stdin, stdout, stderr = client.exec_command('sudo docker rm -f %s' % name)
    errors = stderr.readlines()
    client.close()
    if len(errors) > 0:
        return -1
    
    return 1

def pull_image(server, name):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server, username=user_name, password=password)
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
    client.connect(server, username=user_name, password=password)
    name_list = get_container_list(server, image_name)
    diff = count - len(name_list)
    if diff > 0:
        for i in range(diff):
            stdin, stdout, stderr = client.exec_command('sudo docker run %s %s' % (args, image_name))
    elif diff < 0:
        for i in range(-diff):
            stdin, stdout, stderr = client.exec_command('sudo docker rm -f %s' % name_list[i])
        
    client.close()
    
def update_load_balancer(server, image_name):
    stop_load_balancer(server)
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server, username=user_name, password=password)
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
    client.connect(server, username=user_name, password=password)
    stdin, stdout, stderr = client.exec_command("sudo docker ps --format '{{.Image}} {{.Names}}' | grep '%s' | awk '{print $2}'" % image_name)
    lines = stdout.readlines()
    client.close()
    
    return [line.strip() for line in lines]

def stop_load_balancer(server):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    client.load_system_host_keys()
    client.connect(server, username=user_name, password=password)
    stdin, stdout, stderr = client.exec_command('sudo docker rm -f haproxy')
    errors = stderr.readlines()
    client.close()
    if len(errors) > 0:
        return -1
    
    return 1

if __name__ == "__main__":
#     print(start_container('vophoto-test.chinacloudapp.cn', 'vophoto-test.chinacloudapp.cn:5000/ubuntu', '-d --name ubuntu'))
#     stop_container('vophoto-test.chinacloudapp.cn', 'ubuntu')
#     print(pull_image('vophoto-test.chinacloudapp.cn', 'memcached'))
#     print(inspect_container('vophoto-test.chinacloudapp.cn', 'ubuntu'))
#     print(list_vm('vophoto-test.chinacloudapp.cn'))
    scale_out_container('vophoto-test.chinacloudapp.cn', 'tutum/hello-world', '-d', 1)
    update_load_balancer('vophoto-test.chinacloudapp.cn', 'tutum/hello-world')

