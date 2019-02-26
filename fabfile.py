"""REMOTE SERVER CONTROLS
file has to be named fabfile, functions are accessed from console
using "fab <functionname>" """

from fabric import task
from fabric import Connection
#from fabric.connection import put

c = Connection(
        user='ec2-user',
        host='ec2-18-184-212-150.eu-central-1.compute.amazonaws.com',
        connect_kwargs={'key_filename': '../../sshmatt3000.pem'}
    )

#CMD = '/home/ec2-user/product-api/hello.py'

@task
def basics(context):
    '''installs basic python and git on server'''
    c.run('sudo yum -y install python3')
    c.run('sudo yum -y install git')
#    c.run('sudo pip3 install --user -r display/requirements.txt') #problematic if requirements.txt was created using anaconda
    
@task
def requirements(context):
    '''installs python modules from requirements.txt'''
    with c.cd('product-api'):
        c.run('sudo pip3 install -r requirements.txt')
    
@task
def clone(context):
    c.run('git clone https://github.com/mheerens/product-api.git')
    
@task
def credentials(context):
    '''sends credentials.py to server'''
    c.put("credentials.py")
    c.run('mv credentials.py product-api/credentials.py')

@task
def pull(context):
    with c.cd('product-api'):
        c.run("pwd")
        c.run('git pull')
        
@task
def run(context):
    with c.cd('product-api'):
        c.run("FLASK_APP=api.py flask run --host=0.0.0.0 --port=8080")
#        c.run("export FLASK_APP=hello.py")
#        c.run(f'flask run')

@task
def reset(context):
    c.run('rm product-api -rf')
    c.run('git clone https://github.com/mheerens/product-api.git')

