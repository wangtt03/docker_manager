#Encoding=UTF8

import paramiko
from paramiko import SSHClient
import os
import json

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

if __name__ == "__main__":
#     print(start_container('vophoto-test.chinacloudapp.cn', 'vophoto-test.chinacloudapp.cn:5000/ubuntu', '-d --name ubuntu'))
#     stop_container('vophoto-test.chinacloudapp.cn', 'ubuntu')
#     print(pull_image('vophoto-test.chinacloudapp.cn', 'memcached'))
#     print(inspect_container('vophoto-test.chinacloudapp.cn', 'ubuntu'))
    print(list_vm('vophoto-test.chinacloudapp.cn'))

